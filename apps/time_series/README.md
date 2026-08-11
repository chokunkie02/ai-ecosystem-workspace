# Time-Series Application Service (`apps/time_series`)

> [!NOTE]
> แอปพลิเคชันฝั่งหลังบ้านสำหรับรับ ส่ง และประมวลผลข้อมูลอนุกรมเวลา (Time-Series Data) จากอุปกรณ์ IoT และเซนเซอร์

## บทบาทและหน้าที่ (Responsibilities)
บริการ `apps/time_series` ถูกออกแบบมาเพื่อทำหน้าที่เป็น RESTful API Web Service ด้วย **FastAPI** เพื่อจัดการกับข้อมูลเชิงเวลา (Time-Series Telemetry & IoT Sensor Data) โดยมีหน้าที่หลักดังนี้:

1. **Ingestion & Data Reception**: รับข้อมูล Telemetry/Sensor Data (เช่น อุณหภูมิ, ความชื้น, ความดัน, แรงดันไฟฟ้า) ผ่าน REST HTTP Endpoints
2. **Data Storage Orchestration**: จัดเก็บข้อมูลดิบลงใน **MinIO Object Storage** และบันทึก Metadata / Metrics ลงใน **PostgreSQL**
3. **Async Forecasting Dispatch**: รับคำร้องขอทำอนุกรมเวลาพยากรณ์ (Forecasting Request) และส่งงานผ่าน `libs/arq_client` ไปยัง `workers/timeseries_worker`
4. **Caching & Querying**: ดึงผลการพยากรณ์และแคชข้อมูลอนุกรมเวลาที่ใช้งานบ่อยผ่าน `libs/redis_client` เพื่อเพิ่มความเร็วในการตอบสนอง

## โครงสร้างไดเรกทอรี
```text
apps/time_series/
├── README.md               # เอกสารอธิบายการทำงานของ Time-Series App
├── main.py                 # FastAPI Application entry point
├── api/                    # API Endpoints (v1)
│   ├── routes_telemetry.py # Endpoints สำหรับรับและค้นหาข้อมูลเซนเซอร์
│   └── routes_forecast.py  # Endpoints สำหรับสั่งการรัน Prophet/LSTM Forecasting
├── core/                   # Service Configuration & Dependencies
└── models/                 # Pydantic Schemas สำหรับรับ-ส่งข้อมูล
```

## Developer Job & Task Workflow
- **Developer Job**: พัฒนา FastAPI Endpoints สำหรับการรับ-ส่งข้อมูลเซนเซอร์, Validate Pydantic Schema, และสร้าง Integration ร่วมกับ `libs/minio_client`, `libs/redis_client`, และ `libs/arq_client`
- **การเชื่อมต่อ**:
  - `libs/minio_client` -> บันทึกไฟล์ CSV/Parquet ของเซนเซอร์ลงใน Bucket `timeseries-raw`
  - `libs/redis_client` -> ทำ Caching ผลการค้นหาข้อมูลเซนเซอร์ย้อนหลัง
  - `libs/arq_client` -> สั่ง Enqueue background job พยากรณ์ค่าอนาคต
