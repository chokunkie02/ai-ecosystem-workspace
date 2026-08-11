"""
Generate Word Report Script for FastAPI Ecosystem Architecture.
Outputs formatted .docx document at user Downloads directory.
Requirement Traceability format matching teacher's prompt 1:1.
"""

import os
import sys
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from doc_builder import (
    init_document,
    add_doc_title,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_body_p,
    add_bullet_p,
    add_code_block,
    add_callout,
    add_image_placeholder,
    add_image,
    add_caption_p,
    create_styled_table,
)


def build_part_1(doc):
    """ส่วนที่ 1: การวางโครงสร้างและสถาปัตยกรรมโปรเจค (ตอบโจทย์ข้อ 1-3, 11-12)"""
    add_heading_1(doc, "ส่วนที่ 1: การวางโครงสร้างและสถาปัตยกรรมโปรเจค (ตอบโจทย์ข้อ 1-3, 11-12)")

    add_heading_2(doc, "1.1 ตำแหน่งที่ตั้งของโปรเจค (Repository Location)")
    add_body_p(
        doc,
        "โค้ดทั้งหมดถูกย้ายจากไดเรกทอรีทดลองเดิม (Sandbox ใน backend/sandbox/) "
        "เข้าสู่โครงสร้าง Repository หลัก (Root Directory ของโปรเจกต์) เพื่อจัดระเบียบโปรเจกต์ให้พร้อมสำหรับการนำไปใช้งานจริงระดับ Production "
        "โดยโครงสร้างใหม่นี้ช่วยให้การจัดการระบบในภาพรวมทำได้ง่ายและเป็นระบบระเบียบมากขึ้น"
    )

    add_heading_2(doc, "1.2 โครงสร้าง Monorepo และการแบ่งส่วนการทำงาน")
    add_body_p(
        doc,
        "ในการออกแบบสถาปัตยกรรม ระบบถูกออกแบบโดยใช้แนวคิด Monorepo เพื่อรวมศูนย์การพัฒนาทั้ง REST API, Shared Libraries "
        "และ Background Workers ไว้ในที่เดียว โดยแบ่งโครงสร้างโฟลเดอร์หลักดังนี้:"
    )
    add_bullet_p(
        doc,
        " เก็บ FastAPI Application จำนวน 2 บริการที่แยกตามประเภทของงานอย่างชัดเจน ได้แก่ "
        "apps/time_series (สำหรับข้อมูลอนุกรมเวลา IoT) และ apps/non_time_series (สำหรับงาน Computer Vision)",
        "apps/:",
    )
    add_bullet_p(
        doc,
        " เก็บ Shared Libraries และ Client Wrappers ที่พัฒนาขึ้นเพื่อห่อหุ้มการสื่อสารกับ External Services (Developer Jobs) "
        "ประกอบด้วย libs/minio_client, libs/redis_client, libs/label_studio และ libs/arq_client",
        "libs/ (Shared Libraries) (Developer Jobs):",
    )
    add_bullet_p(
        doc,
        " เก็บ Asynchronous Background Workers สำหรับประมวลผลโมเดลเบื้องหลังผ่าน ARQ Redis Queue (Developer Jobs) "
        "ประกอบด้วย workers/timeseries_worker (ประมวลผล Prophet/LSTM) และ workers/nontimeseries_worker (ประมวลผล ResNet-18)",
        "workers/ (Background Workers) (Developer Jobs):",
    )
    add_bullet_p(
        doc,
        " เก็บสคริปต์เครื่องมือช่วยงาน เช่น สคริปต์แปลง OpenAPI เป็น Excel/CSV (openapi_to_excel.py) "
        "และสคริปต์สร้างรายงาน Word สถาปัตยกรรมนี้",
        "scripts/:",
    )

    add_heading_2(doc, "1.3 การจัดทำเอกสารกำกับโฟลเดอร์สำคัญ (Developer Jobs README.md)")
    add_body_p(
        doc,
        "เพื่อให้ทีมพัฒนาสามารถเข้ามาทำงานต่อหรือตรวจสอบระบบได้อย่างสะดวก ไฟล์ README.md "
        "ถูกจัดทำและแนบไว้ในทุกโฟลเดอร์สำคัญ (apps/, libs/, workers/, scripts/) โดยภายในแต่ละไฟล์ประกอบด้วยรายละเอียด ดังนี้:"
    )
    add_bullet_p(
        doc,
        " อธิบายหน้าที่และความรับผิดชอบของโมดูลในโฟลเดอร์นั้นๆ อย่างตรงไปตรงมา",
        "คำอธิบายหน้าที่การทำงาน (Overview & Scope):",
    )
    add_bullet_p(
        doc,
        " ระบุรายชื่อและค่าเริ่มต้นของ Environment Variables ที่ต้องใช้ เช่น MINIO_ENDPOINT, REDIS_URL, LABEL_STUDIO_URL",
        "การตั้งค่าตัวแปรสภาพแวดล้อม (Environment Variables):",
    )
    add_bullet_p(
        doc,
        " คำสั่งในการสั่งรันบริการหรือการรัน Unit Test เช่น คำสั่ง uvicorn หรือ arq",
        "ขั้นตอนและคำสั่งในการรัน (Execution & Test Commands):",
    )
    add_bullet_p(
        doc,
        " ตัวอย่างโค้ดการเรียกใช้งาน (Code Snippets) เพื่อให้ทีมพัฒนานำไปใช้งานต่อได้ทันที",
        "ตัวอย่างโค้ดการใช้งาน (Usage Examples):",
    )

    add_code_block(
        doc,
        "# ตัวอย่างคำสั่ง CLI สำหรับรัน FastAPI Applications และ Background Workers\n"
        "# 1. รัน Time-Series API Service\n"
        "uvicorn apps.time_series.main:app --reload --port 8000\n\n"
        "# 2. รัน Non-Time-Series API Service\n"
        "uvicorn apps.non_time_series.main:app --reload --port 8001\n\n"
        "# 3. รัน Background Workers ผ่าน ARQ\n"
        "arq workers.timeseries_worker.WorkerSettings\n"
        "arq workers.nontimeseries_worker.WorkerSettings"
    )


def build_part_2(doc):
    """ส่วนที่ 2: การติดตั้ง Library และห่อหุ้ม Component (libs/ และ workers/) (Developer Jobs) (ตอบโจทย์ข้อ 4)"""
    add_heading_1(doc, "ส่วนที่ 2: การติดตั้ง Library และห่อหุ้ม Component (libs/ และ workers/) (Developer Jobs) (ตอบโจทย์ข้อ 4)")

    add_body_p(
        doc,
        "เพื่อลดความซ้ำซ้อนในการเชื่อมต่อกับบริการภายนอก และทำให้โค้ดในฝั่ง API และ Worker อ่านง่าย "
        "การทำงานกับบริการต่าง ๆ ถูกห่อหุ้ม (Encapsulate) ไว้ในโฟลเดอร์ libs/ และ workers/ ให้เป็น Shared Component และ Background Worker สำหรับภาระงานพัฒนา (Developer Jobs) ดังนี้:"
    )

    add_heading_2(doc, "2.1 MinIO Object Storage Wrapper (libs/minio_client) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส MinIOManager ถูกพัฒนาขึ้นใน libs/minio_client/client.py เพื่อจัดการไฟล์รูปภาพและข้อมูลดิบ "
        "รองรับการตรวจสอบและสร้าง Bucket (ensure_bucket_exists), การอัปโหลดไฟล์ (upload_file) "
        "และการสร้าง Presigned URL สำหรับเปิดดูหรือดาวน์โหลดไฟล์ชั่วคราว (get_presigned_url)"
    )

    add_heading_2(doc, "2.2 Redis Cache & State Wrapper (libs/redis_client) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส RedisCacheManager ถูกพัฒนาขึ้นใน libs/redis_client/client.py โดยใช้ redis.asyncio "
        "ช่วยให้การอ่านและบันทึกข้อมูลแคชในรูปแบบ JSON ทำได้สะดวกรวดเร็วผ่านเมธอด get และ set พร้อมตั้งค่าเวลาหมดอายุ (TTL)"
    )

    add_heading_2(doc, "2.3 Label Studio Integration Wrapper (libs/label_studio) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส LabelStudioConnector ถูกพัฒนาขึ้นใน libs/label_studio/connector.py เพื่อสื่อสารกับ Label Studio REST API ผ่าน httpx.AsyncClient "
        "ใช้สำหรับสร้างโปรเจกต์ติดแท็กข้อมูล (create_project), ส่งเข้า Tasks (import_tasks) และดึงผลลัพธ์การติดแท็ก (get_tasks)"
    )

    add_heading_2(doc, "2.4 ARQ Task Dispatcher Wrapper (libs/arq_client) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส TaskDispatcher ถูกพัฒนาขึ้นใน libs/arq_client/dispatcher.py เพื่อสื่อสารกับ ARQ Redis Queue "
        "สำหรับส่งงานประมวลผลหนักเข้าสู่ Background Worker (enqueue_job) และใช้ติดตามสถานะงาน (get_job_status)"
    )

    add_heading_2(doc, "2.5 Time-Series Background Worker (workers/timeseries_worker) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส WorkerSettings และฟังก์ชันงานพยากรณ์ ถูกพัฒนาขึ้นใน workers/timeseries_worker/worker.py เพื่อประมวลผลงานอนุกรมเวลา (Prophet/LSTM) "
        "ผ่าน ARQ Redis Queue แบบ Asynchronous และบันทึกผลลัพธ์ลง Redis Cache และ MinIO Storage"
    )

    add_heading_2(doc, "2.6 Non-Time-Series Background Worker (workers/nontimeseries_worker) (Developer Jobs)")
    add_body_p(
        doc,
        "คลาส WorkerSettings และฟังก์ชันงานจำแนกภาพ ถูกพัฒนาขึ้นใน workers/nontimeseries_worker/worker.py เพื่อประมวลผลโมเดล ResNet-18 "
        "รับภาพจาก MinIO มาทำการ Inference และส่งผลลัพธ์กลับแบบ Asynchronous"
    )


def build_part_3(doc):
    """ส่วนที่ 3: การออกแบบ Backend Server APIs (ตอบโจทย์ข้อ 5-6)"""
    add_heading_1(doc, "ส่วนที่ 3: การออกแบบ Backend Server APIs (ตอบโจทย์ข้อ 5-6)")

    add_body_p(
        doc,
        "ในการออกแบบเส้นทาง REST API รายการ Endpoint ถูกจัดกลุ่มออกเป็น 3 หมวดหมู่หลัก "
        "เพื่อให้สอดคล้องกับลักษณะการทำงานและการแบ่งหน้าที่ของระบบ ดังแสดงในตารางรายละเอียด 4 คอลัมน์ด้านล่างนี้:"
    )

    add_callout(
        doc,
        "ในการเรียกใช้ API เช่น /api/v1/ls/store ระบบจะใช้ project_id เป็นคีย์หลักในการซิงค์ข้อมูลระหว่าง MinIO (จัดเก็บไฟล์วัตถุ), Redis (จัดเก็บ Cache/State) และ Label Studio (จัดเก็บ Annotation Tasks)",
        "ภาพรวมความเชื่อมโยง Data Flow",
    )

    add_heading_2(doc, "3.1 หมวดหมู่ที่ 1: API สำหรับ Label Studio (/api/v1/ls)")
    headers = ["ชื่อ API Endpoint", "HTTP Type", "พารามิเตอร์ที่รับ (Parameters)", "วัตถุประสงค์การทำงาน"]
    rows_ls = [
        [
            "/api/v1/ls/sync-project",
            "POST",
            "title (str, Body), description (str, Body), label_config (str, Body)",
            "สร้างหรือซิงก์โปรเจกต์ใน Label Studio พร้อมกำหนดรูปแบบ XML Label Config",
        ],
        [
            "/api/v1/ls/tasks",
            "POST",
            "project_id (int, Body), tasks (list[dict], Body)",
            "นำส่งรายการข้อมูลดิบ (Tasks) เข้าสู่โปรเจกต์ Label Studio เพื่อรอการติดแท็ก",
        ],
        [
            "/api/v1/ls/annotations/{project_id}",
            "GET",
            "project_id (int, Path)",
            "ดึงรายการผลการติดแท็ก (Annotations) และพิกัดจาก Label Studio เพื่อนำไปฝึกโมเดล",
        ],
    ]
    create_styled_table(doc, headers, rows_ls, [1.8, 0.8, 2.0, 1.8])

    add_heading_2(doc, "3.2 หมวดหมู่ที่ 2: API สำหรับ MinIO & Redis Storage (/api/v1/store)")
    rows_store = [
        [
            "/api/v1/store/telemetry",
            "POST",
            "sensor_id (str, Body), data (list[dict], Body)",
            "บันทึกข้อมูลเซนเซอร์อนุกรมเวลาลง MinIO Bucket และเขียนข้อมูลลง Redis Cache",
        ],
        [
            "/api/v1/store/telemetry/{sensor_id}",
            "GET",
            "sensor_id (str, Path), limit (int, Query)",
            "ดึงข้อมูลเซนเซอร์ล่าสุดจาก Redis Cache (หรือ MinIO หากไม่พบในแคช)",
        ],
        [
            "/api/v1/store/upload-image",
            "POST",
            "file (UploadFile, Form), bucket_name (str, Form)",
            "อัปโหลดไฟล์ภาพเข้า MinIO Object Storage และคืนค่า Presigned URL",
        ],
        [
            "/api/v1/store/images/{image_id}",
            "GET",
            "image_id (str, Path), expires_in (int, Query)",
            "ดึง Metadata ของรูปภาพ และสร้าง Presigned URL สำหรับดาวน์โหลดชั่วคราว",
        ],
    ]
    create_styled_table(doc, headers, rows_store, [1.8, 0.8, 2.0, 1.8])

    add_heading_2(doc, "3.3 หมวดหมู่ที่ 3: API สำหรับสั่งงาน Background Worker (/api/v1/jobs)")
    rows_jobs = [
        [
            "/api/v1/jobs/forecast",
            "POST",
            "sensor_id (str, Body), horizon (int, Body)",
            "ส่งงานประมวลผลพยากรณ์อนุกรมเวลา (Prophet/LSTM) เข้า ARQ Worker คืนค่า job_id",
        ],
        [
            "/api/v1/jobs/inference",
            "POST",
            "image_id (str, Body), model_type (str, Body)",
            "ส่งงานจำแนกภาพ/ตรวจจับวัตถุด้วย ResNet-18 เข้า ARQ Worker คืนค่า job_id",
        ],
        [
            "/api/v1/jobs/{job_id}",
            "GET",
            "job_id (str, Path)",
            "ตรวจสอบสถานะการทำงาน (queued, in_progress, complete) และดึงผลลัพธ์ของ Job",
        ],
    ]
    create_styled_table(doc, headers, rows_jobs, [1.8, 0.8, 2.0, 1.8])


def build_part_4(doc):
    """ส่วนที่ 4: การจัดทำ API Documentation ด้วย FastAPI (ตอบโจทย์ข้อ 7-9)"""
    add_heading_1(doc, "ส่วนที่ 4: การจัดทำ API Documentation ด้วย FastAPI (ตอบโจทย์ข้อ 7-9)")

    add_heading_2(doc, "4.1 การกำหนด Metadata Arguments ใน FastAPI App")
    add_body_p(
        doc,
        "การตั้งค่า Metadata ถูกกำหนดไว้ในขั้นตอนการสร้าง instance ของ FastAPI() ทั้ง 2 แอปพลิเคชัน (time_series และ non_time_series) "
        "โดยระบุ title, description, version และ openapi_tags เพื่อให้เอกสาร API แสดงข้อมูลอธิบายระบบและจัดหมวดหมู่ได้อย่างชัดเจน"
    )

    add_code_block(
        doc,
        "# ตัวอย่างการกำหนด Metadata Arguments ใน apps/time_series/main.py\n"
        "app = FastAPI(\n"
        "    title='Time-Series Analytics & Forecasting API',\n"
        "    description='REST API สำหรับจัดการข้อมูลอนุกรมเวลา และส่งงานพยากรณ์เข้า Background Worker',\n"
        "    version='1.0.0',\n"
        "    openapi_tags=tags_metadata\n"
        ")"
    )

    add_heading_2(doc, "4.2 เอกสาร Interactive API Documentation")
    add_body_p(
        doc,
        "FastAPI มีความสามารถในการสร้างเอกสาร Interactive Documentation ให้อัตโนมัติใน 2 รูปแบบหลัก ได้แก่:"
    )
    add_bullet_p(
        doc,
        " เข้าใช้งานได้ผ่าน URL /docs (เช่น http://localhost:8000/docs) สำหรับทดลองยิง API และส่งพารามิเตอร์จริงผ่านหน้าเว็บ",
        "Swagger UI (/docs):",
    )
    add_bullet_p(
        doc,
        " เข้าใช้งานได้ผ่าน URL /redoc (เช่น http://localhost:8000/redoc) สำหรับอ่านรายละเอียดโครงสร้าง API และ Schema อย่างเป็นระเบียบ",
        "ReDoc (/redoc):",
    )

    add_heading_2(doc, "4.3 ภาพแคปหน้าจอ Swagger UI และ ReDoc")
    add_body_p(
        doc,
        "ด้านล่างนี้คือภาพแคปหน้าจอการทำงานจริงของ Swagger UI และ ReDoc:"
    )

    swagger_img = Path(r"C:\Users\kt856\Pictures\Screenshots\Screenshot (1169).png")
    if swagger_img.exists():
        add_image(doc, str(swagger_img), width_inches=6.0)
    else:
        add_image_placeholder(
            doc,
            "หน้าต่าง Swagger UI Interactive API Documentation (/docs)",
            "แสดงรายการ API Endpoints แยกตาม Tags (/api/v1/ls, /api/v1/store, /api/v1/jobs) พร้อมปุ่ม Try it out",
        )
    add_caption_p(
        doc,
        "รูปที่ 4.1: ภาพแคปหน้าจอ Swagger UI (/docs) แสดงการจัดหมวดหมู่ Tags และ Metadata",
    )

    redoc_img = Path(r"C:\Users\kt856\Pictures\Screenshots\Screenshot (1170).png")
    if redoc_img.exists():
        add_image(doc, str(redoc_img), width_inches=6.0)
    else:
        add_image_placeholder(
            doc,
            "หน้าต่าง ReDoc API Documentation (/redoc)",
            "แสดงรายละเอียดสเปก API, Request Body Schemas และ Response Models แบบสองคอลัมน์อ่านง่าย",
        )
    add_caption_p(
        doc,
        "รูปที่ 4.2: ภาพแคปหน้าจอ ReDoc (/redoc)",
    )



def build_part_5(doc):
    """ส่วนที่ 5: ระบบ Snapshot และแปลง OpenAPI เป็น Excel/CSV (ตอบโจทย์ข้อ 10)"""
    add_heading_1(doc, "ส่วนที่ 5: ระบบ Snapshot และแปลง OpenAPI เป็น Excel/CSV (ตอบโจทย์ข้อ 10)")

    add_heading_2(doc, "5.1 วิธีการทำงานของสคริปต์ openapi_to_excel.py")
    add_body_p(
        doc,
        "สคริปต์ openapi_to_excel.py ถูกพัฒนาขึ้นในโฟลเดอร์ scripts/ เพื่อดึง OpenAPI JSON Schema "
        "โดยสคริปต์สามารถทำงานได้ 2 รูปแบบ ได้แก่ การอิมพอร์ต FastAPI app object เข้ามาดึง app.openapi() ในหน่วยความจำโดยตรง "
        "(In-memory Direct Extraction) หรือการส่ง HTTP Request ไปดึง OpenAPI JSON จาก URL live server"
    )

    add_heading_2(doc, "5.2 โครงสร้างตาราง Snapshot 9 คอลัมน์")
    add_body_p(
        doc,
        "สคริปต์จะทำการแกะ JSON Schema แล้วนำข้อมูลจัดลงตารางสเปรดชีตจำนวน 9 คอลัมน์มาตรฐาน ดังนี้:"
    )
    add_bullet_p(doc, " ชื่อบริการ (Time-Series API หรือ Non-Time-Series API)", "1. Service:")
    add_bullet_p(doc, " เส้นทาง URL Endpoint (เช่น /api/v1/store/telemetry)", "2. Endpoint Path:")
    add_bullet_p(doc, " ประเภท HTTP Method (GET, POST, PUT, DELETE)", "3. HTTP Method:")
    add_bullet_p(doc, " หมวดหมู่ของ Endpoint (Storage, Label Studio, Jobs)", "4. Tags:")
    add_bullet_p(doc, " สรุปหน้าที่การทำงานสั้นๆ", "5. Summary:")
    add_bullet_p(doc, " คำอธิบายรายละเอียดการทำงาน", "6. Description:")
    add_bullet_p(doc, " รายการพารามิเตอร์ที่รับ (Path, Query, Header)", "7. Parameters:")
    add_bullet_p(doc, " โครงสร้าง Request Body Schema (Pydantic Models)", "8. Request Body Schema:")
    add_bullet_p(doc, " โครงสร้าง Response Models", "9. Response Schema:")

    add_heading_2(doc, "5.3 ผลลัพธ์และการบันทึกไฟล์ Snapshot")
    add_body_p(
        doc,
        "เมื่อสั่งรันสคริปต์ openapi_to_excel.py ระบบจะทำการสร้างไฟล์รายงาน 2 รูปแบบ (.xlsx และ .csv) "
        "และบันทึกไปยังโฟลเดอร์เป้าหมายโดยอัตโนมัติ ดังนี้:"
    )
    add_bullet_p(doc, " ./scripts/api_snapshot.xlsx และ ./scripts/api_snapshot.csv", "โฟลเดอร์ ./scripts/ ภายในโปรเจกต์:")
    add_bullet_p(doc, " api_snapshot.xlsx และ api_snapshot.csv ในโฟลเดอร์ปลายทางฝั่ง Client (Downloads)", "โฟลเดอร์ปลายทางฝั่ง Client (Downloads):")

    add_code_block(
        doc,
        "# คำสั่ง CLI สำหรับรันสคริปต์สกัด API Snapshot เป็น Excel/CSV\n"
        "python scripts/openapi_to_excel.py\n\n"
        "# ผลลัพธ์การทำงานใน Terminal:\n"
        "# Successfully generated API snapshot files:\n"
        "# - ./scripts/api_snapshot.xlsx\n"
        "# - ./scripts/api_snapshot.csv\n"
        "# - ./downloads/api_snapshot.xlsx\n"
        "# - ./downloads/api_snapshot.csv"
    )

    add_callout(
        doc,
        "ไฟล์ api_snapshot.xlsx ที่ได้ สามารถนำไปเปิดตรวจทานโครงสร้าง API ร่วมกับทีมพัฒนาและผู้ตรวจประเมินได้ทันที "
        "โดยไม่ต้องคอยเปิดอ่านทีละเส้นทางในไฟล์โค้ด",
        "ประโยชน์ของ API Snapshot",
    )


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print("Building Word Document Report (Traceability Format)...")
    print("==================================================")

    doc = init_document()

    # Document Header Title (No Cover Page)
    add_doc_title(
        doc,
        "รายงานการพัฒนาระบบนิเวศ FastAPI Ecosystem",
        "(ตอบโจทย์โครงสร้าง Monorepo, Shared Libraries, Workers และ OpenAPI Automation)",
    )

    # Build 5 Main Sections
    build_part_1(doc)
    build_part_2(doc)
    build_part_3(doc)
    build_part_4(doc)
    build_part_5(doc)

    output_dir = Path.home() / "Downloads"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "รายงานสถาปัตยกรรมระบบ_FastAPI_Ecosystem.docx"

    doc.save(output_path)

    print(f"Successfully generated Word report document at:\n{output_path}")
    print("==================================================")


if __name__ == "__main__":
    main()
