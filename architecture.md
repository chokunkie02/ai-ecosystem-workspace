# System Architecture: AI Ecosystem MLOps Serving & Training

This document maps out the system architecture, directory layout, data flows, and state machines for the MLOps Training & Inference Ecosystem integrating FastAPI, Redis Queue, MinIO, PostgreSQL, MLflow Tracking Server, Trainer Worker (GPU), and Inference Worker.

## 1. Directory Structure

```text
C:\eco\friday\
├── fastapi_app/                 # FastAPI REST API Gateway
│   ├── Dockerfile               # Container build file for FastAPI service
│   ├── main.py                  # API routes (dataset import, train queue, predict queue, job status)
│   └── requirements.txt         # FastAPI, pydantic, redis, minio, datasets, uvicorn
├── trainer_worker/              # Async Background Training Worker
│   ├── Dockerfile               # Container build file with CUDA/PyTorch support
│   ├── train.py                 # Training script with MLflow logging & metrics tracking
│   ├── worker.py                # Redis queue listener & job orchestrator
│   └── requirements.txt         # PyTorch, transformers, seqeval, minio, redis, mlflow
├── inference_worker/            # Async Background Inference Worker
│   ├── Dockerfile               # Container build file for inference runtime
│   ├── worker.py                # Redis queue listener, model fetcher from MLflow/MinIO, prediction engine
│   └── requirements.txt         # PyTorch, transformers, minio, redis, mlflow
├── backend/                     # Modular backend libraries & configs
│   ├── core/                    # Environment settings (Redis, MinIO, MLflow, Postgres)
│   └── ...
├── apps/                        # Sub-applications & services
├── libs/                        # Shared SDK wrappers (minio_client, redis_client)
├── storage/                     # Persistent volumes & local caches
│   ├── artifacts/               # Generated reports and test artifacts
│   ├── data/                    # Datasets & local storage
│   └── log/                     # Application & container execution logs
├── compose.yml                  # Docker Compose multi-container orchestrator
├── task-graph.md                # Living roadmap and autonomous execution blueprint
├── architecture.md              # System architecture specification & data flows
├── architecture_diagram.drawio  # Visual architecture diagram (Draw.io)
└── skill-instructions.md        # Workspace development rules & conventions
```

> **Note on Non-Code Artifacts**: In accordance with user requirements, all handwritten report guides, theoretical summaries, and study materials for conversion to PDF are isolated under `C:\Users\kt856\Downloads\oat\`.

---

## 2. Multi-Container Architecture & Data Flow

```text
                        ┌───────────────────────────────┐
                        │      Client / Web User        │
                        └──────┬─────────────────▲──────┘
             1. Enqueue Job    │                 │ 6. Query Job Result
             (Train / Predict) │                 │    (GET /predict/{job_id})
                               ▼                 │
                        ┌────────────────────────┴──────┐
                        │     FastAPI App (:8000)       │
                        └──────┬─────────────────┬──────┘
                               │                 │
             2. Push Task      │                 │ 2. Push Predict Job
             (ZADD train)      ▼                 ▼ (LPUSH inference)
                        ┌───────────────────────────────┐
                        │      Redis In-Memory Bus      │
                        │ - scheduled_training_queue    │
                        │ - inference_jobs_queue        │
                        │ - inference_results (hash/kv) │
                        └──────┬─────────────────┬──────┘
                               │                 │
             3. Poll Training  │                 │ 4. Poll Inference
             Job (When Due)    ▼                 ▼ Job (BRPOP)
             ┌─────────────────────────┐  ┌─────────────────────────┐
             │  Trainer Worker (GPU)   │  │    Inference Worker     │
             │   (trainer_worker)      │  │   (inference_worker)    │
             └──────┬────────────┬─────┘  └─────▲─────────────┬─────┘
                    │            │              │             │
                    │ Log Params │ Fetch Model  │             │ 5. Store Prediction
                    │ & Metrics  │ Artifact     │             │    Result in Redis
                    ▼            │              │             ▼
    ┌──────────────────────────┐ │              │     ┌──────────────────┐
    │  MLflow Tracking Server  │─┘              │     │  Redis Job Cache │
    │       (Port 5000)        │────────────────┘     │ (Key: {job_id})  │
    └──────┬────────────┬──────┘                      └──────────────────┘
           │            │
           │ Metadata   │ Artifacts
           ▼            ▼
    ┌─────────────┐  ┌───────────────────────────────────┐
    │ PostgreSQL  │  │        MinIO Object Storage       │
    │  (:5432)    │  │       (:9000 API, :9001 Web)      │
    │ (Backend    │  │ - Bucket 'datasets' (Raw data)    │
    │  Store)     │  │ - Bucket 'models'   (Model files) │
    │             │  │ - Bucket 'mlflow'   (Run output)  │
    └─────────────┘  └───────────────────────────────────┘
```

---

## 3. Core Component Breakdown

| Service Component | Port(s) | Technology | Responsibilities |
| :--- | :--- | :--- | :--- |
| **FastAPI Gateway** | `8000` | FastAPI, Uvicorn, Python 3.11 | - Data ingestion (`/api/v1/dataset/import`)<br>- Training queue scheduling (`/api/v1/train/enqueue`)<br>- Prediction request enqueueing (`/api/v1/predict`)<br>- Prediction status/result retrieval (`/api/v1/predict/{job_id}`) |
| **Redis Broker** | `6379` | Redis 7 Alpine | - Sorted Set for scheduled training (`scheduled_training_queue`)<br>- List for asynchronous inference tasks (`inference_jobs_queue`)<br>- Key-Value/Hash cache for inference results with TTL |
| **PostgreSQL** | `5432` | PostgreSQL 16 Alpine | - Relational backend store for MLflow tracking metadata (experiments, runs, metrics, params, model registry tags) |
| **MinIO Storage** | `9000`, `9001` | MinIO RELEASE | - S3-compatible object storage.<br>- `datasets`: Raw/processed training data.<br>- `models`: Archived checkpoints.<br>- `mlflow`: MLflow artifact root store. |
| **MLflow Server** | `5000` | MLflow Tracking Server | - Centralized MLOps tracking and model registry.<br>- Connects to PostgreSQL (`--backend-store-uri`) and MinIO (`--default-artifact-root s3://models/mlflow`). |
| **Trainer Worker** | Background | PyTorch, Hugging Face, MLflow | - Consumes scheduled training tasks from Redis.<br>- Streams training metrics (loss, F1, precision, recall) to MLflow.<br>- Saves trained model weights to MLflow artifacts and MinIO. |
| **Inference Worker**| Background | PyTorch, Hugging Face, MLflow | - Loads latest or specified model run directly from MLflow / MinIO.<br>- Continuously pops prediction tasks from `inference_jobs_queue`.<br>- Computes Named Entity Recognition (NER) tokens and labels.<br>- Stores outputs in Redis against `job_id`. |

---

## 4. Inference State Machine & Lifecycle

```text
[Client: POST /predict]
       │
       ▼
[FastAPI: Generate job_id, push to Redis 'inference_jobs_queue']
       │
       ├──> Return {"job_id": "<uuid>", "status": "PENDING"} to Client
       │
       ▼
[Inference Worker: BRPOP task from 'inference_jobs_queue']
       │
       ├──> Status: "PROCESSING" in Redis
       │
       ├──> Check Model Cache (Load from MLflow if not cached locally)
       │
       ├──> Run Tokenizer & Model Forward Pass (GPU/CPU)
       │
       ├──> Format Output: Entities, Tokens, Confidence Scores
       │
       ▼
[Inference Worker: Save Result in Redis Key `predict_job:<job_id>` (TTL: 3600s)]
       │
       ▼ Status: "COMPLETED"
       │
[Client: GET /predict/<job_id>]
       │
       ▼
[FastAPI returns {"status": "COMPLETED", "result": {...}}]
```
