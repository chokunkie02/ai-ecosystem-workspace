# AI Ecosystem Workspace

โปรเจกต์นี้เป็นการฝึกวางระบบ AI ecosystem แบบครบวงจร ครอบคลุมตั้งแต่การตั้งค่าเครื่องมือพื้นฐาน (Git, Docker, WSL, GPU) ไปจนถึงการรันบริการ Redis ผ่าน Docker Compose

## โครงสร้างโปรเจกต์

- `diagrams/` — ไดอะแกรมภาพรวมระบบ (system overview)
- `compose.yml` — ไฟล์ตั้งค่า Docker Compose สำหรับรัน Redis server

## System Overview

ระบบประกอบด้วยส่วนหลักๆ ดังนี้:

- **End user / Admin** เข้าถึงระบบผ่าน Inference Channel และ Management Channel
- **Central API Server** เป็นจุดกลางเชื่อมต่อระหว่าง channel ต่างๆ กับฐานข้อมูลและ worker
- **Redis Server** ใช้เป็น queue/cache สำหรับงานที่ต้องประมวลผล
- **PostgreSQL** เก็บข้อมูลหลักของระบบ
- **Job worker / Training worker** ทำหน้าที่ประมวลผล inference และ training โดยดึงโมเดลและข้อมูลจาก Annotated Database

รายละเอียดไดอะแกรมดูได้ที่ [diagrams/overview.drawio](diagrams/overview.drawio)

## การใช้งาน Docker

### ตรวจสอบ GPU
```
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

### รัน Redis server
```
docker compose up -d
```

ตรวจสอบว่า Redis ทำงานปกติ:
```
docker compose exec redis redis-cli ping
docker ps --all
```
