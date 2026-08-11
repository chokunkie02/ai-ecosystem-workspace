# Time-Series ML Worker (`workers/timeseries_worker`)

> [!NOTE]
> บริการ Worker สำหรับประมวลผลโมเดล Machine Learning อนุกรมเวลา (Prophet / LSTM) แบบ Asynchronous

## บทบาทและหน้าที่ (Responsibilities)
`workers/timeseries_worker` รันประมวลผลเป็นกระบวนการหลังบ้าน (Background Process) ผ่านระบบ **ARQ Worker** โดยดึง Job การพยากรณ์ข้อมูลเชิงเวลาจาก Redis Queue เพื่อทำการประมวลผลโมเดลวิเคราะห์แนวโน้มและตรวจจับสิ่งผิดปกติ (Anomaly Detection):

1. **Prophet Forecasting Model**: ประมวลผลข้อมูลอนุกรมเวลาระดับมหภาคหรือระดับรายวัน/รายชั่วโมง ด้วยโมเดล **Facebook Prophet** เพื่อทำนายค่าในอนาคต
2. **LSTM Neural Network Model**: ประมวลผลข้อมูลอนุกรมเวลาที่มีความซับซ้อนและมีความสัมพันธ์เชิงเวลาสูงด้วยโมเดล **Deep Learning LSTM**
3. **Data Preprocessing & Feature Engineering**: รับข้อมูลเซนเซอร์ทำ Normalization และ Resampling ก่อนส่งเข้าโมเดล
4. **Result Persistence**: จัดเก็บผลลัพธ์การทำนายลงใน MinIO Object Storage (`timeseries-predictions`) และอัปเดตแคชใน Redis

## Environment Variables

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `REDIS_HOST` | `localhost` | Host ของ Redis server ที่ ARQ Worker เชื่อมต่อ |
| `REDIS_PORT` | `6379` | Port ของ Redis server ที่ ARQ Worker เชื่อมต่อ |
| `REDIS_PASSWORD` | `None` | รหัสผ่าน Redis server (ถ้ามี) |
| `MINIO_ENDPOINT` | `localhost:9000` | Endpoint สำหรับ MinIO Object Storage |
| `MINIO_ACCESS_KEY` | `minioadmin` | Access Key สำหรับ MinIO |
| `MINIO_SECRET_KEY` | `minioadmin` | Secret Key สำหรับ MinIO |
| `MINIO_SECURE` | `false` | กำหนดการใช้งาน HTTPS (`true` / `false`) |

## โครงสร้างไดเรกทอรี
```text
workers/timeseries_worker/
├── README.md               # เอกสารอธิบายการทำงานของ Time-series Worker
├── __init__.py             # Module Initializer
└── worker.py               # ARQ Worker Entry Point & Registered Tasks
```

## วิธีการรัน ARQ Worker

```bash
# 1. การรันผ่าน ARQ CLI โดยตรง
arq workers.timeseries_worker.worker.WorkerSettings

# 2. การรันผ่าน Docker Compose
docker compose up -d timeseries_worker
```

## ตัวอย่างการเรียกใช้งานผ่าน TaskDispatcher (Usage Example)

```python
import asyncio
from libs.arq_client.dispatcher import TaskDispatcher

async def main():
    dispatcher = TaskDispatcher()

    # 1. ส่งงานพยากรณ์อนุกรมเวลา (Time-Series Forecasting Task)
    sensor_data = [
        {"timestamp": "2026-08-12T00:00:00Z", "value": 102.5},
        {"timestamp": "2026-08-12T00:05:00Z", "value": 105.0},
        {"timestamp": "2026-08-12T00:10:00Z", "value": 103.8},
    ]

    job_info = await dispatcher.enqueue_job(
        "process_timeseries_forecast",
        sensor_id="sensor_temp_01",
        data_points=sensor_data,
        horizon=12
    )
    print(f"Forecast Job Enqueued: {job_info}")

    # 2. ส่งงานเทรนโมเดลอนุกรมเวลา (Model Training Task)
    train_job = await dispatcher.enqueue_job(
        "train_timeseries_model",
        dataset_id="dataset_iot_2026",
        model_type="prophet",
        params={"epochs": 50}
    )
    print(f"Training Job Enqueued: {train_job}")

    await dispatcher.close()

if __name__ == "__main__":
    asyncio.run(main())
```
