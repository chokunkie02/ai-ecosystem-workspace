# Non-Time-Series ML Worker (`workers/nontimeseries_worker`)

> [!NOTE]
> บริการ Worker สำหรับประมวลผลโมเดล Deep Learning Computer Vision (ResNet-18) แบบ Asynchronous

## บทบาทและหน้าที่ (Responsibilities)
`workers/nontimeseries_worker` ทำหน้าที่เป็น Background Processing Engine สำหรับงานด้าน Computer Vision โดยเน้นการประมวลผลภาพถ่ายทั่วไปและภาพเอ็กซเรย์ทางการแพทย์ (Medical X-Ray Classification) ด้วยสถาปัตยกรรม **ResNet-18**:

1. **Image Inference Engine**: โหลดโมเดล **ResNet-18 (PyTorch)** เพื่อทำ Image Classification / Detection
2. **MinIO Image Fetching**: ดึงไฟล์ภาพไบนารีจาก MinIO Object Storage Bucket `general-images` หรือ `nontimeseries-images` มาทำ Preprocessing
3. **Batch Processing**: รองรับการทำ Batch Inference สำหรับประมวลผลภาพจำนวนมากผ่าน `process_batch_image_inference`
4. **Prediction Result & Confidence Scoring**: คำนวณค่า Probability/Confidence Score บันทึกผลลัพธ์ลง MinIO (`vision-results`) และอัปเดตแคชใน Redis

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
workers/nontimeseries_worker/
├── README.md               # เอกสารอธิบายการทำงานของ Non-Time-Series Worker
├── __init__.py             # Module Initializer
└── worker.py               # ARQ Worker Entry Point & Computer Vision Tasks
```

## วิธีการรัน ARQ Worker

```bash
# 1. การรันผ่าน ARQ CLI โดยตรง
arq workers.nontimeseries_worker.worker.WorkerSettings

# 2. การรันผ่าน Docker Compose
docker compose up -d nontimeseries_worker
```

## ตัวอย่างการเรียกใช้งานผ่าน TaskDispatcher (Usage Example)

```python
import asyncio
from libs.arq_client.dispatcher import TaskDispatcher

async def main():
    dispatcher = TaskDispatcher()

    # 1. ส่งงานประมวลผลภาพเดี่ยว (Single Image Inference Task)
    job_info = await dispatcher.enqueue_job(
        "process_image_inference",
        image_id="img_xray_001",
        image_bucket="general-images",
        object_key="xray_sample.jpg"
    )
    print(f"Single Image Job Enqueued: {job_info}")

    # 2. ส่งงานประมวลผลภาพแบบกลุ่ม (Batch Image Inference Task)
    batch_job = await dispatcher.enqueue_job(
        "process_batch_image_inference",
        batch_id="batch_dataset_01",
        image_keys=["xray_01.jpg", "xray_02.jpg", "xray_03.jpg"]
    )
    print(f"Batch Image Job Enqueued: {batch_job}")

    await dispatcher.close()

if __name__ == "__main__":
    asyncio.run(main())
```
