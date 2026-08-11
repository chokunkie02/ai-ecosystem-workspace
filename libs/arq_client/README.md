# Arq Task Queue Dispatcher Library (`libs/arq_client`)

> [!NOTE]
> ไลบรารีส่วนกลางสำหรับส่งและบริหารจัดการคิวงงาน Asynchronous Background Task ด้วย ARQ และ Redis

## บทบาทและหน้าที่ (Responsibilities)
`libs/arq_client` ทำหน้าที่เป็น Job Dispatcher Client ให้กับบริการ FastAPI (`apps/time_series` และ `apps/non_time_series`) เพื่อส่งงานการประมวลผลโมเดล ML/DL หรือการประมวลผลไฟล์ขนาดใหญ่เข้าไปยังคิวงงาน (Redis-backed Queue) โดยไม่ต้องรอให้การประมวลผลเสร็จสิ้นในระหว่างรอบ HTTP Request/Response

## Environment Variables

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `REDIS_HOST` | `localhost` | Host สำหรับเชื่อมต่อ Redis server ของ ARQ |
| `REDIS_PORT` | `6379` | Port สำหรับเชื่อมต่อ Redis server ของ ARQ |

## Developer Job (ภาระงานของนักพัฒนา)
1. **ARQ Pool Connection**: จัดการการเชื่อมต่อ ARQ Redis Pool ด้วย `get_pool`
2. **Job Enqueue Dispatching**: ส่ง Background Job เข้าคิวด้วย `enqueue_job` พร้อมพารามิเตอร์และ Custom Job ID
3. **Job Status & Result Tracking**: ค้นหาและดึงสถานะงาน/ผลลัพธ์ด้วย `get_job_status`
4. **Resource Cleanup**: ปิดการเชื่อมต่อ Connection Pool อย่างถูกต้องด้วย `close`

## โครงสร้างไดเรกทอรี
```text
libs/arq_client/
├── README.md               # เอกสารอธิบายการใช้งาน ARQ Task Dispatcher
├── __init__.py             # Module Initializer
└── dispatcher.py           # TaskDispatcher implementation
```

## วิธีการรัน (Docker & Tests)

```bash
# สตาร์ท Redis Container
docker compose up -d redis

# การรัน Unit / Integration Tests
pytest libs/arq_client/tests/
```

## ตัวอย่างการใช้งาน (Usage Example)

```python
import asyncio
from libs.arq_client.dispatcher import TaskDispatcher

async def main():
    # 1. Initialize Task Dispatcher
    dispatcher = TaskDispatcher()

    # 2. ส่ง Background Task เข้าคิว ARQ Queue
    job_info = await dispatcher.enqueue_job(
        "process_image_inference",
        image_id="img_001",
        image_bucket="general-images",
        object_key="sample.jpg"
    )
    print(f"Job Enqueued: {job_info}")

    # 3. ตรวจสอบสถานะงานและผลลัพธ์ตาม Job ID
    if job_info:
        job_id = job_info["job_id"]
        status = await dispatcher.get_job_status(job_id)
        print(f"Job Status: {status}")

    # 4. ปิดการเชื่อมต่อ Pool
    await dispatcher.close()

if __name__ == "__main__":
    asyncio.run(main())
```
