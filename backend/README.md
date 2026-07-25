# Backend Service - AI Ecosystem

โฟลเดอร์นี้รวบรวมระบบย่อยและเครื่องมือฝั่งระบบหลังบ้านทั้งหมด โดยขับเคลื่อนด้วยโมดูลย่อยและสคริปต์ทดสอบต่าง ๆ

## โครงสร้างระบบ (System Structure)

- `core/config.py` — ตัวจัดการอ่านการตั้งค่าของโปรเจกต์ผ่าน Pydantic BaseSettings จากไฟล์ `.env`
- `sandbox/test_settings.py` — สคริปต์สำหรับพิมพ์ตรวจสอบว่า Pydantic Settings สามารถดึงค่าได้ถูกต้อง
- `worker_settings.py` — คลาสกำหนดค่าสำหรับการทำ Background Job Worker ด้วยไลบรารี ARQ
- `enqueue.py` — สคริปต์สำหรับทดสอบการผลัก Job เข้าสู่ Redis Queue
- `postgres_test.py` — สคริปต์ทำรายการ CRUD บน PostgreSQL เพื่อตรวจสอบสิทธิ์และการเชื่อมต่อฐานข้อมูล
- `label_studio_test.py` — สคริปต์ทดสอบการเชื่อมต่อและเรียกใช้ API ของ Label Studio ผ่าน Python SDK
- `generate_report.py` — สคริปต์สำหรับรวบรวมโค้ดและ Log เพื่อนำไปสร้างไฟล์ส่งงาน Word Report (.docx)

## การรันและทดสอบระบบหลังบ้าน (Running & Testing)

ก่อนการเริ่มรัน ให้แน่ใจว่าได้จำลองบริการ PostgreSQL, Redis และ Label Studio เรียบร้อยแล้ว (สามารถเริ่มได้ผ่าน Docker Compose ในโฟลเดอร์ `work1/`)

1. **ตรวจสอบความถูกต้องของการตั้งค่า (Settings):**
   ```bash
   uv run python -m sandbox.test_settings
   ```

2. **ทดสอบระบบคิว ARQ Worker:**
   - **รัน Worker (รอรับคำสั่ง):**
     ```bash
     uv run arq worker_settings.WorkerSettings
     ```
   - **ทำการผลัก Job เข้าคิว (เปิดอีกหน้าต่าง Terminal):**
     ```bash
     uv run python enqueue.py
     ```

3. **ทดสอบการเชื่อมต่อ PostgreSQL Database (CRUD):**
   ```bash
   uv run python postgres_test.py
   ```

4. **ทดสอบดึงข้อมูลโปรเจกต์จาก Label Studio SDK:**
   ```bash
   uv run python label_studio_test.py
   ```
