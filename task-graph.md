# Monorepo Project Task Graph & Execution Plan

> [!NOTE]
> Living task graph and execution plan for the AI Ecosystem Monorepo. All tasks follow the strict 5-part schema: Task ID, File, Logic/Target, Why, and Verification.

## Phase 1: Monorepo Foundation & Workspace Setup
- [x] **Task 1.1**: Monorepo Directory Tree Structure Setup
    - *File*: [apps/](file:///c:/eco/friday/apps/), [libs/](file:///c:/eco/friday/libs/), [workers/](file:///c:/eco/friday/workers/), [scripts/](file:///c:/eco/friday/scripts/), [docs/](file:///c:/eco/friday/docs/)
    - *Logic/Target*: Create all primary monorepo directories: `apps/time_series`, `apps/non_time_series`, `libs/minio_client`, `libs/redis_client`, `libs/arq_client`, `libs/label_studio`, `workers/timeseries_worker`, `workers/nontimeseries_worker`, `scripts`, `docs`.
    - *Why*: Establish a modular monorepo structure separating application APIs, shared clients, async background workers, tools, and documentation.
    - *Verification*: **[AUTONOMOUS]** Check path existence for all 10 subdirectories.
- [x] **Task 1.2**: Module-Level Documentation Initializer
    - *File*: [apps/time_series/README.md](file:///c:/eco/friday/apps/time_series/README.md), [apps/non_time_series/README.md](file:///c:/eco/friday/apps/non_time_series/README.md), [libs/minio_client/README.md](file:///c:/eco/friday/libs/minio_client/README.md), [libs/redis_client/README.md](file:///c:/eco/friday/libs/redis_client/README.md), [libs/arq_client/README.md](file:///c:/eco/friday/libs/arq_client/README.md), [libs/label_studio/README.md](file:///c:/eco/friday/libs/label_studio/README.md), [workers/timeseries_worker/README.md](file:///c:/eco/friday/workers/timeseries_worker/README.md), [workers/nontimeseries_worker/README.md](file:///c:/eco/friday/workers/nontimeseries_worker/README.md), [scripts/README.md](file:///c:/eco/friday/scripts/README.md), [README.md](file:///c:/eco/friday/README.md)
    - *Logic/Target*: Create comprehensive README.md files for every app, library client, worker, script, and root directory detailing responsibilities, architecture, and developer jobs.
    - *Why*: Provide clear technical guidelines and documentation standards across all monorepo modules.
    - *Verification*: **[AUTONOMOUS]** Inspect existence and non-empty status of all generated README.md files.
- [x] **Task 1.3**: Complete Task Graph Blueprint Update
    - *File*: [task-graph.md](file:///c:/eco/friday/task-graph.md)
    - *Logic/Target*: Write detailed 7-phase implementation roadmap adhering strictly to the 5-part schema (Task ID, File, Logic/Target, Why, Verification).
    - *Why*: Serve as the master living plan and tracking document for all developer and sub-agent tasks.
    - *Verification*: **[AUTONOMOUS]** Validate structure and schema completeness of `task-graph.md`.

## Phase 2: Core Libraries Implementation (`libs/`)
- [ ] **Task 2.1**: Implement MinIO Object Storage Client
    - *File*: [libs/minio_client/client.py](file:///c:/eco/friday/libs/minio_client/client.py)
    - *Logic/Target*: Build asynchronous MinIO wrapper supporting bucket creation, object uploads (binary streams, images, CSVs), presigned URLs, and download streams.
    - *Why*: Centralize S3-compatible object storage access for raw IoT data, images, and ML model checkpoints.
    - *Verification*: **[AUTONOMOUS]** Run unit tests connecting to local MinIO container to upload/download test payload.
- [ ] **Task 2.2**: Implement Redis Caching & State Client
    - *File*: [libs/redis_client/client.py](file:///c:/eco/friday/libs/redis_client/client.py)
    - *Logic/Target*: Develop Redis client helper with automatic connection pooling, key prefix management, time-series cache setters/getters, and JSON serialization.
    - *Why*: Provide high-performance caching for frequent telemetry queries, prediction outputs, and worker job statuses.
    - *Verification*: **[AUTONOMOUS]** Run integration test verifying set/get operations with expiration logic against Redis.
- [ ] **Task 2.3**: Implement ARQ Queue Task Dispatcher Client
    - *File*: [libs/arq_client/dispatcher.py](file:///c:/eco/friday/libs/arq_client/dispatcher.py)
    - *Logic/Target*: Implement helper for background job enqueueing, task status tracking, and worker connection configuration.
    - *Why*: Decouple API response cycles from heavy ML worker computations (Prophet, LSTM, ResNet-18).
    - *Verification*: **[AUTONOMOUS]** Execute test enqueue script and verify task entry in Redis ARQ queue.
- [ ] **Task 2.4**: Implement Label Studio Integration SDK Wrapper
    - *File*: [libs/label_studio/client.py](file:///c:/eco/friday/libs/label_studio/client.py)
    - *Logic/Target*: Implement Label Studio client for project creation, task import (X-ray images, sensor metrics), and annotation export parsing.
    - *Why*: Automate data annotation workflows for human-in-the-loop ML model training and validation.
    - *Verification*: **[AUTONOMOUS]** Test API authentication, list active projects, and create dummy annotation task.

## Phase 3: Asynchronous Background Workers (`workers/`)
- [ ] **Task 3.1**: Implement Time-Series ML Worker (Prophet / LSTM)
    - *File*: [workers/timeseries_worker/worker.py](file:///c:/eco/friday/workers/timeseries_worker/worker.py)
    - *Logic/Target*: Construct ARQ background tasks for forecasting IoT telemetry data using Facebook Prophet and LSTM neural network models. Write inference output back to MinIO/PostgreSQL.
    - *Why*: Process compute-heavy time-series forecasting asynchronously without blocking FastAPI HTTP endpoints.
    - *Verification*: **[AUTONOMOUS]** Enqueue sample time-series dataset job and verify predicted values are saved to storage.
- [ ] **Task 3.2**: Implement Non-Time-Series Computer Vision Worker (ResNet-18)
    - *File*: [workers/nontimeseries_worker/worker.py](file:///c:/eco/friday/workers/nontimeseries_worker/worker.py)
    - *Logic/Target*: Construct ARQ worker processing image/X-ray classification using PyTorch ResNet-18 model. Fetch image from MinIO, run inference, and return labels.
    - *Why*: Provide scalable async image processing and classification pipelines for non-time-series domain.
    - *Verification*: **[AUTONOMOUS]** Enqueue test image inference task and confirm classification output labels and confidence scores.

## Phase 4: FastAPI Applications (`apps/`)
- [ ] **Task 4.1**: Implement Time-Series FastAPI Web Service
    - *File*: [apps/time_series/main.py](file:///c:/eco/friday/apps/time_series/main.py)
    - *Logic/Target*: Build FastAPI application exposing endpoints for sensor data ingestion, forecasting job submission, and historical telemetry retrieval.
    - *Why*: Serve as the primary API interface for IoT device integration and time-series analytics dashboards.
    - *Verification*: **[AUTONOMOUS]** Run FastAPI service with uvicorn and execute HTTP requests to `/health` and `/api/v1/forecast`.
- [ ] **Task 4.2**: Implement Non-Time-Series FastAPI Web Service
    - *File*: [apps/non_time_series/main.py](file:///c:/eco/friday/apps/non_time_series/main.py)
    - *Logic/Target*: Build FastAPI application for uploading medical X-ray / general image datasets, dispatching classification worker tasks, and fetching Label Studio annotations.
    - *Why*: Serve as the dedicated API service for image analysis workflows.
    - *Verification*: **[AUTONOMOUS]** Post multipart image upload request to `/api/v1/classify` and verify response task_id.

## Phase 5: Automation Tools & Utility Scripts (`scripts/`)
- [x] **Task 5.1**: Implement OpenAPI to Excel Generator Script
    - *File*: [scripts/openapi_to_excel.py](file:///c:/eco/friday/scripts/openapi_to_excel.py)
    - *Logic/Target*: Create CLI script utilizing openpyxl / pandas to fetch OpenAPI schema (`openapi.json`) from FastAPI applications and export structured Excel spreadsheet documentation (Endpoints, Method, Parameters, Requests, Responses).
    - *Why*: Automate developer and client documentation generation directly from API source code.
    - *Verification*: **[AUTONOMOUS]** Execute `python scripts/openapi_to_excel.py` against running app and verify `.xlsx` report output.
- [ ] **Task 5.2**: Implement Integration Seed & Utility Scripts
    - *File*: [scripts/seed_data.py](file:///c:/eco/friday/scripts/seed_data.py)
    - *Logic/Target*: Develop script to seed initial MinIO buckets, PostgreSQL database tables, and sample dataset files.
    - *Why*: Facilitate quick environment initialization and automated testing setup.
    - *Verification*: **[AUTONOMOUS]** Run seed script and verify created buckets and initial DB rows.

## Phase 6: Infrastructure Orchestration & Environment Configuration
- [x] **Task 6.1**: Update Docker Compose & Multi-Container Setup
    - *File*: [compose.yml](file:///c:/eco/friday/compose.yml)
    - *Logic/Target*: Configure containers for PostgreSQL, Redis, MinIO, Label Studio, Time-Series Worker, Non-Time-Series Worker, and FastAPI apps with healthchecks and network bridges.
    - *Why*: Orchestrate the complete AI ecosystem infrastructure in a single unified Docker Compose environment.
    - *Verification*: **[AUTONOMOUS]** Run `docker compose up -d` and verify all service containers are healthy.
- [ ] **Task 6.2**: Standardize Environment Variable Settings
    - *File*: [.env.example](file:///c:/eco/friday/.env.example), [backend/core/config.py](file:///c:/eco/friday/backend/core/config.py)
    - *Logic/Target*: Consolidate all configuration environment keys across apps, workers, and clients with Pydantic Settings validation.
    - *Why*: Ensure secure, unified environment handling across development, testing, and production.
    - *Verification*: **[AUTONOMOUS]** Test configuration loading across different sub-modules.

## Phase 7: End-to-End Integration, Verification & System Documentation
- [ ] **Task 7.1**: End-to-End Integration Testing
    - *File*: [docs/integration_test.py](file:///c:/eco/friday/docs/integration_test.py)
    - *Logic/Target*: Create integration test suite verifying full flow: API upload -> MinIO -> Redis/ARQ Worker -> ML inference -> Label Studio / Database storage.
    - *Why*: Ensure system reliability and inter-module communication integrity.
    - *Verification*: **[AUTONOMOUS]** Execute integration test suite and verify 100% pass rate.
- [ ] **Task 7.2**: Final System Documentation & Architecture Update
    - *File*: [architecture.md](file:///c:/eco/friday/architecture.md), [README.md](file:///c:/eco/friday/README.md), [docs/api_spec.xlsx](file:///c:/eco/friday/docs/api_spec.xlsx)
    - *Logic/Target*: Update full monorepo architecture diagram, directory layout docs, and generate API Excel documentation.
    - *Why*: Maintain accurate, production-grade documentation for the entire AI ecosystem monorepo.
    - *Verification*: **[AUTONOMOUS]** Review documentation completeness and file links.
