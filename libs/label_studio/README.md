# Label Studio Integration Library (`libs/label_studio`)

> [!NOTE]
> ไลบรารีส่วนกลางสำหรับเชื่อมต่อ จัดการ และซิงก์ข้อมูลกับ Label Studio (Data Annotation Platform)

## บทบาทและหน้าที่ (Responsibilities)
`libs/label_studio` ทำหน้าที่เป็น SDK Client Wrapper สำหรับสื่อสารกับ **Label Studio API** เพื่อสนับสนุนกระบวนการกำกับแท็กข้อมูล (Data Labeling / Annotation) ทั้งรูปภาพ (X-Ray Classification / Object Detection) และข้อมูลอนุกรมเวลา (Anomaly Detection)

## Environment Variables

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `LABEL_STUDIO_URL` | `http://localhost:8080` | Host URL สำหรับเชื่อมต่อ Label Studio Instance |
| `LABEL_STUDIO_API_KEY` | `""` | User Access Token สำหรับยืนยันตัวตนกับ Label Studio API |

## Developer Job (ภาระงานของนักพัฒนา)
1. **Project Management**: สร้างและดึงข้อมูล Project ด้วย `create_project`, `get_projects` และ `get_project`
2. **Task Import Pipeline**: นำเข้าข้อมูลรูปภาพหรือข้อความเพื่อทำ Annotation ด้วย `import_tasks`
3. **Task Retrieval**: ดึงผลการ Label / Annotation ด้วย `get_tasks`
4. **Cloud Storage Sync**: ซิงก์ข้อมูลกับ Cloud Storage / MinIO S3 ด้วย `sync_data`

## โครงสร้างไดเรกทอรี
```text
libs/label_studio/
├── README.md               # เอกสารอธิบายการใช้งาน Label Studio Integration
├── __init__.py             # Module Initializer
└── connector.py            # LabelStudioConnector implementation
```

## วิธีการรัน (Docker & Tests)

```bash
# สตาร์ท Label Studio Container
docker compose up -d label-studio

# การรัน Unit / Integration Tests
pytest libs/label_studio/tests/
```

## ตัวอย่างการใช้งาน (Usage Example)

```python
import asyncio
from libs.label_studio.connector import LabelStudioConnector

async def main():
    # 1. Initialize Label Studio Connector
    connector = LabelStudioConnector()

    # 2. สร้าง Project สำหรับการ Annotation
    project = await connector.create_project(
        title="Medical Image Classification",
        description="Dataset annotation for X-ray images"
    )
    project_id = project["id"]
    print(f"Created Project ID: {project_id}")

    # 3. นำเข้า Task สำหรับการ Label
    tasks = [
        {"data": {"image": "http://localhost:9000/general-images/xray_01.jpg"}},
        {"data": {"image": "http://localhost:9000/general-images/xray_02.jpg"}}
    ]
    imported = await connector.import_tasks(project_id, tasks)
    print(f"Imported Tasks: {imported}")

    # 4. ดึงข้อมูล Tasks และ Annotations ของ Project
    all_tasks = await connector.get_tasks(project_id)
    print(f"Project Tasks Count: {len(all_tasks)}")

if __name__ == "__main__":
    asyncio.run(main())
```
