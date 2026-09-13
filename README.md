# AI Ecosystem Monorepo Workspace

ยินดีต้อนรับสู่โปรเจกต์ **AI Ecosystem Monorepo Architecture** ที่รวมการบริหารจัดการระบบประมวลผลข้อมูลอนุกรมเวลา (Time-Series / IoT Sensors Data) และข้อมูลภาพถ่ายรังสีทางการแพทย์ (Non-Time-Series / Medical X-Ray Image Classification) พร้อมระบบ Data Annotation และ Background Task Processing ในสถาปัตยกรรมระดับองค์กร

---

## โครงสร้างสถาปัตยกรรม Monorepo (Monorepo Directory Structure)

```text
├── apps/                          # แอปพลิเคชันฝั่งหลังบ้าน (FastAPI Services)
│   ├── time_series/               # API Service สำหรับข้อมูลอนุกรมเวลา (IoT/Sensors Telemetry)
│   │   └── README.md
│   └── non_time_series/           # API Service สำหรับข้อมูลภาพถ่ายทางการแพทย์ (Image/X-Ray)
│       └── README.md
│
├── libs/                          # Shared Libraries & Client SDK Wrappers
│   ├── minio_client/              # MinIO Object Storage SDK Client (S3 Storage)
│   │   └── README.md
│   ├── redis_client/              # Redis Cache & Task Status Client
│   │   └── README.md
│   ├── arq_client/                # ARQ Async Task Queue Dispatcher Client
│   │   └── README.md
│   └── label_studio/              # Label Studio Data Annotation SDK Wrapper
│       └── README.md
│
├── workers/                       # Asynchronous ML/DL Background Workers
│   ├── timeseries_worker/         # Worker ประมวลผลโมเดล Prophet / PyTorch LSTM
│   │   └── README.md
│   └── nontimeseries_worker/      # Worker ประมวลผลโมเดล PyTorch ResNet-18 Image Classification
│       └── README.md
│
├── scripts/                       # Automation Utilities & Tools
│   ├── openapi_to_excel.py        # สคริปต์แปลง OpenAPI (Swagger JSON) เป็น Excel Documentation (.xlsx)
│   └── README.md
│
├── docs/                          # เอกสารสถาปัตยกรรม รายงานผล และ API Excel Spreadsheets
│
├── backend/                       # Legacy Backend Core & Configuration Workspace
├── overview/                      # ภาพรวมสถาปัตยกรรมระบบ (Draw.io / Diagram PNG)
├── storage/                       # แหล่งเก็บข้อมูลดิบและ Artifacts
├── compose.yml                    # Docker Compose Orchestration (PostgreSQL, Redis, MinIO, Label Studio)
├── task-graph.md                  # Master Plan & Living Execution Graph (7 Phases)
├── architecture.md                # เอกสารสถาปัตยกรรมระบบโดยละเอียด
└── pyproject.toml                 # UV Workspace Configuration
```

---

## ระบบย่อยและส่วนประกอบหลัก (Core System Components)

1. **FastAPI Applications (`apps/`)**:
   - `apps/time_series`: ให้บริการ REST API รับข้อมูลจากเซนเซอร์ IoT, ดึงกราฟประวัติย้อนหลัง และสั่งรัน Prophet/LSTM Forecasting
   - `apps/non_time_series`: ให้บริการ REST API สำหรับอัปโหลดภาพถ่าย X-Ray, สั่งรัน ResNet-18 Classification และซิงก์ข้อมูลกับ Label Studio

2. **Shared Libraries (`libs/`)**:
   - `libs/minio_client`: บริหารจัดการการอัปโหลด/ดาวน์โหลดไฟล์ไบนารีและรูปภาพขนาดใหญ่กับ MinIO S3 Object Storage
   - `libs/redis_client`: ระบบ Caching ความเร็วสูง เก็บแคชการพยากรณ์และสถานะการทำงานของ Worker
   - `libs/arq_client`: ส่งงานประมวลผลขนาดใหญ่เข้าคิว ARQ Redis แบบ Asynchronous
   - `libs/label_studio`: สื่อสารกับ Label Studio เพื่อนำภาพเข้ากระบวนการ Labeling และดึง Annotations ออกมา Retrain

3. **Background Workers (`workers/`)**:
   - `workers/timeseries_worker`: ประมวลผลทำนายแนวโน้มด้วย Facebook Prophet และ PyTorch LSTM
   - `workers/nontimeseries_worker`: ประมวลผลวิเคราะห์และจำแนกรูปภาพด้วย PyTorch ResNet-18

4. **Automation Tools (`scripts/`)**:
   - `scripts/openapi_to_excel.py`: แปลง OpenAPI Schema เป็นรายงาน Excel ให้อัตโนมัติ

---

## ขั้นตอนการติดตั้งและการใช้งาน (Getting Started)

### 1. ความต้องการของระบบ (Prerequisites)
- Python `>= 3.12`
- [UV Project & Package Manager](https://github.com/astral-sh/uv)
- Docker Desktop / Docker Compose

### 2. การเริ่มต้นระบบ (Environment Setup)
```bash
# 1. ติดตั้ง Dependencies และสร้าง Virtual Environment แบบ Workspace
uv sync

# 2. เปิดใช้งาน Container ทั้งหมด (FastAPI, Redis, MinIO, PostgreSQL, MLflow, Inference Worker, Trainer Worker)
docker compose up -d --build
```

---

## 🚀 MLOps Serving, Training Queue & Inference Worker

โปรเจกต์นี้ได้รับการขยายขีดความสามารถเข้าสู่สถาปัตยกรรม **MLOps Production Pipeline**:

1. **FastAPI Serving Gateway (Port 8000)**:
   - `POST /api/v1/predict`: ส่งข้อความทำนายผล Named Entity Recognition (NER) เข้าคิว Redis แบบ Asynchronous
   - `GET /api/v1/predict/{job_id}`: ดึงสถานะและผลลัพธ์การทำนาย
   - `POST /api/v1/train/enqueue`: จัดคิวงานเทรนโมเดลล่วงหน้า (Scheduled Training)
2. **Inference Worker**:
   - ดึงงานจาก Redis Queue (`inference_queue` / `inference_jobs_queue`)
   - โหลดโมเดลจาก MLflow Model Registry หรือ Fallback Base Model
   - คำนวณผลและจัดเก็บลง Redis (TTL 1 ชั่วโมง)
3. **MLflow Tracking & Registry (Port 5000)**:
   - บันทึก Experiment Metrics, Parameters และลงทะเบียน Model Registry
   - เชื่อมต่อ Backend Store บน **PostgreSQL (Port 5432)**
   - จัดเก็บ Model Artifacts บน **MinIO Object Storage (Port 9000/9001)**

### 3. ตรวจสอบสถานะการทำงาน
- **Swagger Documentation**: เข้าถึงได้ที่ `http://localhost:8000/docs`
- **MLflow Tracking UI**: เข้าถึงได้ที่ `http://localhost:5000`
- **MinIO S3 Console**: เข้าถึงได้ที่ `http://localhost:9001` (User: `minioadmin` / Pass: `minioadmin`)
- **Task Graph Roadmap**: สามารถดูแผนการดำเนินงานและสถานะงานได้ใน [task-graph.md](file:///c:/eco/friday/task-graph.md)
- **Architecture Spec**: ศึกษาผังและกระบวนการทำงานได้ใน [architecture.md](file:///c:/eco/friday/architecture.md)
- **Architecture Diagram**: แผนผัง Draw.io อยู่ที่ [architecture_diagram.drawio](file:///c:/eco/friday/architecture_diagram.drawio)
