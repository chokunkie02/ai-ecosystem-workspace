import time
import json
import os
import redis
from minio import Minio
import logging
from train import run_training

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadminpassword")

QUEUE_NAME = "scheduled_training_queue"
DATASET_BUCKET = "datasets"
MODEL_BUCKET = "models"

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def setup_worker_logger(job_id):
    log_filename = f"training_{job_id}.log"
    logger = logging.getLogger(f"Worker_{job_id}")
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    
    # Stream handler
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger, log_filename

def main():
    print("Trainer Worker started. Listening for scheduled jobs in Redis...")
    while True:
        try:
            current_time = time.time()
            # Fetch jobs whose score (scheduled_at) is <= current_time
            due_jobs = redis_client.zrangebyscore(QUEUE_NAME, 0, current_time, start=0, num=1)
            
            if due_jobs:
                job_raw = due_jobs[0]
                # Atomic remove to prevent duplicate worker processing
                removed = redis_client.zrem(QUEUE_NAME, job_raw)
                if removed:
                    job_data = json.loads(job_raw)
                    job_id = job_data.get("job_id", "job_unknown")
                    logger, log_file = setup_worker_logger(job_id)
                    
                    logger.info(f"== Starting Job {job_id} ==")
                    logger.info(f"Payload: {job_data}")
                    
                    # 1. Download Dataset from MinIO
                    dataset_object = job_data.get("dataset_object", "conll2003_train.json")
                    local_dataset_path = f"./local_{dataset_object}"
                    logger.info(f"Downloading {dataset_object} from MinIO bucket '{DATASET_BUCKET}'...")
                    minio_client.fget_object(DATASET_BUCKET, dataset_object, local_dataset_path)
                    logger.info(f"Downloaded dataset to {local_dataset_path}")
                    
                    # 2. Train Model with MLflow Tracking
                    base_model = job_data.get("base_model", "bert-base-cased")
                    num_epochs = int(job_data.get("epochs", 1))
                    batch_size = int(job_data.get("batch_size", 8))
                    learning_rate = float(job_data.get("learning_rate", 5e-5))
                    experiment_name = job_data.get("experiment_name", "bert-ner-training")
                    registered_model_name = job_data.get("registered_model_name", "bert-ner")
                    output_dir = f"./output_{job_id}"
                    
                    logger.info(f"Initiating model training with base model '{base_model}'...")
                    train_info = run_training(
                        dataset_path=local_dataset_path,
                        base_model_name=base_model,
                        output_dir=output_dir,
                        logger=logger,
                        num_epochs=num_epochs,
                        batch_size=batch_size,
                        learning_rate=learning_rate,
                        experiment_name=experiment_name,
                        registered_model_name=registered_model_name,
                    )
                    
                    run_id = train_info.get("run_id") if isinstance(train_info, dict) else None
                    model_uri = train_info.get("model_uri") if isinstance(train_info, dict) else None
                    reg_name = train_info.get("registered_model_name", registered_model_name) if isinstance(train_info, dict) else registered_model_name
                    metrics = train_info.get("metrics", {}) if isinstance(train_info, dict) else {}
                    
                    logger.info(f"Training completed. MLflow Run ID: {run_id}, Model URI: {model_uri}")
                    
                    # 3. Save Model Archive to MinIO (Backup/Artifact)
                    minio_model_name = f"model_{job_id}_bert_token_cls.tar.gz"
                    tar_path = f"./{minio_model_name}"
                    os.system(f"tar -czf {tar_path} -C {output_dir} .")
                    
                    logger.info(f"Uploading trained model {minio_model_name} to MinIO bucket '{MODEL_BUCKET}'...")
                    minio_client.fput_object(MODEL_BUCKET, minio_model_name, tar_path)
                    
                    # 4. Upload Log File to MinIO
                    logger.info(f"Uploading log file {log_file} to MinIO bucket '{MODEL_BUCKET}'...")
                    minio_client.fput_object(MODEL_BUCKET, log_file, log_file)
                    
                    # 5. Store Latest Model Discovery Metadata in Redis for Inference Worker
                    latest_model_payload = {
                        "job_id": job_id,
                        "run_id": run_id,
                        "model_name": reg_name,
                        "model_uri": model_uri,
                        "registered_model_name": reg_name,
                        "minio_tar": minio_model_name,
                        "metrics": metrics,
                        "updated_at": time.time(),
                    }
                    redis_client.set("latest_model_info", json.dumps(latest_model_payload))
                    logger.info(f"Updated Redis key 'latest_model_info': {latest_model_payload}")
                    
                    logger.info(f"== Job {job_id} Completed Successfully ==")
            else:
                time.sleep(2)
        except Exception as e:
            print(f"[Worker Error] {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
