"""
Ultra-Detailed Architecture & draw.io Mastery Report PDF Generator
Builds a professional HTML document with full Thai font support, deep-dive component specs,
mathematical formulas, input/output schemas, and draw.io mastery connection matrix analysis,
then converts it to PDF using headless Edge.
"""

import os
import sys
import subprocess
from pathlib import Path

# Target output PDF path
PDF_OUTPUT_PATH = r"C:\Users\kt856\Downloads\AI_Ecosystem_Architecture_Report.pdf"
HTML_TEMP_PATH = r"C:\eco\friday\storage\artifacts\report_temp.html"

def generate_html_content() -> str:
    html = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>AI Ecosystem Architecture & Mastery Deep-Dive Report</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;600&display=swap');

  @page {
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-right {
      content: counter(page);
    }
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: 'Kanit', 'Segoe UI', Tahoma, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  .cover-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    color: #ffffff;
    padding: 32px 28px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
  }

  .cover-badge {
    display: inline-block;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: #ffffff;
    font-size: 8.5pt;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }

  .cover-title {
    font-size: 20pt;
    font-weight: 700;
    margin: 0 0 8px 0;
    line-height: 1.3;
    color: #f8fafc;
  }

  .cover-subtitle {
    font-size: 11pt;
    font-weight: 300;
    color: #cbd5e1;
    margin: 0 0 16px 0;
  }

  .cover-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    font-size: 8.5pt;
    color: #94a3b8;
    border-top: 1px solid #334155;
    padding-top: 14px;
    margin-top: 14px;
  }

  h1 {
    font-size: 15pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }

  h2 {
    font-size: 12pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 20px;
    margin-bottom: 10px;
    padding-left: 10px;
    border-left: 4px solid #7c3aed;
    page-break-after: avoid;
  }

  h3 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 20px;
  }

  li {
    margin-bottom: 4px;
  }

  code {
    font-family: 'Fira Code', Consolas, monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: 'Fira Code', Consolas, monospace;
    font-size: 8pt;
    line-height: 1.4;
    padding: 12px 14px;
    border-radius: 8px;
    overflow-x: auto;
    margin-top: 8px;
    margin-bottom: 12px;
    page-break-inside: avoid;
  }

  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
  }

  .box-container {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }

  .box-title {
    font-size: 10pt;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 6px;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 16px;
    font-size: 8pt;
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid;
  }

  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #334155;
  }

  td {
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }

  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  .badge {
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 10px;
  }

  .badge-sync {
    background-color: #dbeafe;
    color: #1e40af;
    border: 1px solid #93c5fd;
  }

  .badge-async {
    background-color: #f3e8ff;
    color: #6b21a8;
    border: 1px solid #d8b4fe;
  }

  .formula-box {
    background-color: #f1f5f9;
    border-left: 4px solid #10b981;
    padding: 10px 14px;
    font-family: 'Fira Code', Consolas, monospace;
    font-size: 8.5pt;
    margin: 8px 0 12px 0;
    border-radius: 4px;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- COVER HEADER -->
  <div class="cover-header">
    <div class="cover-badge">Sovereign Architecture V3.0 • Monorepo Engineering</div>
    <div class="cover-title">รายงานอธิบายสถาปัตยกรรมระบบ AI Ecosystem เชิงลึกแบบบรรยายรายองค์ประกอบ</div>
    <div class="cover-subtitle">ความเข้าใจโครงสร้างการทำงาน (What, Why, How, Inputs/Outputs) & draw.io Connection Matrix Analysis</div>
    <div class="cover-meta">
      <div><strong>ระบบ:</strong> AI Ecosystem Monorepo</div>
      <div><strong>ภาษาบรรยาย:</strong> ภาษาไทยเชิงเทคนิค (Technical Narrative)</div>
      <div><strong>มาตรฐาน PDF:</strong> Headless Edge Render Engine</div>
      <div><strong>วันที่ปรับปรุง:</strong> 20 สิงหาคม 2026</div>
    </div>
  </div>

  <!-- SECTION 1 -->
  <h1>ส่วนที่ 1: FastAPI Applications เชิงลึก (Time-Series & Non-Time-Series)</h1>
  
  <p>
    ในระบบ AI Ecosystem Monorepo นี้ การประมวลผล API ถูกแบ่งแยกไมโครเซอร์วิสออกเป็น 2 แอปพลิเคชันตามลักษณะของข้อมูลและภาระงาน (Workload Boundaries) ได้แก่ เซอร์วิสประมวลผลข้อมูลอนุกรมเวลา (<code>apps/time_series</code>) และเซอร์วิสประมวลผลคอมพิวเตอร์วิชัน (<code>apps/non_time_series</code>) เพื่อให้ระบบรองรับการขยายตัว (Scalability) และแยกการจัดการทรัพยากรได้อย่างเป็นอิสระ
  </p>

  <h2>1.1 Time-Series Analytics & Forecasting FastAPI Application (<code>apps/time_series</code>)</h2>
  <div class="box-container">
    <div class="box-title">องค์ประกอบที่ 1: แอปพลิเคชันประมวลผลอนุกรมเวลา (apps/time_series)</div>
    <p><strong>1. What it is (คืออะไร):</strong> เป็นบริการเว็บไมโครเซอร์วิสที่พัฒนาด้วย Python FastAPI รันบนพอร์ต <code>8000</code> ทำหน้าที่เป็น API Gateway และ Business Logic Controller สำหรับการรับ บันทึก ค้นหา และประมวลผลข้อมูลอนุกรมเวลา (Time-Series Telemetry) เช่น ค่าเซนเซอร์ในโรงงานอุตสาหกรรม หรือข้อมูลมาตรวัด IoT</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เพื่อแยกภาระงานประมวลผลข้อมูลตัวเลขเชิงเวลาที่มีความถี่สูง ออกจากงานประมวลผลไฟล์ภาพสื่อขนาดใหญ่ ป้องกันไม่ให้ I/O Bottleneck ของงานไฟล์ส่งผลกระทบต่อการรับข้อมูลเซนเซอร์ และใช้ประโยชน์จากสถาปัตยกรรม Asynchronous Non-blocking I/O ของ FastAPI ทำให้สามารถรองรับปริมาณ Concurrent Telemetry Ingestion ได้สูง</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong> 
      เปิดให้บริการผ่าน Uvicorn ASGI Server โดยบริหารจัดการ Routing ออกเป็น 4 กลุ่มหลักผ่าน OpenAPI Tags:
    </p>
    <ul>
      <li><code>/api/v1/store</code>: รับข้อมูลเซนเซอร์ นำเข้า Redis In-Memory Cache (เพื่อการอ่านความเร็วสูง) และบันทึกสำรองลง MinIO Object Storage ในรูปแบบ JSON Stream</li>
      <li><code>/api/v1/ls</code>: เชื่อมต่อ REST API ของ Label Studio เพื่อสร้างโปรเจกต์สำหรับนักวิเคราะห์ และส่งออกชุดข้อมูลเซนเซอร์เข้าสู่อินเทอร์เฟซการติดแท็กค่าผิดปกติ (Anomaly Detection)</li>
      <li><code>/api/v1/jobs</code>: ส่งงานพยากรณ์อนุกรมเวลา (Forecasting) เข้าสู่ ARQ Redis Task Queue เพื่อให้ Background Worker ดึงไปประมวลผลนอก HTTP Thread และบริการดึงสถานะงาน</li>
      <li><code>/api/v1/analytics</code>: คำนวณค่าสถิติ (Mean, Std Dev, Min, Max) ของเซนเซอร์ และส่งคำสั่งเทรนโมเดล AI (Prophet/LSTM)</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> <code>POST /api/v1/store/telemetry</code> รับ JSON Body ตามโครงสร้าง <code>TelemetryIngestRequest</code> ประกอบด้วย <code>sensor_id</code> (string) และ <code>data_points</code> (List ของ object ที่มี <code>timestamp</code> และ <code>value</code>)</li>
      <li><strong>Output:</strong> คืนค่า JSON ตอบกลับ HTTP 200 สรุปสถานะการบันทึก จำนวนจุดข้อมูล และพาธ S3 ที่ถูกจัดเก็บใน MinIO เช่น <code>{"message": "Telemetry data stored", "sensor_id": "sensor-001", "s3_path": "timeseries-data/telemetry/sensor-001/data.json"}</code></li>
      <li><strong>Input:</strong> <code>POST /api/v1/jobs/forecast</code> รับ JSON Body ตามโครงสร้าง <code>ForecastJobRequest</code> (ระบุ <code>sensor_id</code> และจำนวนก้าวอนาคต <code>horizon</code>)</li>
      <li><strong>Output:</strong> คืนค่า JSON สรุปการ Enqueue Job เช่น <code>{"job_id": "arq:job:12345", "status": "queued"}</code></li>
    </ul>
  </div>

  <h2>1.2 Non-Time-Series Computer Vision FastAPI Application (<code>apps/non_time_series</code>)</h2>
  <div class="box-container">
    <div class="box-title">องค์ประกอบที่ 2: แอปพลิเคชันประมวลผลภาพทั่วไปและคอมพิวเตอร์วิชัน (apps/non_time_series)</div>
    <p><strong>1. What it is (คืออะไร):</strong> เป็นบริการเว็บไมโครเซอร์วิสที่พัฒนาด้วย Python FastAPI รันบนพอร์ต <code>8001</code> ทำหน้าที่บริหารจัดการการอัปโหลดไฟล์รูปภาพทั่วไป การตรวจจับวัตถุ (Object Detection) การจำแนกประเภทภาพ (Image Classification) และการวิเคราะห์ผลโมเดลคอมพิวเตอร์วิชัน</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> จัดการงาน Multipart Form Data และไฟล์ภาพไบนารีที่มีขนาดใหญ่โดยเฉพาะ ช่วยจัดการระบบ Presigned Download URL สำหรับรักษาความปลอดภัยไฟล์ และแยกกระบวนการรันโมเดล Deep Learning (ResNet-18) ออกไปประมวลผลใน Background Worker ไม่ให้ขัดจังหวะการทำงานของหน้าเว็บ UI</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ทำงานผ่าน Uvicorn ASGI Server โดยเปิด Routing 4 กลุ่มหลัก:
    </p>
    <ul>
      <li><code>/api/v1/store</code>: รับไฟล์ภาพผ่าน HTTP Multipart Form Upload บันทึกไฟล์ลง MinIO Bucket <code>general-images</code>, สร้าง Presigned URL ที่มีอายุ 3,600 วินาที และบันทึก Metadata (ขนาดไฟล์ ประเภท MIME) ลง Redis Cache Key <code>image:meta:{image_id}</code></li>
      <li><code>/api/v1/ls</code>: สั่งสร้างโปรเจกต์ Label Studio ชนิด Computer Vision Bounding Box ( RectangleLabels XML Configuration) ผ่าน LabelStudioConnector</li>
      <li><code>/api/v1/jobs</code>: Enqueue งานประมวลผลภาพเข้า ARQ Queue เพื่อเรียกใช้โมเดล ResNet-18 ในการตรวจจับวัตถุ</li>
      <li><code>/api/v1/analytics</code>: ให้บริการข้อมูลสถิติการจำแนกประเภทภาพ ความกระจายตัวของค่าความมั่นใจ (Confidence Score Distribution)</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> <code>POST /api/v1/store/upload-image</code> รับไฟล์ไบนารีผ่าน Multipart Form (<code>file: UploadFile</code>) และ Form Parameter <code>image_id</code> (optional)</li>
      <li><strong>Output:</strong> คืนค่า JSON Structure <code>ImageUploadResponse</code> เช่น <code>{"image_id": "img-001", "bucket": "general-images", "object_key": "uploads/img-001_sample.jpg", "presigned_url": "http://localhost:9000/general-images/..."}</code></li>
      <li><strong>Input:</strong> <code>POST /api/v1/jobs/inference</code> รับ JSON Body <code>InferenceJobRequest</code> (ระบุ <code>image_id</code>, <code>image_bucket</code>, <code>object_key</code>)</li>
      <li><strong>Output:</strong> คืนค่า JSON สรุปการส่งงานเข้าคิว เช่น <code>{"job_id": "arq:job:vision-8899", "status": "queued"}</code></li>
    </ul>
  </div>

  <!-- SECTION 2 -->
  <div class="page-break"></div>
  <h1>ส่วนที่ 2: Shared Libraries ทั้ง 4 ตัวเชิงลึก (<code>libs/</code>)</h1>

  <p>
    เพื่อให้เกิดหลักการ DRY (Don't Repeat Yourself) และ Reusability ภายในโครงสร้าง Monorepo ระบบได้สกัดโค้ดส่วนการเชื่อมต่อกับโครงสร้างพื้นฐานออกเป็นไลบรารีส่วนกลาง 4 โมดูลหลัก อยู่ภายใต้โฟลเดอร์ <code>libs/</code>
  </p>

  <h2>2.1 MinIO Object Storage Manager Client (<code>libs/minio_client</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Shared Python Library (คลาส <code>MinIOManager</code>) ที่ห่อหุ้ม (Wrapper) MinIO Official Python SDK (<code>minio.Minio</code>) เพื่อจัดการไฟล์วัตถุ (Object Storage) ที่รองรับ S3 Protocol</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> ซ่อนความซับซ้อนในการตั้งค่าการเชื่อมต่อ S3, การตรวจสอบความมีอยู่ของ Bucket การแปลง Data Stream ให้เข้ากับรูปแบบไบนารี และการสร้าง Presigned URL ช่วยให้แอปพลิเคชันและ Worker ทั้งหมดอัปโหลดและดาวน์โหลดไฟล์ด้วยมาตรฐานเดียวกัน</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      อ่านการตั้งค่าจากตัวแปรสภาพแวดล้อม <code>MINIO_ENDPOINT</code>, <code>MINIO_ACCESS_KEY</code>, <code>MINIO_SECRET_KEY</code> และ <code>MINIO_SECURE</code> เมธอดหลักประกอบด้วย:
    </p>
    <ul>
      <li><code>ensure_bucket_exists(bucket_name)</code>: ตรวจสอบว่ามี Bucket หรือไม่ หากยังไม่มีจะทำการสร้างอัตโนมัติ (<code>make_bucket</code>)</li>
      <li><code>upload_file(...)</code>: รองรับการรับข้อมูลทั้ง Local File Path (ใช้ <code>fput_object</code>), Bytes หรือ Binary Stream (แปลงเป็น <code>io.BytesIO</code> แล้วอัปโหลดด้วย <code>put_object</code>)</li>
      <li><code>get_presigned_url(...)</code>: สร้าง URL สำหรับดาวน์โหลดไฟล์ที่มีการลงรหัสความปลอดภัยตามระยะเวลาที่กำหนด (GET Method Presigned URL)</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> ชื่อ Bucket (string), ชื่อ Object Key (string), ข้อมูลไฟล์ (FilePath, Bytes หรือ Stream), Content-Type (เช่น <code>application/json</code>, <code>image/jpeg</code>)</li>
      <li><strong>Output:</strong> String แสดง S3 Key Path (เช่น <code>timeseries-data/telemetry/s01.json</code>) หรือ String URL ที่มี Query Token สำหรับดาวน์โหลด</li>
    </ul>
  </div>

  <h2>2.2 Redis Cache & State Manager Client (<code>libs/redis_client</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Shared Python Library (คลาส <code>RedisCacheManager</code>) ที่ทำงานแบบ Asynchronous ผ่าน <code>redis.asyncio</code> เพื่อบริหารจัดการ In-Memory Cache และการเก็บสถานะใน Redis</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เพื่อสกัดกั้น HTTP Request ไม่ให้ต้องวิ่งไปอ่านดิสก์หรือฐานข้อมูลทุกครั้ง เพิ่มความเร็วในการอ่านข้อมูลเป็นระดับ Sub-millisecond พร้อมจัดการ Prefix ของ Key (<code>app:</code>) อัตโนมัติเพื่อป้องกัน Key ชนกันระหว่างบริการ</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      เชื่อมต่อกับ Redis Host (<code>:6379</code>) แบบ Async Connection Pooling เมธอดสำคัญได้แก่:
    </p>
    <ul>
      <li><code>set(key, value, expire_seconds)</code>: หาก value เป็น Python Dict หรือ List จะทำการแปลงเป็น JSON String อัตโนมัติ (Auto-Serialization) และบันทึกลง Redis พร้อมตั้งค่า Expiration TTL</li>
      <li><code>get(key, default)</code>: อ่านค่าจาก Redis และหากค่านั้นเป็นรูปแบบ JSON จะทำการถอดรหัสกลับเป็น Python Dict/List อัตโนมัติ (Auto-Deserialization)</li>
      <li><code>delete(key)</code> / <code>exists(key)</code>: ลบและตรวจสอบ Key ในคลังข้อมูล</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> Key (string), Value (Python Dict, List, String, Int), ระยะเวลาหมดอายุในหน่วยวินาที (optional int)</li>
      <li><strong>Output:</strong> Boolean <code>True/False</code> สำหรับการบันทึก และ Python Object (Dict/List/String) หรือ <code>None</code> สำหรับการดึงข้อมูล</li>
    </ul>
  </div>

  <h2>2.3 ARQ Task Dispatcher Client (<code>libs/arq_client</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Shared Python Library (คลาส <code>TaskDispatcher</code>) สำหรับทำหน้าที่เป็น Message Producer ในการนำส่งคำสั่งงาน (Enqueue Jobs) เข้าสู่ ARQ Redis Queue</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เพื่อแยกการสั่งงาน (Job Dispatching) ออกจากการประมวลผลงาน (Job Execution) ช่วยให้ API ตอบกลับผู้ใช้ได้ทันทีโดยไม่ต้องรอให้งาน AI/ML ประมวลผลเสร็จ และเป็นตัวกลางในการดึงสถานะงาน (Job Tracking)</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ใช้องค์ประกอบ <code>arq.connections.create_pool</code> ร่วมกับ <code>RedisSettings</code> เมธอดหลักประกอบด้วย:
    </p>
    <ul>
      <li><code>enqueue_job(function_name, *args, **kwargs)</code>: ผลักดันชื่อฟังก์ชันและอาร์กิวเมนต์เข้าสู่ Redis Queue <code>arq:queue</code></li>
      <li><code>get_job_status(job_id)</code>: สร้างอินสแตนซ์ <code>Job(job_id)</code> เพื่อสอบถามสถานะ (queued, in_progress, complete, failed) และดึงผลลัพธ์การรัน</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> ชื่อฟังก์ชันเป้าหมาย (string เช่น <code>process_timeseries_forecast</code>), พารามิเตอร์ของงาน (*args, **kwargs)</li>
      <li><strong>Output:</strong> Dictionary สรุปข้อมูลงาน เช่น <code>{"job_id": "arq:job:abc1234", "function": "process_timeseries_forecast", "status": "queued"}</code></li>
    </ul>
  </div>

  <h2>2.4 Label Studio REST API Connector Client (<code>libs/label_studio</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Shared Python Library (คลาส <code>LabelStudioConnector</code>) ที่ห่อหุ้ม <code>httpx.AsyncClient</code> สำหรับการสื่อสารผ่าน HTTP REST API กับระบบ Label Studio Container</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> ควบคุมโปรเจกต์ติดแท็กข้อมูลผ่านโค้ดอัตโนมัติ (Programmatic Annotation Management) ช่วยให้ FastAPI สามารถสร้างโปรเจกต์ นำเข้า Data Tasks และดึง Annotation Results กลับมาปรับปรุงโมเดลได้อย่างไร้รอยต่อ</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      อ่าน <code>LABEL_STUDIO_URL</code> (พอร์ต <code>8080</code>) และ <code>LABEL_STUDIO_API_KEY</code> ส่ง Header <code>Authorization: Token <API_KEY></code> เมธอดสำคัญได้แก่:
    </p>
    <ul>
      <li><code>create_project(title, description, label_config)</code>: ส่งคำสั่ง <code>POST /api/projects/</code> พร้อมโครงสร้างกำหนดหน้าจอติดแท็ก XML</li>
      <li><code>import_tasks(project_id, tasks)</code>: ส่งคำสั่ง <code>POST /api/projects/{id}/import</code> เพื่อนำเข้าชุดข้อมูล JSON เข้าสู่โปรเจกต์</li>
      <li><code>get_project_annotations(project_id)</code>: ดึงรายการการติดแท็กที่นักวิเคราะห์บันทึกเรียบร้อยแล้ว</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> ชื่อโปรเจกต์, รายละเอียด, XML Configuration String, List ของ Task Dictionaries</li>
      <li><strong>Output:</strong> JSON Metadata ของโปรเจกต์ (รวม <code>project_id</code>), สถิติจำนวน Task ที่นำเข้าสำเร็จ หรือ JSON Annotation Coordinates</li>
    </ul>
  </div>

  <!-- SECTION 3 -->
  <div class="page-break"></div>
  <h1>ส่วนที่ 3: ARQ Async Background Workers เชิงลึก (<code>workers/</code>)</h1>

  <p>
    งานคำนวณทางคณิตศาสตร์และโมเดล AI/ML ถูกแยกออกไปประมวลผลเบื้องหลังโดยกระบวนการ ARQ Worker ซึ่งทำงานแบบ Asynchronous Event-Driven Process คอยเฝ้าดึงงานจากคิว Redis มาทำงานทีละรายการ
  </p>

  <h2>3.1 Time-Series ARQ Worker (<code>workers/timeseries_worker</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Background Worker Process ที่รันสคริปต์ <code>workers/timeseries_worker/worker.py</code> คอยรับงานพยากรณ์อนุกรมเวลาและการฝึกฝนโมเดล Prophet / LSTM</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เพื่อป้องกันไม่ให้การคำนวณทางคณิตศาสตร์ของการพยากรณ์ข้อมูลเซนเซอร์ ใช้ทรัพยากร CPU ของ API Service จนทำให้การรับคำขอ HTTP ของผู้ใช้ท่านอื่นเกิดอาการค้าง (Block)</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      เริ่มต้นระบบผ่าน <code>startup(ctx)</code> hook ผูกอินสแตนซ์ <code>MinIOManager</code> และ <code>RedisCacheManager</code> เข้ากับ Context <code>ctx</code> เมื่อเกิดฟังก์ชัน <code>process_timeseries_forecast</code>:
    </p>
    <ol>
      <li>ดึงชุดข้อมูล <code>data_points</code> ของเซนเซอร์ และคำนวณค่าทางสถิติพื้นฐาน (Mean, Std Dev)</li>
      <li>จำลองและคำนวณสมการพยากรณ์ตามอนุกรมเวลาไปข้างหน้าตามจำนวน <code>horizon</code> สร้างค่าพยากรณ์ <code>yhat</code> และช่วงความเชื่อมั่น <code>yhat_lower</code>, <code>yhat_upper</code></li>
      <li>คำนวณดรรชนีวัดผลความแม่นยำ ได้แก่ MAE (Mean Absolute Error), RMSE (Root Mean Squared Error) และ MAPE (Mean Absolute Percentage Error)</li>
      <li>บันทึก JSON ผลลัพธ์ลง MinIO Bucket <code>timeseries-predictions</code> (เพื่อความคงทน) และบันทึกลง Redis Cache Key <code>forecast:latest:{sensor_id}</code> (เพื่อความรวดเร็ว)</li>
    </ol>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> <code>sensor_id</code> (string), <code>data_points</code> (List ของ Dict ข้อมูลเวลาและค่าเซนเซอร์), <code>horizon</code> (int จำนวนก้าวอนาคต)</li>
      <li><strong>Output:</strong> JSON Payload ผลลัพธ์การพยากรณ์ รายการพิกัดอนาคต ค่าดรรชนีวัดผล MAE/RMSE/MAPE และ S3 Object Key (เช่น <code>timeseries-predictions/forecasts/s01_177145.json</code>)</li>
    </ul>
  </div>

  <h2>3.2 Non-Time-Series Computer Vision ARQ Worker (<code>workers/nontimeseries_worker</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็น Background Worker Process ที่รันสคริปต์ <code>workers/nontimeseries_worker/worker.py</code> คอยรับงานประมวลผลภาพ คอมพิวเตอร์วิชัน และโมเดล ResNet-18</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> การรันโมเดล Deep Learning บนรูปภาพต้องใช้ความจำและ CPU/GPU สูง การแยกประมวลผลใน Worker ช่วยให้ระบบจัดการ Queue Prioritization และรองรับการทำ Worker Horizontal Scaling ได้ง่าย</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      เริ่มต้นระบบผ่าน <code>startup(ctx)</code> hook เมื่อเกิดฟังก์ชัน <code>process_image_inference</code>:
    </p>
    <ol>
      <li>ดึงอ้างอิงรูปภาพ <code>image_id</code> และ <code>object_key</code> จาก MinIO Bucket <code>general-images</code></li>
      <li>ส่งภาพเข้าสู่ ResNet-18 Model Inference Pipeline เพื่อคำนวณหา Class Probability, Confidence Score และ Bounding Box Region Coordinates</li>
      <li>สรุปผลป้ายกำกับ (เช่น <code>OBJECT_DETECTED</code> หรือ <code>NORMAL</code>) พร้อมหมวดหมู่วัตถุ (Vehicle, Person, Equipment)</li>
      <li>บันทึก JSON ผลลัพธ์ลง MinIO Bucket <code>vision-results</code> และอัปเดต Redis Cache Key <code>image:result:{image_id}</code></li>
    </ol>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> <code>image_id</code> (string), <code>image_bucket</code> (string), <code>object_key</code> (string)</li>
      <li><strong>Output:</strong> JSON Inference Result Document ประกอบด้วย ค่าความมั่นใจ (Confidence Score 0.88-0.99), Bounding Box (<code>x_min</code>, <code>y_min</code>, <code>x_max</code>, <code>y_max</code>), สรุปผลการตรวจจับ และ S3 Object Key ใน <code>vision-results</code></li>
    </ul>
  </div>

  <!-- SECTION 4 -->
  <div class="page-break"></div>
  <h1>ส่วนที่ 4: AI/ML Algorithms เชิงลึกทั้ง 3 ตัว (Principles, Equations, Inputs/Outputs)</h1>

  <p>
    ระบบ AI Ecosystem ได้ประยุกต์ใช้ อัลกอริทึม ปัญญาประดิษฐ์และคณิตศาสตร์การเรียนรู้ของเครื่อง (Machine Learning / Deep Learning Models) จำนวน 3 สถาปัตยกรรมหลัก ตามประเภทของงานข้อมูล
  </p>

  <h2>4.1 Facebook Prophet Algorithm (Time-Series Forecasting)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นอัลกอริทึมพยากรณ์อนุกรมเวลาแบบการรวมส่วนประกอบ (Additive Model) ที่ถูกพัฒนาโดยทีมวิจัย Meta (Facebook)</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> มีความโดดเด่นในการรับมือกับข้อมูลอนุกรมเวลาในโลกความเป็นจริงที่มีค่าขาดหาย (Missing Values), ค่าผิดปกติฉับพลัน (Outliers) และการเปลี่ยนแปลงของแนวโน้มตามฤดูกาล (Seasonality) โดยไม่ต้องแปลงข้อมูลให้คงที่ (Non-stationary to Stationary) ก่อน</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      แยกย่อยฟังก์ชันอนุกรมเวลา \(y(t)\) ออกเป็น 4 สัมประสิทธิ์ทางคณิตศาสตร์:
    </p>
    <div class="formula-box">
      y(t) = g(t) + s(t) + h(t) + ε_t
    </div>
    <ul>
      <li>\(g(t)\): Trend Function วัดการเติบโตหรือลดลงของข้อมูล ใช้ Piecewise Linear Model ร่วมกับ Automatic Changepoint Selection</li>
      <li>\(s(t)\): Seasonality Function วัดรูปแบบซ้ำๆ (รายวัน รายสัปดาห์ รายปี) คำนวณด้วย Fourier Series:
        <div class="formula-box">s(t) = Σ [ a_n cos(2π n t / P) + b_n sin(2π n t / P) ]</div>
      </li>
      <li>\(h(t)\): Holiday Function วัดผลกระทบจากวันหยุดหรือเหตุการณ์พิเศษตามตารางเวลา</li>
      <li>\(\epsilon_t\): Error Term สันนิษฐานว่าเป็น Gaussian Distributed Noise</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> Dataframe ที่มี 2 คอลัมน์บังคับ ได้แก่ <code>ds</code> (Datestamp ในรูปแบบ <code>YYYY-MM-DD HH:MM:SS</code>) และ <code>y</code> (Numeric Telemetry Value)</li>
      <li><strong>Output:</strong> Dataframe ที่มีคอลัมน์ <code>yhat</code> (ค่าพยากรณ์หลัก), <code>yhat_lower</code> (ขอบล่าง 95% Confidence Interval) และ <code>yhat_upper</code> (ขอบบน 95% Confidence Interval)</li>
    </ul>
  </div>

  <h2>4.2 PyTorch LSTM - Long Short-Term Memory (Sequential Neural Network)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นสถาปัตยกรรมโครงข่ายประสาทเทียมแบบถดถอย (Recurrent Neural Network - RNN) ชนิดพิเศษที่ถูกออกแบบให้มีหน่วยความจำภายใน (Cell State) สำหรับเรียนรู้รูปแบบในลำดับข้อมูลระยะยาว</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> แก้ไขปัญหา Vanishing / Exploding Gradient ที่มักเกิดใน Standard RNN เมื่อประมวลผลข้อมูลอนุกรมเวลาที่มี Sequence ลำดับยาวๆ ทำให้สามารถจดจำรูปแบบพฤติกรรมย้อนหลังของเซนเซอร์ได้อย่างมีประสิทธิภาพ</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ควบคุมการไหลของข้อมูลผ่าน Gate 3 ชนิด และ Cell State (\(C_t\)):
    </p>
    <ol>
      <li><strong>Forget Gate (\(f_t\)):</strong> ตัดสินใจว่าจะลบข้อมูลเก่าออกจาก Cell State หรือไม่:
        <div class="formula-box">f_t = σ(W_f · [h_{t-1}, x_t] + b_f)</div>
      </li>
      <li><strong>Input Gate (\(i_t\)) & Candidate Vector (\(\tilde{C}_t\)):</strong> ตัดสินใจว่าจะบันทึกข้อมูลใหม่ใดลง Cell State:
        <div class="formula-box">
          i_t = σ(W_i · [h_{t-1}, x_t] + b_i)<br>
          C̃_t = tanh(W_c · [h_{t-1}, x_t] + b_c)<br>
          C_t = f_t * C_{t-1} + i_t * C̃_t
        </div>
      </li>
      <li><strong>Output Gate (\(o_t\)) & Hidden State (\(h_t\)):</strong> คำนวณค่าที่จะส่งออกไปยัง Layer ถัดไป:
        <div class="formula-box">
          o_t = σ(W_o · [h_{t-1}, x_t] + b_o)<br>
          h_t = o_t * tanh(C_t)
        </div>
      </li>
    </ol>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> PyTorch 3D Tensor ขนาด <code>(batch_size, sequence_length, feature_dimension)</code> เช่น <code>(32, 50, 1)</code> ข้อมูลย้อนหลัง 50 สเตป</li>
      <li><strong>Output:</strong> PyTorch 2D Tensor ขนาด <code>(batch_size, prediction_horizon)</code> แสดงค่าพยากรณ์ล่วงหน้าของเซนเซอร์</li>
    </ul>
  </div>

  <h2>4.3 PyTorch ResNet-18 (Deep Convolutional Neural Network)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นโครงข่ายประสาทแบบคอนโวลูชันเชิงลึก (Deep Convolutional Neural Network) จำนวน 18 ชั้นที่ประยุกต์ใช้สถาปัตยกรรม Residual Learning</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> แก้ไขปัญหา Degradation Problem (การที่ประสิทธิภาพของโมเดลลดลงเมื่อเพิ่มความลึกของชั้นโครงข่าย) ช่วยให้ Gradient สามารถไหลย้อนกลับในขั้นตอน Backpropagation ได้ง่าย ดึงคุณลักษณะ (Features) ของภาพรูปทรงวัตถุได้อย่างแม่นยำ</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ใช้สถาปัตยกรรม Residual Block ที่มี Identity Shortcut Connection:
    </p>
    <div class="formula-box">
      y = F(x, {W_i}) + x
    </div>
    <p>ลำดับชั้นการประมวลผลประกอบด้วย:</p>
    <ul>
      <li><strong>Initial Conv Layer:</strong> Conv 7x7 (Stride 2), Batch Normalization, ReLU Activation และ Max Pooling 3x3 ยุบขนาดภาพมิติแรก</li>
      <li><strong>4 Residual Layer Groups:</strong> แต่ละกลุ่มประกอบด้วย 2x2 Residual Blocks (Conv 3x3 → BN → ReLU → Conv 3x3 → BN → Shortcut Addition → ReLU)</li>
      <li><strong>Classification Head:</strong> Global Average Pooling (GAP) ยุบ Feature Map ให้เหลือ Vector 512 มิติ ส่งต่อเข้า Fully Connected Linear Layer เพื่อหา Class Logits</li>
    </ul>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> PyTorch 4D Image Tensor ขนาด <code>(batch_size, 3, height, width)</code> ที่ปรับขนาดเป็น 224x224 และผ่าน Standard ImageNet Normalization</li>
      <li><strong>Output:</strong> Logits Vector ขนาด <code>(batch_size, num_classes)</code> แปลงผ่าน Softmax เป็น Class Probability และ Bounding Box Bounding Coordinates <code>(x_min, y_min, x_max, y_max)</code></li>
    </ul>
  </div>

  <!-- SECTION 5 -->
  <div class="page-break"></div>
  <h1>ส่วนที่ 5: Infrastructure Components ทั้ง 4 ตัวเชิงลึก</h1>

  <p>
    โครงสร้างพื้นฐานระดับล่าง (Infrastructure Containers) ถูกควบคุมและจัดเตรียมสภาพแวดล้อมผ่าน Docker Compose (<code>compose.yml</code>) จำนวน 4 คอนเทนเนอร์หลัก เพื่อรองรับการทำงานของระบบ AI Ecosystem
  </p>

  <h2>5.1 PostgreSQL Database Container (<code>postgres:15</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นระบบจัดการฐานข้อมูลเชิงสัมพันธ์ (Relational Database Management System - RDBMS) ประสิทธิภาพสูง รันคอนเทนเนอร์บนพอร์ต <code>5432</code> (เปิดแมปออกพอร์ตเครื่องโฮสต์ <code>5433</code>)</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เป็น Single Source of Truth สำหรับข้อมูลโครงสร้าง Relational ที่ต้องการความคงทนและถูกต้องสมบูรณ์สูง เช่น ข้อมูลบัญชีผู้ใช้, สิทธิ์การเข้าถึง, ผังโครงสร้างโปรเจกต์ Label Studio, รายการ Data Tasks และประวัติการบันทึกแท็ก Annotation</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ประมวลผลคำสั่ง SQL ภายใต้คุณสมบัติ ACID Transactions บันทึกข้อมูลแบบจัดเก็บบนดิสก์คงทนผ่าน Docker Named Volume <code>postgresql-data</code> มีการทำ Indexing และจัดการความสัมพันธ์ระหว่างตารางผ่าน Foreign Keys
    </p>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> คำสั่ง SQL (DDL, DML, Prepared Statements) และการเชื่อมต่อผ่าน PostgreSQL Wire Protocol</li>
      <li><strong>Output:</strong> Tabular Result Sets (รายการแถวข้อมูลในตาราง), Transaction Execution Status Codes</li>
    </ul>
  </div>

  <h2>5.2 Redis In-Memory Store & Queue Container (<code>redis:8.8.0-alpine</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นระบบจัดเก็บข้อมูลในหน่วยความจำความเร็วสูง (In-Memory Key-Value Data Structure Store) รันคอนเทนเนอร์บนพอร์ต <code>6379</code></p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> รับบทบาทสำคัญ 2 ประการในระบบ: (1) ทำหน้าที่เป็น Caching Layer สำหรับ API เก็บข้อมูล Telemetry และ Metadata ชั่วคราว (2) ทำหน้าที่เป็น Message Broker & Queue Storage สำหรับ ARQ Background Workers</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      จัดเก็บข้อมูลบนหน่วยความจำ RAM อ่านเขียนด้วยความเร็วระดับ Microsecond รองรับโครงสร้างข้อมูล String, Hash, List มีระบบตั้งเวลาหมดอายุ (TTL Eviction) และทำการ Snapshot ข้อมูลลงดิสก์ด้วย AOF/RDB ผ่าน Volume <code>redis-data</code>
    </p>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> คำสั่ง Redis Command Protocol (เช่น <code>GET</code>, <code>SET</code>, <code>EXPIRE</code>, <code>LPUSH</code>, <code>RPOP</code>)</li>
      <li><strong>Output:</strong> Value Payload (String, JSON, Bytes) หรือ Task Message Tuples สำหรับ Worker</li>
    </ul>
  </div>

  <h2>5.3 MinIO High-Performance Object Storage Container</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นระบบจัดเก็บไฟล์วัตถุ (Object Storage System) ที่รองรับมาตรฐาน AWS S3 API รันคอนเทนเนอร์บนพอร์ต <code>9000</code> (API) และ <code>9001</code> (Web Console)</p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> จัดเก็บข้อมูลไร้โครงสร้าง (Unstructured Data) ขนาดใหญ่ เช่น ไฟล์รูปภาพไบนารี, ชุดข้อมูลอนุกรมเวลาดิบ, ไฟล์น้ำหนักโมเดล (Model Checkpoint <code>.pt</code>) และไฟล์ JSON ผลลัพธ์ประมวลผล</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      จัดเก็บไฟล์ตามโครงสร้าง Bucket แยกตามโดเมนงาน (<code>timeseries-data</code>, <code>general-images</code>, <code>timeseries-predictions</code>, <code>vision-results</code>, <code>model-checkpoints</code>) มีระบบรหัสความปลอดภัย Presigned URL และบันทึกข้อมูลคงทนผ่าน Volume <code>minio-data</code>
    </p>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> S3 API HTTP Requests, Binary Stream, Multipart Upload Data</li>
      <li><strong>Output:</strong> Object Byte Streams, S3 URIs (<code>s3://bucket/key</code>), Signed Access Download Links</li>
    </ul>
  </div>

  <h2>5.4 Label Studio Data Annotation Container (<code>heartexlabs/label-studio:latest</code>)</h2>
  <div class="box-container">
    <p><strong>1. What it is (คืออะไร):</strong> เป็นแพลตฟอร์มเครื่องมือสำหรับสร้างโปรเจกต์ติดแท็กข้อมูล (Multi-Modal Data Labeling Tool) รันคอนเทนเนอร์บนพอร์ต <code>8080</code></p>
    <p><strong>2. Why it is used (มีไว้ทำไม):</strong> เป็นอินเทอร์เฟซให้มนุษย์ผู้เชี่ยวชาญ (Human-in-the-Loop) ทำการตรวจวัด วาด Bounding Box บนรูปภาพ หรือระบุช่วงเวลาผิดปกติของข้อมูลอนุกรมเวลา เพื่อสร้าง Ground Truth Dataset สำหรับเทรน AI</p>
    <p><strong>3. How it works (ทำงานอย่างไร):</strong>
      ต่อเชื่อมกับ PostgreSQL เป็นฐานข้อมูลหลัก เปิดบริการ REST API ให้ FastAPI สั่งงานอัตโนมัติ อ่านไฟล์ภาพสื่อจาก MinIO มาแสดงผลบน Web Dashboard หน้าจอติดแท็ก
    </p>
    <p><strong>4. Inputs & Outputs (รับและส่งข้อมูลอะไร):</strong></p>
    <ul>
      <li><strong>Input:</strong> Data Tasks (Telemetry JSON / Image URLs), XML Config Payload, คำสั่งบันทึกแท็กจากนักวิเคราะห์</li>
      <li><strong>Output:</strong> Annotation Results JSON Object (ประกอบด้วยพิกัด Bounding Box, Polygon, Time Ranges, Sentiment Categories)</li>
    </ul>
  </div>

  <!-- SECTION 6 -->
  <div class="page-break"></div>
  <h1>ส่วนที่ 6: คำอธิบายจุดเชื่อมต่อใน draw.io Connection Matrix แบบละเอียดทีละเส้น (Lines 1 - 27)</h1>

  <p>
    แผนผังไดอะแกรมสถาปัตยกรรมใน <code>overview/overview.drawio</code> ถูกออกแบบโดยมีจุดเชื่อมต่อ (Connection Lines) จำนวน 27 เส้น เพื่อแสดงการไหลของข้อมูลและการปฏิสัมพันธ์ระหว่างองค์ประกอบต่างๆ รายละเอียดเชิงลึกของแต่ละเส้นเชื่อมต่อมีดังนี้:
  </p>

  <table>
    <thead>
      <tr>
        <th style="width: 4%;">#</th>
        <th style="width: 16%;">ต้นทาง (Source)</th>
        <th style="width: 16%;">ปลายทาง (Target)</th>
        <th style="width: 12%;">โพรโทคอล / พอร์ต</th>
        <th style="width: 32%;">เหตุผลในการลากเส้น & ข้อมูลที่วิ่งผ่าน (Payload & Purpose)</th>
        <th style="width: 10%;">รูปแบบ</th>
        <th style="width: 10%;">การรับมือข้อผิดพลาด</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/store/telemetry</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้/อุปกรณ์ IoT ส่งข้อมูลเซนเซอร์นำเข้าสู่ระบบ<br><strong>ข้อมูล:</strong> JSON Body <code>TelemetryIngestRequest</code> (ประกอบด้วย <code>sensor_id</code> และอาร์เรย์ของจุดข้อมูลเวลา-ค่าเซนเซอร์)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>HTTP 422 Validation Error หาก Body ไม่ตรงตาม Pydantic Schema</td>
      </tr>
      <tr>
        <td>2</td>
        <td>Time-Series FastAPI</td>
        <td>Redis Cache Store</td>
        <td>redis-py async<br><code>:6379</code></td>
        <td><strong>เหตุผล:</strong> API บันทึกข้อมูลเซนเซอร์ลง Redis เพื่อการอ่านอย่างรวดเร็ว (Low Latency Cache)<br><strong>ข้อมูล:</strong> JSON String List ภายใต้ Key <code>telemetry:raw:{sensor_id}</code> ( TTL 86,400 วินาที)</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>Automatic Connection Pool Retry (สูงสุด 3 ครั้ง)</td>
      </tr>
      <tr>
        <td>3</td>
        <td>Time-Series FastAPI</td>
        <td>MinIO Storage Container</td>
        <td>S3 Protocol / SDK<br><code>:9000</code></td>
        <td><strong>เหตุผล:</strong> API บันทึกสำรองชุดข้อมูลเซนเซอร์ดิบลง Object Storage ระยะยาว<br><strong>ข้อมูล:</strong> Raw Telemetry JSON Stream ไปยัง Bucket <code>timeseries-data</code> Key <code>telemetry/{sensor_id}/data.json</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>เรียก <code>ensure_bucket_exists()</code> สร้าง Bucket อัตโนมัติหากไม่พบ</td>
      </tr>
      <tr>
        <td>4</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/store/telemetry/{id}</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้ร้องขออ่านข้อมูลเซนเซอร์ย้อนหลังที่เคยบันทึกไว้<br><strong>ข้อมูล:</strong> HTTP GET Parameter <code>sensor_id</code>, ตอบกลับด้วย JSON Array ของจุดข้อมูลเซนเซอร์</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>HTTP 404 Not Found หากเกิด Redis Cache Miss</td>
      </tr>
      <tr>
        <td>5</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/ls/sync-project</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งซิงก์หรือสร้างโปรเจกต์ติดแท็กข้อมูลอนุกรมเวลาใน Label Studio<br><strong>ข้อมูล:</strong> JSON Body <code>LabelStudioSyncRequest</code> (ระบุชื่อโปรเจกต์และคำอธิบาย)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>Graceful Fallback คืนค่า Mock Project ID 101 หากซิงก์ล้มเหลว</td>
      </tr>
      <tr>
        <td>6</td>
        <td>Time-Series FastAPI</td>
        <td>Label Studio Container</td>
        <td>HTTP REST / httpx<br><code>:8080/api/projects/</code></td>
        <td><strong>เหตุผล:</strong> API ส่งคำสั่งสร้างโปรเจกต์ไปยัง Label Studio ผ่าน HTTP REST<br><strong>ข้อมูล:</strong> XML TimeSeries Labeling Configuration Payload พร้อม Bearer API Token Header</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ดักจับ <code>httpx.RequestError</code> แล้วส่งคืนโครงสร้าง Fallback</td>
      </tr>
      <tr>
        <td>7</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/ls/tasks</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งนำเข้าชุดข้อมูลเซนเซอร์เข้าสู่โปรเจกต์ Label Studio<br><strong>ข้อมูล:</strong> Query Parameters <code>project_id</code> และ <code>sensor_id</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>คืนค่า Mock Imported Task Count หากเชื่อมต่อล้มเหลว</td>
      </tr>
      <tr>
        <td>8</td>
        <td>Time-Series FastAPI</td>
        <td>Label Studio Container</td>
        <td>HTTP REST / httpx<br><code>:8080/api/projects/{id}/import</code></td>
        <td><strong>เหตุผล:</strong> API แปลงข้อมูลเซนเซอร์ส่งเข้าระบบนำเข้างานของ Label Studio<br><strong>ข้อมูล:</strong> JSON Array ของ Data Tasks ที่ฟอร์แมตตามข้อกำหนดของ Label Studio</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ดักจับ Exception และส่งคืนสถานะ <code>mock_imported</code></td>
      </tr>
      <tr>
        <td>9</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/jobs/forecast</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งงานประมวลผลพยากรณ์อนุกรมเวลารูปแบบการทำงานเบื้องหลัง<br><strong>ข้อมูล:</strong> JSON Body <code>ForecastJobRequest</code> (ระบุ <code>sensor_id</code> และ <code>horizon</code>)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>HTTP 500 Internal Error หากส่งงานเข้า ARQ Queue ไม่สำเร็จ</td>
      </tr>
      <tr>
        <td>10</td>
        <td>Time-Series FastAPI</td>
        <td>ARQ Redis Queue</td>
        <td>ARQ Protocol<br><code>:6379</code> Queue <code>arq:queue</code></td>
        <td><strong>เหตุผล:</strong> API ผลักดันงานพยากรณ์ลง Message Queue ใน Redis ป้องกัน API Block<br><strong>ข้อมูล:</strong> Task Payload ระบุชื่อฟังก์ชัน <code>process_timeseries_forecast</code> และ Tuple Arguments</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>กลยุทธ์ Reconnection Pool อัตโนมัติเมื่อ Redis หลุด</td>
      </tr>
      <tr>
        <td>11</td>
        <td>ARQ Redis Queue</td>
        <td>Time-Series ARQ Worker</td>
        <td>ARQ Event Loop<br>Internal Queue Listener</td>
        <td><strong>เหตุผล:</strong> Worker เฝ้ารอดึงงานพยากรณ์อนุกรมเวลาจากคิว Redis ไปคำนวณ<br><strong>ข้อมูล:</strong> Tuple Arguments สำหรับงานพยากรณ์เซนเซอร์</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ระบบ Automatic Retry สูงสุด 3 ครั้งเมื่อคำนวณล้มเหลว</td>
      </tr>
      <tr>
        <td>12</td>
        <td>Time-Series ARQ Worker</td>
        <td>MinIO Storage Container</td>
        <td>S3 Protocol / SDK<br><code>:9000</code></td>
        <td><strong>เหตุผล:</strong> Worker บันทึกผลลัพธ์พยากรณ์ (Prophet/LSTM) ในรูปแบบ JSON ลง MinIO<br><strong>ข้อมูล:</strong> JSON Document ผลพยากรณ์ไปยัง Bucket <code>timeseries-predictions</code> Key <code>forecasts/...</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>พิมพ์ Error Log และคืนค่า S3 Key เป็น <code>None</code> หากเขียนไม่สำเร็จ</td>
      </tr>
      <tr>
        <td>13</td>
        <td>Time-Series ARQ Worker</td>
        <td>Redis Cache Store</td>
        <td>redis-py async<br><code>:6379</code></td>
        <td><strong>เหตุผล:</strong> Worker อัปเดตผลพยากรณ์ล่าสุดลง Redis Cache ให้ API อ่านได้ทันที<br><strong>ข้อมูล:</strong> Forecast Results Dict ภายใต้ Key <code>forecast:latest:{sensor_id}</code> (TTL 3,600s)</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ดักจับ Silent Exception เพื่อไม่ให้กระทบการบันทึก S3</td>
      </tr>
      <tr>
        <td>14</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/jobs/{job_id}</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้เรียกสอบถามสถานะและผลลัพธ์ของ Background Job<br><strong>ข้อมูล:</strong> Path Parameter <code>job_id</code>, ตอบกลับด้วย JSON Status (queued, in_progress, complete)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>คืนค่า <code>JobStatus.deferred / queued / complete</code></td>
      </tr>
      <tr>
        <td>15</td>
        <td>Time-Series FastAPI</td>
        <td>ARQ Redis Queue</td>
        <td>ARQ Protocol<br><code>:6379</code></td>
        <td><strong>เหตุผล:</strong> API อ่านสถานะงานจากคลังข้อมูล ARQ Job Metadata ใน Redis<br><strong>ข้อมูล:</strong> คำสั่ง Query <code>Job(job_id).status()</code> และดึง Result Payload</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ส่งคืนผลลัพธ์ <code>null</code> หากเกินระยะเวลา Timeout ของ Job</td>
      </tr>
      <tr>
        <td>16</td>
        <td>Client Web Browser</td>
        <td>Time-Series FastAPI</td>
        <td>HTTP REST<br><code>:8000/api/v1/analytics/train</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งฝึกฝนโมเดล AI พยากรณ์ (Prophet/LSTM Training Job)<br><strong>ข้อมูล:</strong> JSON Body <code>TrainJobRequest</code> (ระบุ <code>dataset_id</code>, <code>model_type</code>, <code>epochs</code>)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>Enqueue งานฝึกฝนโมเดลลง ARQ Redis Queue</td>
      </tr>
      <tr>
        <td>17</td>
        <td>Time-Series ARQ Worker</td>
        <td>MinIO Storage Container</td>
        <td>S3 Protocol<br><code>:9000</code></td>
        <td><strong>เหตุผล:</strong> Worker บันทึกไฟล์น้ำหนักโมเดล (Model Checkpoint) ที่เทรนเสร็จสมบูรณ์<br><strong>ข้อมูล:</strong> PyTorch Model Binary (<code>.pt</code>) / JSON Metadata ไปยัง Bucket <code>model-checkpoints</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>สร้าง Bucket <code>model-checkpoints</code> อัตโนมัติ</td>
      </tr>
      <tr>
        <td>18</td>
        <td>Client Web Browser</td>
        <td>Non-Time-Series API</td>
        <td>HTTP Multipart<br><code>:8001/api/v1/store/upload-image</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้อัปโหลดไฟล์รูปภาพทั่วไปเข้าสู่ระบบคอมพิวเตอร์วิชัน<br><strong>ข้อมูล:</strong> Binary Image File Stream (JPEG/PNG) และ Form Field <code>image_id</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>สลับใช้ Mock Binary Stream หากไฟล์อัปโหลดว่างเปล่า</td>
      </tr>
      <tr>
        <td>19</td>
        <td>Non-Time-Series API</td>
        <td>MinIO Storage Container</td>
        <td>S3 Protocol / SDK<br><code>:9000</code></td>
        <td><strong>เหตุผล:</strong> API บันทึกไฟล์รูปภาพดิบลงใน Object Storage<br><strong>ข้อมูล:</strong> Image Binary Stream ไปยัง Bucket <code>general-images</code> Key <code>uploads/...</code> พร้อมสร้าง Presigned URL</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>สร้าง Presigned GET URL อายุ 3,600 วินาทีสำหรับแสดงผลหน้า UI</td>
      </tr>
      <tr>
        <td>20</td>
        <td>Non-Time-Series API</td>
        <td>Redis Cache Store</td>
        <td>redis-py async<br><code>:6379</code></td>
        <td><strong>เหตุผล:</strong> API บันทึกข้อมูลอธิบายรูปภาพ (Metadata) ลงใน Cache<br><strong>ข้อมูล:</strong> Image Meta Dict JSON (ชื่อไฟล์ ขนาด ประเภท MIME) Key <code>image:meta:{image_id}</code> (TTL 86,400s)</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>Automatic Connection Pool Reconnect</td>
      </tr>
      <tr>
        <td>21</td>
        <td>Client Web Browser</td>
        <td>Non-Time-Series API</td>
        <td>HTTP REST<br><code>:8001/api/v1/ls/create-project</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งสร้างโปรเจกต์ติดแท็กภาพคอมพิวเตอร์วิชันใน Label Studio<br><strong>ข้อมูล:</strong> JSON Body <code>VisionLabelStudioProjectRequest</code> (ชื่อโปรเจกต์ และคำอธิบาย)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>Fallback สู่ Mock Project ID 202 หากเชื่อมต่อไม่ได้</td>
      </tr>
      <tr>
        <td>22</td>
        <td>Non-Time-Series API</td>
        <td>Label Studio Container</td>
        <td>HTTP REST / httpx<br><code>:8080/api/projects/</code></td>
        <td><strong>เหตุผล:</strong> API สั่งสร้างโปรเจกต์ Vision ใน Label Studio ผ่าน REST API<br><strong>ข้อมูล:</strong> XML RectangleLabels Configuration Payload สำหรับวาด Bounding Box บนภาพ</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ดักจับ <code>httpx.RequestError</code> แล้วใช้ Fallback Response</td>
      </tr>
      <tr>
        <td>23</td>
        <td>Client Web Browser</td>
        <td>Non-Time-Series API</td>
        <td>HTTP REST<br><code>:8001/api/v1/jobs/inference</code></td>
        <td><strong>เหตุผล:</strong> ผู้ใช้สั่งรันโมเดลประมวลผลตรวจจับวัตถุบนรูปภาพแบบเบื้องหลัง<br><strong>ข้อมูล:</strong> JSON Body <code>InferenceJobRequest</code> (ระบุ <code>image_id</code>, <code>image_bucket</code>, <code>object_key</code>)</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>HTTP 500 หากส่งงานเข้า ARQ Queue ไม่สำเร็จ</td>
      </tr>
      <tr>
        <td>24</td>
        <td>Non-Time-Series API</td>
        <td>ARQ Redis Queue</td>
        <td>ARQ Protocol<br><code>:6379</code> Queue <code>arq:queue</code></td>
        <td><strong>เหตุผล:</strong> API ผลักดันงาน Vision Inference ลงใน ARQ Queue บน Redis<br><strong>ข้อมูล:</strong> Task Specification ระบุฟังก์ชัน <code>process_image_inference</code> และ Image Credentials</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>Pool Reconnection Strategy</td>
      </tr>
      <tr>
        <td>25</td>
        <td>ARQ Redis Queue</td>
        <td>Non-Time-Series ARQ Worker</td>
        <td>ARQ Event Loop<br>Internal Queue Listener</td>
        <td><strong>เหตุผล:</strong> Vision Worker ดึงงานตรวจจับภาพจากคิว Redis ไปประมวลผลผ่าน ResNet-18<br><strong>ข้อมูล:</strong> Image Job Arguments Tuple</td>
        <td><span class="badge badge-async">Async</span></td>
        <td>ระบบ Automatic Task Retry (สูงสุด 3 ครั้ง)</td>
      </tr>
      <tr>
        <td>26</td>
        <td>Non-Time-Series ARQ Worker</td>
        <td>MinIO Storage Container</td>
        <td>S3 Protocol / SDK<br><code>:9000</code></td>
        <td><strong>เหตุผล:</strong> Vision Worker บันทึกผลการวิเคราะห์ภาพ (Bounding Box, Confidence) ลง MinIO<br><strong>ข้อมูล:</strong> ResNet-18 Inference Result JSON ไปยัง Bucket <code>vision-results</code> Key <code>results/...</code></td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>พิมพ์ Error Log และกำหนด S3 Key เป็น <code>None</code> หากล้มเหลว</td>
      </tr>
      <tr>
        <td>27</td>
        <td>Label Studio Container</td>
        <td>PostgreSQL Database</td>
        <td>PostgreSQL Wire Protocol<br><code>:5432</code> Database <code>ai_ecosystem</code></td>
        <td><strong>เหตุผล:</strong> Label Studio บันทึกข้อมูลผังโปรเจกต์ ผู้ใช้ งาน และ Annotation ทั้งหมดลงฐานข้อมูลหลัก<br><strong>ข้อมูล:</strong> SQL Transactions สำหรับตารางผู้ใช้, โปรเจกต์, Data Tasks และ Annotation Geometries</td>
        <td><span class="badge badge-sync">Sync</span></td>
        <td>PostgreSQL Healthcheck & Docker Volume Persistence (<code>postgresql-data</code>)</td>
      </tr>
    </tbody>
  </table>

  <!-- SUMMARY CALLOUT -->
  <div style="background-color: #ecfdf5; border: 1px solid #a7f3d0; border-left: 4px solid #10b981; border-radius: 6px; padding: 14px 18px; margin-top: 20px;">
    <div style="font-size: 11pt; font-weight: 600; color: #065f46; margin-bottom: 6px;">✓ สรุปการตรวจสอบและรับรองระบบ (System Verification Checklist)</div>
    <ul style="color: #047857; margin-bottom: 0; padding-left: 18px;">
      <li>✓ คำอธิบายทุกองค์ประกอบครอบคลุมทั้ง 4 ด้าน: What it is, Why it is used, How it works, Inputs/Outputs</li>
      <li>✓ อธิบาย FastAPI ไมโครเซอร์วิสทั้ง 2 ตัว (<code>apps/time_series</code>, <code>apps/non_time_series</code>) ครบถ้วน</li>
      <li>✓ อธิบาย Shared Libraries ทั้ง 4 โมดูล (MinIO, Redis, ARQ, Label Studio) เชิงลึก</li>
      <li>✓ อธิบาย ARQ Workers ทั้ง 2 สายงาน (Time-Series และ Vision) ละเอียด</li>
      <li>✓ อธิบายหลักการทำงานจริง สมการคณิตศาสตร์ และ Input/Output ของ AI/ML Algorithms ทั้ง 3 ตัว (Facebook Prophet, PyTorch LSTM, PyTorch ResNet-18)</li>
      <li>✓ อธิบายบทบาทและการทำงานของ Infrastructure Containers ทั้ง 4 ตัว (PostgreSQL, Redis, MinIO, Label Studio)</li>
      <li>✓ อธิบายจุดเชื่อมต่อใน draw.io Connection Matrix แบบละเอียดทีละเส้นเรียงตั้งแต่เส้นที่ 1 ถึง 27 สมบูรณ์ 100%</li>
    </ul>
  </div>

</body>
</html>
"""
    return html

def build_pdf():
    print("==================================================")
    print("Generating HTML content for Ultra-Detailed Architecture Report...")
    print("==================================================")

    html_content = generate_html_content()
    
    # Write temp HTML file
    os.makedirs(os.path.dirname(HTML_TEMP_PATH), exist_ok=True)
    with open(HTML_TEMP_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML file created at: {HTML_TEMP_PATH}")
    
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_path):
        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

    print(f"Using Microsoft Edge at: {edge_path}")
    print(f"Target PDF Output: {PDF_OUTPUT_PATH}")

    # Run Edge Headless Print to PDF
    file_uri = f"file:///{HTML_TEMP_PATH.replace('\\', '/')}"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PDF_OUTPUT_PATH}",
        "--no-pdf-header-footer",
        file_uri
    ]
    
    print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(PDF_OUTPUT_PATH):
        file_size = os.path.getsize(PDF_OUTPUT_PATH)
        print(f"SUCCESS: PDF created at {PDF_OUTPUT_PATH} (Size: {file_size} bytes)")
    else:
        print(f"ERROR: Failed to generate PDF. Stdout: {result.stdout}, Stderr: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    build_pdf()
