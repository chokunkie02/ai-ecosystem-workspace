import json
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from minio import Minio
from datasets import load_dataset
import os
import io

app = FastAPI(title="Trainer Queue API")

# Config from Environment
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadminpassword")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

QUEUE_NAME = "scheduled_training_queue"
DATASET_BUCKET = "datasets"
MODEL_BUCKET = "models"

@app.on_event("startup")
def startup_event():
    for bucket in [DATASET_BUCKET, MODEL_BUCKET]:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)

class EnqueueRequest(BaseModel):
    job_id: str = "job_001"
    dataset_name: str = "conll2003"
    base_model: str = "bert-base-cased"
    delay_seconds: int = 10  # Seconds from now to start training

@app.get("/")
def read_root():
    return {"message": "Trainer Queue API Service is Running"}

@app.post("/api/v1/dataset/import")
def import_dataset(dataset_name: str = "conll2003"):
    """Load dataset from Hugging Face and store in MinIO"""
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
    """Enqueue a training job with a scheduled start timestamp"""
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
    """List pending scheduled training jobs in Redis"""
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
