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
                    
                    # 2. Train Model
                    base_model = job_data.get("base_model", "bert-base-cased")
                    output_dir = f"./output_{job_id}"
                    logger.info(f"Initiating model training with base model '{base_model}'...")
                    run_training(local_dataset_path, base_model, output_dir, logger)
                    
                    # 3. Save Model to MinIO
                    minio_model_name = f"model_{job_id}_bert_token_cls.tar.gz"
                    tar_path = f"./{minio_model_name}"
                    os.system(f"tar -czf {tar_path} -C {output_dir} .")
                    
                    logger.info(f"Uploading trained model {minio_model_name} to MinIO bucket '{MODEL_BUCKET}'...")
                    minio_client.fput_object(MODEL_BUCKET, minio_model_name, tar_path)
                    
                    # 4. Upload Log File to MinIO
                    logger.info(f"Uploading log file {log_file} to MinIO bucket '{MODEL_BUCKET}'...")
                    minio_client.fput_object(MODEL_BUCKET, log_file, log_file)
                    
                    logger.info(f"== Job {job_id} Completed Successfully ==")
            else:
                time.sleep(2)
        except Exception as e:
            print(f"[Worker Error] {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
