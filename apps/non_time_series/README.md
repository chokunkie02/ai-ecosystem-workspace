# Non-Time-Series Application Service (`apps/non_time_series`)

> [!NOTE]
> แอปพลิเคชันฝั่งหลังบ้านสำหรับประมวลผลข้อมูลภาพทางการแพทย์ (Medical X-Ray) และรูปภาพทั่วไป (Non-Time-Series Data)

## บทบาทและหน้าที่ (Responsibilities)
บริการ `apps/non_time_series` พัฒนาด้วย **FastAPI** เพื่อให้บริการ REST API สำหรับการจัดการไฟล์รูปภาพ, ภาพเอ็กซเรย์ทางการแพทย์ (Medical X-Ray), งาน Computer Vision และการทำ Image Classification:

1. **Image File Ingestion**: รับไฟล์รูปภาพ/ภาพถ่ายรังสีทางการแพทย์ผ่าน Multipart Form-Data Upload
2. **Binary Storage Management**: ส่งไฟล์รูปภาพความละเอียดสูงไปจัดเก็บบน **MinIO Object Storage** ใน Bucket `nontimeseries-images`
3. **Inference Workflow Dispatch**: ส่งงานประมวลผลภาพไปยัง `workers/nontimeseries_worker` (ResNet-18 Deep Learning Worker) ผ่าน `libs/arq_client`
4. **Label Studio Integration**: เชื่อมต่อกับ **Label Studio** ผ่าน `libs/label_studio` เพื่อส่งภาพเข้าสู่กระบวนการจัดทำ Data Annotation (Labeling) โดยผู้เชี่ยวชาญ/แพทย์

## โครงสร้างไดเรกทอรี
```text
apps/non_time_series/
├── README.md               # เอกสารอธิบายการทำงานของ Non-Time-Series App
├── main.py                 # FastAPI Application entry point
├── api/                    # API Endpoints (v1)
│   ├── routes_images.py    # Endpoints อัปโหลดและจัดการไฟล์ภาพ
│   ├── routes_classify.py  # Endpoints สำหรับสั่งประมวลผล ResNet-18
│   └── routes_labeling.py  # Endpoints สำหรับ Sync ข้อมูลกับ Label Studio
└── models/                 # Pydantic Schemas สำหรับรับ-ส่งข้อมูลภาพและผลการจำแนก
```

## Developer Job & Task Workflow
- **Developer Job**: พัฒนา FastAPI Endpoints สำหรับการรับอัปโหลดภาพ, ตรวจสอบประเภทไฟล์ (JPEG/PNG/DICOM), ส่งงานเข้า ARQ Queue และดึงสถานะ Annotation จาก Label Studio
- **การเชื่อมต่อ**:
  - `libs/minio_client` -> บันทึกไฟล์ภาพดิบและภาพที่ผ่านการ Preprocess ลง MinIO
  - `libs/arq_client` -> สั่ง Enqueue background job สำหรับการประมวลผลโมเดล ResNet-18
  - `libs/label_studio` -> Import งานภาพเข้าสู่ Label Studio Project และ Export Annotations
