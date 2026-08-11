# Monorepo Utility Scripts (`scripts/`)

> [!NOTE]
> สคริปต์เครื่องมือช่วยอำนวยความสะดวกในการพัฒนา การสร้างเอกสารอัตโนมัติ และการบริหารจัดการระบบ AI Ecosystem

## สคริปต์หลักในไดเรกทอรี (Key Scripts)

### 1. `scripts/openapi_to_excel.py`
สคริปต์อัตโนมัติสำหรับดึงข้อกำหนด OpenAPI (Swagger Specification `openapi.json`) จากบริการ FastAPI (`apps/time_series` และ `apps/non_time_series`) แล้วทำการแปลงข้อมูลโครงสร้าง API ทั้งหมดให้อยู่ในรูปแบบ **Excel Documentation (.xlsx)** อย่างเป็นระเบียบ

#### คุณสมบัติหลัก (Features):
- ดึง Schema โดยตรงจาก FastAPI Running Server หรือไฟล์ `openapi.json`
- สร้างแผ่นงาน Excel ที่แยกหมวดหมู่ API Endpoints, HTTP Methods (GET, POST, PUT, DELETE), Summary, Description, Path Parameters, Query Parameters, Request Body Schemas และ Response Status Codes
- จัดรูปแบบตาราง สีกรอบ และความกว้างคอลัมน์โดยอัตโนมัติด้วย **openpyxl** / **pandas** เพื่อให้นำเสนอเอกสารได้อย่างมืออาชีพ

#### วิธีการรันใช้งาน (Usage):
```bash
# สั่งรันสคริปต์ดึง OpenAPI Schema มาแปลงเป็น Excel Documentation
uv run python scripts/openapi_to_excel.py --url http://localhost:8000/openapi.json --output docs/api_spec_timeseries.xlsx
uv run python scripts/openapi_to_excel.py --url http://localhost:8001/openapi.json --output docs/api_spec_nontimeseries.xlsx
```

---

### 2. `scripts/seed_data.py`
สคริปต์สำหรับเตรียมข้อมูลทดสอบเริ่มต้น (Data Seeding) เช่น การสร้าง Buckets ใน MinIO, การเตรียมตารางใน PostgreSQL และการอัปโหลดรูปภาพทดสอบ/ไฟล์เซนเซอร์เริ่มต้น

#### วิธีการรันใช้งาน (Usage):
```bash
uv run python scripts/seed_data.py
```

## โครงสร้างไดเรกทอรี
```text
scripts/
├── README.md               # เอกสารอธิบายเครื่องมือและสคริปต์ใน scripts/
├── openapi_to_excel.py     # สคริปต์แปลง OpenAPI JSON เป็น Excel Spreadsheets
└── seed_data.py            # สคริปต์เตรียมข้อมูลเริ่มต้นสำหรับ MinIO, Postgres & Redis
```
