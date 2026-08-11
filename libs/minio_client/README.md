# MinIO Object Storage Client Library (`libs/minio_client`)

> [!NOTE]
> ไลบรารีส่วนกลางสำหรับเชื่อมต่อและจัดการ MinIO Object Storage (S3-Compatible Object Storage)

## บทบาทและหน้าที่ (Responsibilities)
`libs/minio_client` ทำหน้าที่เป็น SDK Client กลาง (Shared Module) ให้กับแอปพลิเคชันและ Worker ภายใน Monorepo เพื่อจัดการ Object Storage ในการเก็บไฟล์ไบนารีขนาดใหญ่ เช่น ไฟล์ภาพถ่ายรังสี X-Ray, ชุดข้อมูลอนุกรมเวลา CSV/Parquet และไฟล์โมเดล ML (Checkpoints)

## Environment Variables

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `MINIO_ENDPOINT` | `localhost:9000` | Host และ Port สำหรับเชื่อมต่อ MinIO server |
| `MINIO_ACCESS_KEY` | `minioadmin` | Access Key (User ID) สำหรับ MinIO |
| `MINIO_SECRET_KEY` | `minioadmin` | Secret Key (Password) สำหรับ MinIO |
| `MINIO_SECURE` | `false` | กำหนดการใช้งาน HTTPS (`true` / `false`) |

## Developer Job (ภาระงานของนักพัฒนา)
1. **Bucket Management**: ตรวจสอบและสร้าง Buckets อัตโนมัติด้วย `ensure_bucket_exists`
2. **Object Upload & Stream**: อัปโหลดไฟล์ (Path, Bytes, Stream) ด้วย `upload_file`
3. **Object Download & Presigned URL**: ดาวน์โหลดไฟล์ด้วย `download_file` และสร้าง URL ชั่วคราวด้วย `get_presigned_url`
4. **List & Delete Objects**: แสดงรายชื่อวัตถุด้วย `list_objects` และลบวัตถุด้วย `delete_object`

## โครงสร้างไดเรกทอรี
```text
libs/minio_client/
├── README.md               # เอกสารอธิบายการใช้งาน MinIO Client
├── __init__.py             # Module Initializer
└── client.py               # MinIOManager implementation
```

## วิธีการรัน (Docker & Tests)

```bash
# สตาร์ท MinIO Container
docker compose up -d minio

# การรัน Unit / Integration Tests
pytest libs/minio_client/tests/
```

## ตัวอย่างการใช้งาน (Usage Example)

```python
from libs.minio_client.client import MinIOManager

# 1. Initialize MinIO Manager (โหลดค่าจาก Env Vars โดยอัตโนมัติ)
minio_mgr = MinIOManager()

# 2. ตรวจสอบหรือสร้าง Bucket
minio_mgr.ensure_bucket_exists("nontimeseries-images")

# 3. อัปโหลดไฟล์ (รองรับ File Path, Bytes, หรือ Stream)
object_key = minio_mgr.upload_file(
    bucket_name="nontimeseries-images",
    object_name="xray_001.png",
    file_data=b"...binary_data...",
    content_type="image/png"
)
print(f"Uploaded: {object_key}")

# 4. สร้าง Presigned URL สำหรับดาวน์โหลดไฟล์
url = minio_mgr.get_presigned_url(
    bucket_name="nontimeseries-images",
    object_name="xray_001.png",
    expires_seconds=3600
)
print(f"Presigned URL: {url}")

# 5. ดาวน์โหลดไฟล์
data = minio_mgr.download_file(
    bucket_name="nontimeseries-images",
    object_name="xray_001.png"
)
```
