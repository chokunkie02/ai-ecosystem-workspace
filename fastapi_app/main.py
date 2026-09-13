import io
import json
import os
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

from datasets import load_dataset
from fastapi import FastAPI, HTTPException, Query
from minio import Minio
from pydantic import BaseModel, Field
import redis

app = FastAPI(
    title="MLOps Serving & Trainer Queue API",
    description="API for scheduled training jobs and asynchronous NER inference serving with Redis & MLflow.",
    version="1.0.0"
)

# Config from Environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadminpassword")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

QUEUE_NAME = "scheduled_training_queue"
INFERENCE_QUEUE_PRIMARY = "inference_queue"
INFERENCE_QUEUE_SECONDARY = "inference_jobs_queue"
DATASET_BUCKET = "datasets"
MODEL_BUCKET = "models"
DEFAULT_JOB_TTL = 3600  # 1 hour TTL for prediction job status & results in Redis


@app.on_event("startup")
def startup_event():
    """Ensure required MinIO buckets exist on startup."""
    for bucket in [DATASET_BUCKET, MODEL_BUCKET]:
        try:
            if not minio_client.bucket_exists(bucket):
                minio_client.make_bucket(bucket)
        except Exception as e:
            # MinIO might still be booting up in Docker Compose
            print(f"[Warning] Could not initialize bucket '{bucket}': {e}")


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class EnqueueRequest(BaseModel):
    job_id: str = "job_001"
    dataset_name: str = "conll2003"
    base_model: str = "bert-base-cased"
    delay_seconds: int = 10  # Seconds from now to start training


class PredictRequest(BaseModel):
    text: str = Field(..., description="Raw text to run Named Entity Recognition (NER) inference on", min_length=1)
    model_name: Optional[str] = Field(None, description="Optional target model name in MLflow registry")
    model_version: Optional[str] = Field(None, description="Optional target model version or run ID")


class PredictResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    created_at: Optional[str] = None
    queue_name: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Core System Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "service": "MLOps Serving & Trainer Queue API",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "predict": "/api/v1/predict",
            "predict_status": "/api/v1/predict/{job_id}",
            "models_status": "/api/v1/models/status",
            "train_enqueue": "/api/v1/train/enqueue",
            "queue_status": "/api/v1/queue/status",
            "dataset_import": "/api/v1/dataset/import"
        }
    }


# ---------------------------------------------------------------------------
# Dataset & Training Endpoints (Preserved)
# ---------------------------------------------------------------------------

@app.post("/api/v1/dataset/import")
def import_dataset(dataset_name: str = "conll2003"):
    """Load dataset from Hugging Face and store in MinIO."""
    try:
        try:
            dataset = load_dataset(dataset_name)
        except Exception:
            # Fallback for conll2003 repository path on Hugging Face Hub
            dataset = load_dataset("eriktks/conll2003" if dataset_name == "conll2003" else dataset_name)

        # Convert to JSON format in memory
        json_data = json.dumps(dataset['train'].to_dict()).encode('utf-8')
        data_stream = io.BytesIO(json_data)

        object_name = f"{dataset_name}_train.json"
        minio_client.put_object(
            DATASET_BUCKET,
            object_name,
            data_stream,
            length=len(json_data),
            content_type="application/json"
        )
        return {
            "status": "success",
            "message": f"Dataset {dataset_name} imported into MinIO bucket '{DATASET_BUCKET}' as '{object_name}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/train/enqueue")
def enqueue_training(req: EnqueueRequest):
    """Enqueue a training job with a scheduled start timestamp."""
    scheduled_at = int(time.time()) + req.delay_seconds
    job_payload = {
        "job_id": req.job_id,
        "dataset_name": req.dataset_name,
        "base_model": req.base_model,
        "dataset_object": f"{req.dataset_name}_train.json",
        "scheduled_at": scheduled_at,
        "enqueued_at": int(time.time())
    }

    # Store in Redis Sorted Set with scheduled_at as score
    redis_client.zadd(QUEUE_NAME, {json.dumps(job_payload): scheduled_at})

    scheduled_dt = datetime.fromtimestamp(scheduled_at).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "status": "enqueued",
        "queue_name": QUEUE_NAME,
        "job_id": req.job_id,
        "scheduled_at_timestamp": scheduled_at,
        "scheduled_at_datetime": scheduled_dt,
        "delay_seconds": req.delay_seconds
    }


@app.get("/api/v1/queue/status")
def queue_status():
    """List pending scheduled training jobs in Redis."""
    jobs_raw = redis_client.zrange(QUEUE_NAME, 0, -1, withscores=True)
    jobs = []
    current_time = time.time()
    for item, score in jobs_raw:
        payload = json.loads(item)
        jobs.append({
            "job": payload,
            "scheduled_score": score,
            "is_due": score <= current_time,
            "seconds_remaining": max(0, int(score - current_time))
        })
    return {"queue_name": QUEUE_NAME, "total_jobs": len(jobs), "jobs": jobs}


# ---------------------------------------------------------------------------
# Prediction & Serving Endpoints
# ---------------------------------------------------------------------------

def _enqueue_prediction_job(request: PredictRequest, wait: bool = False, timeout_seconds: float = 10.0) -> Dict[str, Any]:
    """Helper to enqueue a prediction job to Redis and optionally wait for result."""
    job_id = str(uuid.uuid4())
    created_timestamp = time.time()
    created_at_str = datetime.fromtimestamp(created_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    # Initial metadata payload
    initial_metadata = {
        "job_id": job_id,
        "status": "PENDING",
        "text": request.text,
        "model_name": request.model_name,
        "model_version": request.model_version,
        "created_at": created_at_str,
        "created_timestamp": created_timestamp,
    }

    # 1. Record initial state in Redis with TTL
    redis_client.set(f"job:{job_id}:status", "PENDING", ex=DEFAULT_JOB_TTL)
    redis_client.set(f"predict_job:{job_id}", json.dumps(initial_metadata), ex=DEFAULT_JOB_TTL)

    # 2. Push job into both inference queues to ensure full compatibility
    queue_item = {
        "job_id": job_id,
        "text": request.text,
        "model_name": request.model_name,
        "model_version": request.model_version,
        "created_at": created_at_str,
    }
    item_json = json.dumps(queue_item)
    redis_client.rpush(INFERENCE_QUEUE_PRIMARY, item_json)
    redis_client.rpush(INFERENCE_QUEUE_SECONDARY, item_json)

    # 3. If wait=False, return immediately with PENDING status
    if not wait:
        return {
            "job_id": job_id,
            "status": "PENDING",
            "result": None,
            "created_at": created_at_str,
            "queue_name": INFERENCE_QUEUE_PRIMARY,
        }

    # 4. If wait=True, poll Redis for completion up to timeout_seconds
    start_wait = time.time()
    poll_interval = 0.2  # 200ms polling

    while time.time() - start_wait < timeout_seconds:
        status = redis_client.get(f"job:{job_id}:status") or "PENDING"
        if status == "COMPLETED":
            result_raw = redis_client.get(f"job:{job_id}:result")
            result = json.loads(result_raw) if result_raw else None
            return {
                "job_id": job_id,
                "status": "COMPLETED",
                "result": result,
                "created_at": created_at_str,
            }
        elif status == "FAILED":
            error_msg = redis_client.get(f"job:{job_id}:error") or "Inference failed"
            return {
                "job_id": job_id,
                "status": "FAILED",
                "result": None,
                "error": error_msg,
                "created_at": created_at_str,
            }
        time.sleep(poll_interval)

    # If timeout reached while waiting, return current status (likely PROCESSING or PENDING)
    current_status = redis_client.get(f"job:{job_id}:status") or "PENDING"
    return {
        "job_id": job_id,
        "status": current_status,
        "result": None,
        "message": f"Wait timeout ({timeout_seconds}s) exceeded. Query /api/v1/predict/{job_id} for updates.",
        "created_at": created_at_str,
    }


def _get_prediction_job_status(job_id: str) -> Dict[str, Any]:
    """Helper to fetch prediction job status and result from Redis."""
    # Check simple status key
    status = redis_client.get(f"job:{job_id}:status")
    meta_raw = redis_client.get(f"predict_job:{job_id}")

    if not status and not meta_raw:
        raise HTTPException(status_code=404, detail=f"Prediction job '{job_id}' not found.")

    status = status or "PENDING"
    result = None
    error = None

    # Fetch result if completed
    result_raw = redis_client.get(f"job:{job_id}:result")
    if result_raw:
        try:
            result = json.loads(result_raw)
        except Exception:
            result = result_raw

    # Check for error
    error_raw = redis_client.get(f"job:{job_id}:error")
    if error_raw:
        error = error_raw

    # Check meta json if result was not in separate key
    if result is None and meta_raw:
        try:
            meta_json = json.loads(meta_raw)
            if "result" in meta_json and meta_json["result"] is not None:
                result = meta_json["result"]
            if "error" in meta_json and meta_json["error"]:
                error = meta_json["error"]
            if not status and "status" in meta_json:
                status = meta_json["status"]
        except Exception:
            pass

    return {
        "job_id": job_id,
        "status": status,
        "result": result,
        "error": error,
    }


# Endpoints for POST /predict & /api/v1/predict
@app.post("/predict", response_model=PredictResponse, tags=["Inference"])
@app.post("/api/v1/predict", response_model=PredictResponse, tags=["Inference"])
def create_prediction(request: PredictRequest, wait: bool = Query(False, description="Wait for inference completion")):
    """Submit a text sample for asynchronous Named Entity Recognition inference."""
    return _enqueue_prediction_job(request, wait=wait)


# Endpoints for GET /predict/{job_id} & /api/v1/predict/{job_id}
@app.get("/predict/{job_id}", tags=["Inference"])
@app.get("/api/v1/predict/{job_id}", tags=["Inference"])
def get_prediction(job_id: str):
    """Retrieve the status and results of an inference job by its ID."""
    return _get_prediction_job_status(job_id)


# Endpoint for GET /api/v1/models/status
@app.get("/api/v1/models/status", tags=["Models"])
def get_models_status():
    """
    Check the current active model information from Redis and MLflow tracking server.
    """
    # 1. Fetch latest model metadata from Redis
    latest_model_info = None
    latest_info_raw = redis_client.get("latest_model_info")
    if latest_info_raw:
        try:
            latest_model_info = json.loads(latest_info_raw)
        except Exception:
            latest_model_info = latest_info_raw

    # 2. Check MLflow server connectivity
    mlflow_available = False
    mlflow_details = {}
    try:
        health_url = f"{MLFLOW_TRACKING_URI.rstrip('/')}/health"
        req = urllib.request.Request(health_url, headers={"User-Agent": "FastAPI-StatusCheck"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                mlflow_available = True
                mlflow_details = {"status": "healthy", "url": MLFLOW_TRACKING_URI}
    except Exception as e:
        mlflow_details = {"status": "unreachable", "error": str(e), "url": MLFLOW_TRACKING_URI}

    # 3. Check Redis Queue statistics
    primary_queue_len = 0
    secondary_queue_len = 0
    scheduled_queue_len = 0
    try:
        primary_queue_len = redis_client.llen(INFERENCE_QUEUE_PRIMARY)
        secondary_queue_len = redis_client.llen(INFERENCE_QUEUE_SECONDARY)
        scheduled_queue_len = redis_client.zcard(QUEUE_NAME)
    except Exception as e:
        print(f"[Warning] Error querying Redis queues: {e}")

    return {
        "status": "ready" if (latest_model_info or mlflow_available) else "initializing",
        "latest_model_info": latest_model_info,
        "mlflow_server": mlflow_details,
        "queue_lengths": {
            INFERENCE_QUEUE_PRIMARY: primary_queue_len,
            INFERENCE_QUEUE_SECONDARY: secondary_queue_len,
            QUEUE_NAME: scheduled_queue_len,
        },
        "timestamp": time.time(),
    }
