# AI Ecosystem Workspace

ยินดีต้อนรับสู่โครงการศึกษาและพัฒนาระบบ AI Ecosystem ในลักษณะครบวงจร (Full-Stack/Integration) 
โปรเจกต์นี้ได้รับการตั้งค่าเป็น **UV Workspace** เพื่อรองรับการจัดการ Dependencies และโมดูลย่อยต่าง ๆ อย่างรวดเร็วและเป็นระเบียบ

## โครงสร้างโปรเจกต์ (Project Structure)

- `backend/` — โมดูลหลักสำหรับโค้ดฝั่งระบบหลังบ้าน ประกอบด้วย:
  - การจัดการ Settings ด้วย `pydantic-settings`
  - การรัน Task แบบ Background (Queue) ด้วย Redis และ ARQ
  - การทำ CRUD กับฐานข้อมูล PostgreSQL ด้วย SQLAlchemy
  - การเรียกใช้ SDK ของ Label Studio
  - `sandbox/` — แหล่งรวบรวมสคริปต์ทดสอบ และสคริปต์จาก Assignment 1 (เช่น `db_test_assignment1.py` และ `report_generator_assignment1.py`)
- `overview/` — ไดอะแกรมอธิบายภาพรวมสถาปัตยกรรมระบบ (`overview.drawio`, `overview.png`)
- `storage/` — โฟลเดอร์เก็บข้อมูลประเภทต่าง ๆ:
  - `artifacts/` — แหล่งรวมผลลัพธ์การทดสอบและเอกสารรายงานส่งงานต่างๆ ของ Assignment 1 และ Assignment 3
  - `data/` — ข้อมูลสำหรับการจัดเก็บหรือทดสอบระบบ
  - `log/` — ล็อกไฟล์จาก Docker และ Server
- `utils/` — ฟังก์ชันและยูทิลิตี้เสริมต่าง ๆ (เช่น helper สำหรับจัดการไดเรกทอรีและ logging)
- `compose.yml` — ไฟล์ Docker Compose สำหรับสร้างคอนเทนเนอร์ Redis, PostgreSQL และ Label Studio สำหรับโปรเจกต์

## วิธีการใช้งาน (Getting Started)

### ความต้องการของระบบ (Prerequisites)
- [Python >= 3.12](https://www.python.org/)
- [UV](https://github.com/astral-sh/uv) (เครื่องมือจัดการโปรเจกต์ Python)
- Docker & Docker Compose

### การติดตั้งและใช้งาน

1. **เตรียมฐานข้อมูลและบริการต่างๆ (Docker Setup):**
   รัน Docker Compose เพื่อเปิดใช้งานระบบ Redis, PostgreSQL และ Label Studio:
   ```bash
   docker compose up -d
   ```

2. **ติดตั้ง Dependencies:**
   ทำผ่านระบบ Workspace ที่รูทโปรเจกต์:
   ```bash
   uv sync
   ```

3. **การสั่งรันและทดสอบระบบย่อยฝั่ง Backend:**
   กรุณาดูรายละเอียดการเรียกใช้งานสคริปต์ทดสอบระบบต่าง ๆ (เช่น PostgreSQL CRUD, ARQ Worker, Label Studio SDK) ได้ใน [backend/README.md](file:///c:/eco/friday/backend/README.md)
