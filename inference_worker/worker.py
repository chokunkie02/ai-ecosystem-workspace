import os
import time
import json
import logging
import redis
from transformers import pipeline

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("InferenceWorker")

# Environment Configurations
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "bert-ner")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL_NAME", "dslim/bert-base-NER")
RESULT_TTL = int(os.getenv("RESULT_TTL", 3600))
MODEL_CHECK_INTERVAL = int(os.getenv("MODEL_CHECK_INTERVAL", 10))

# AWS / MinIO Configurations for MLflow Artifact Retrieval
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://minio:9000")
os.environ["MLFLOW_S3_IGNORE_TLS"] = os.getenv("MLFLOW_S3_IGNORE_TLS", "true")

# Supported Redis Queues (support both primary and secondary names)
INFERENCE_QUEUES = ["inference_queue", "inference_jobs_queue"]

# Global Model & State
ner_pipeline = None
current_model_source = "None"
current_model_version = "None"
last_model_check_time = 0.0

# Initialize Redis Client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


def load_model_from_mlflow(model_uri_or_name: str):
    """
    Attempt to load a model pipeline from MLflow Tracking Server / Registry.
    """
    import mlflow
    import mlflow.transformers

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    logger.info(f"Attempting to load model from MLflow: {model_uri_or_name}")

    try:
        loaded_pipe = mlflow.transformers.load_model(model_uri_or_name)
        return loaded_pipe
    except Exception as e:
        logger.warning(f"mlflow.transformers.load_model failed: {e}. Trying mlflow.pyfunc.load_model...")
        loaded_pyfunc = mlflow.pyfunc.load_model(model_uri_or_name)
        return loaded_pyfunc


def load_fallback_model():
    """
    Load Hugging Face base model pipeline as fallback when MLflow model is unavailable.
    """
    logger.info(f"Loading fallback HuggingFace base model: '{FALLBACK_MODEL_NAME}'...")
    pipe = pipeline(
        "token-classification",
        model=FALLBACK_MODEL_NAME,
        aggregation_strategy="simple"
    )
    logger.info(f"Fallback model '{FALLBACK_MODEL_NAME}' successfully loaded.")
    return pipe


def init_or_reload_model(force: bool = False):
    """
    Initialize model or check if a newer model is available in MLflow/Redis.
    """
    global ner_pipeline, current_model_source, current_model_version, last_model_check_time

    now = time.time()
    if not force and (now - last_model_check_time < MODEL_CHECK_INTERVAL) and ner_pipeline is not None:
        return

    last_model_check_time = now

    # 1. Check Redis for 'latest_model_info' set by Trainer Worker
    latest_info_raw = None
    try:
        latest_info_raw = redis_client.get("latest_model_info")
    except Exception as redis_err:
        logger.warning(f"Could not check Redis for latest_model_info: {redis_err}")

    latest_run_id = None
    target_uri = None

    if latest_info_raw:
        try:
            latest_info = json.loads(latest_info_raw)
            latest_run_id = latest_info.get("run_id")
            target_uri = latest_info.get("model_uri") or f"runs:/{latest_run_id}/model"
        except Exception as parse_err:
            logger.warning(f"Error parsing latest_model_info: {parse_err}")

    # If we already loaded this exact run_id, no reload is needed
    if ner_pipeline is not None and latest_run_id and current_model_version == latest_run_id and not force:
        return

    # 2. Try loading target MLflow model
    loaded_model = None
    source_desc = None
    version_desc = None

    # Candidate 1: Latest run model from Redis pointer
    if target_uri:
        try:
            loaded_model = load_model_from_mlflow(target_uri)
            source_desc = f"MLflow Run ({target_uri})"
            version_desc = latest_run_id
        except Exception as e:
            logger.warning(f"Failed loading MLflow model from {target_uri}: {e}")

    # Candidate 2: Registered Model 'models:/{MODEL_NAME}/latest'
    if loaded_model is None:
        for stage_or_ver in ["latest", "1"]:
            reg_uri = f"models:/{MODEL_NAME}/{stage_or_ver}"
            try:
                loaded_model = load_model_from_mlflow(reg_uri)
                source_desc = f"MLflow Registry ({reg_uri})"
                version_desc = f"{MODEL_NAME}:{stage_or_ver}"
                break
            except Exception as reg_err:
                logger.debug(f"Registry URI {reg_uri} not available: {reg_err}")

    # Candidate 3: Fallback HuggingFace pipeline
    if loaded_model is None:
        if ner_pipeline is None or force:
            logger.info("No trained model found in MLflow. Initializing base fallback model...")
            try:
                loaded_model = load_fallback_model()
                source_desc = f"HuggingFace Base ({FALLBACK_MODEL_NAME})"
                version_desc = "base-fallback"
            except Exception as fb_err:
                logger.error(f"Critical error loading fallback model: {fb_err}")
                if ner_pipeline is None:
                    raise fb_err
        else:
            # Keep existing pipeline
            return

    if loaded_model is not None:
        ner_pipeline = loaded_model
        current_model_source = source_desc
        current_model_version = version_desc
        logger.info(f"Model active: {current_model_source} [Version: {current_model_version}]")


def execute_inference(text: str) -> list:
    """
    Execute NER token classification inference on input text and format entities.
    """
    if not text or not text.strip():
        return []

    if ner_pipeline is None:
        init_or_reload_model(force=True)

    # Run inference
    raw_results = ner_pipeline(text)

    # Handle pipeline vs pyfunc output differences
    if isinstance(raw_results, dict) and "entities" in raw_results:
        raw_results = raw_results["entities"]
    elif isinstance(raw_results, list) and len(raw_results) > 0 and isinstance(raw_results[0], list):
        raw_results = raw_results[0]

    formatted_entities = []
    if isinstance(raw_results, list):
        for item in raw_results:
            if isinstance(item, dict):
                entity_label = (
                    item.get("entity_group")
                    or item.get("entity")
                    or item.get("label")
                    or "ENTITY"
                )
                word = item.get("word") or item.get("text") or ""
                score = float(item.get("score", 0.0))
                start_idx = item.get("start")
                end_idx = item.get("end")

                entity_dict = {
                    "entity": str(entity_label),
                    "word": str(word).strip(),
                    "score": round(score, 4),
                }
                if start_idx is not None:
                    entity_dict["start"] = int(start_idx)
                if end_idx is not None:
                    entity_dict["end"] = int(end_idx)

                formatted_entities.append(entity_dict)

    return formatted_entities


def process_inference_job(raw_job_payload: str):
    """
    Process an individual prediction task popped from Redis.
    """
    try:
        job_data = json.loads(raw_job_payload)
    except Exception as parse_err:
        logger.error(f"Failed to parse job JSON: {parse_err}")
        return

    job_id = job_data.get("job_id", f"job_{int(time.time()*1000)}")
    text = job_data.get("text", "")

    print(f"[Inference Worker] Processing job {job_id}...")
    start_time = time.time()

    # 1. Update job status to PROCESSING
    try:
        redis_client.set(f"job:{job_id}:status", "PROCESSING", ex=RESULT_TTL)
        redis_client.set(
            f"predict_job:{job_id}",
            json.dumps({
                "job_id": job_id,
                "status": "PROCESSING",
                "text": text,
                "started_at": start_time,
            }),
            ex=RESULT_TTL,
        )
    except Exception as redis_err:
        logger.warning(f"Failed to record PROCESSING status for job {job_id}: {redis_err}")

    # 2. Run Inference
    try:
        entities = execute_inference(text)
        latency_ms = round((time.time() - start_time) * 1000, 2)

        result_payload = {
            "job_id": job_id,
            "text": text,
            "entities": entities,
            "model_source": current_model_source,
            "latency_ms": latency_ms,
        }

        # 3. Store Result and COMPLETED status in Redis
        redis_client.set(f"job:{job_id}:result", json.dumps(result_payload), ex=RESULT_TTL)
        redis_client.set(f"job:{job_id}:status", "COMPLETED", ex=RESULT_TTL)
        redis_client.set(
            f"predict_job:{job_id}",
            json.dumps({
                "job_id": job_id,
                "status": "COMPLETED",
                "result": result_payload,
                "latency_ms": latency_ms,
                "completed_at": time.time(),
            }),
            ex=RESULT_TTL,
        )

        print(f"[Inference Worker] Processing job {job_id}... Done")
        logger.info(f"Job {job_id} completed in {latency_ms}ms with {len(entities)} entities detected.")

    except Exception as infer_err:
        logger.error(f"[Inference Worker] Error processing job {job_id}: {infer_err}")
        try:
            redis_client.set(f"job:{job_id}:status", "FAILED", ex=RESULT_TTL)
            redis_client.set(f"job:{job_id}:error", str(infer_err), ex=RESULT_TTL)
            redis_client.set(
                f"predict_job:{job_id}",
                json.dumps({
                    "job_id": job_id,
                    "status": "FAILED",
                    "error": str(infer_err),
                    "failed_at": time.time(),
                }),
                ex=RESULT_TTL,
            )
        except Exception as redis_err:
            logger.error(f"Failed to write failure status to Redis for job {job_id}: {redis_err}")


def main():
    logger.info("Starting Inference Worker service...")
    logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    logger.info(f"Connecting to MLflow Tracking Server at {MLFLOW_TRACKING_URI}...")

    # Initial Model Load
    init_or_reload_model(force=True)

    logger.info(f"Inference Worker listening on Redis queues: {INFERENCE_QUEUES}...")

    while True:
        try:
            # Check if there is an updated model available periodically
            init_or_reload_model(force=False)

            # Blocking pop with 2 seconds timeout from Redis queues
            item = redis_client.blpop(INFERENCE_QUEUES, timeout=2)
            if item:
                queue_name, raw_payload = item
                process_inference_job(raw_payload)

        except redis.ConnectionError as conn_err:
            logger.error(f"Redis connection error: {conn_err}. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Worker interrupted by user. Shutting down cleanly.")
            break
        except Exception as loop_err:
            logger.error(f"Unexpected worker loop exception: {loop_err}")
            time.sleep(2)


if __name__ == "__main__":
    main()
