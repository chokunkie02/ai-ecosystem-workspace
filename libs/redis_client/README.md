# Redis Cache Client Library (`libs/redis_client`)

> [!NOTE]
> ไลบรารีส่วนกลางสำหรับจัดการการเชื่อมต่อ Caching และ In-Memory Data Store ด้วย Redis

## บทบาทและหน้าที่ (Responsibilities)
`libs/redis_client` ให้บริการการทำ Caching ความเร็วสูง และจัดเก็บสถานะการทำงานชั่วคราว (State & Session Store) ให้กับบริการย่อยทั้งหมดใน Monorepo เพื่อลดภาระการค้นหาข้อมูลซ้ำซ้อนจาก PostgreSQL หรือ MinIO

## Environment Variables

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `REDIS_HOST` | `localhost` | Host สำหรับเชื่อมต่อ Redis server |
| `REDIS_PORT` | `6379` | Port สำหรับเชื่อมต่อ Redis server |
| `REDIS_PASSWORD` | `None` | รหัสผ่านในการเข้าถึง Redis (ถ้ามี) |
| `REDIS_DB` | `0` | Database Index สำหรับ Redis cache |

## Developer Job (ภาระงานของนักพัฒนา)
1. **Connection Pool Management**: เชื่อมต่อแบบ Redis Connection Pool ที่เสถียรรองรับการทำงานแบบ Asynchronous (`redis.asyncio`)
2. **Key-Value & JSON Cache**: จัดเก็บและดึงข้อมูล String/JSON ด้วย `set` และ `get` พร้อมรองรับ TTL
3. **Redis Hash Operations**: เก็บและอ่านข้อมูลรูปแบบ Hash ด้วย `set_hash` และ `get_hash`
4. **Key Management**: ตรวจสอบการมีอยู่ (`exists`), ค้นหา Key (`list_keys`) และลบข้อมูล (`delete`)

## โครงสร้างไดเรกทอรี
```text
libs/redis_client/
├── README.md               # เอกสารอธิบายการใช้งาน Redis Client
├── __init__.py             # Module Initializer
└── client.py               # RedisCacheManager implementation
```

## วิธีการรัน (Docker & Tests)

```bash
# สตาร์ท Redis Container
docker compose up -d redis

# การรัน Unit / Integration Tests
pytest libs/redis_client/tests/
```

## ตัวอย่างการใช้งาน (Usage Example)

```python
import asyncio
from libs.redis_client.client import RedisCacheManager

async def main():
    # 1. Initialize Redis Cache Manager
    redis_mgr = RedisCacheManager(key_prefix="app:")

    # 2. Set key พร้อม JSON payload และกำหนดเวลาหมดอายุ (expire_seconds)
    await redis_mgr.set(
        key="task:status:12345",
        value={"status": "PROCESSING", "progress": 45},
        expire_seconds=3600
    )

    # 3. Get key (ถอดรหัส JSON อัตโนมัติ)
    status_data = await redis_mgr.get("task:status:12345")
    print(f"Task Status: {status_data}")

    # 4. Hash Operations
    await redis_mgr.set_hash("user:session:99", {"username": "admin", "role": "operator"})
    session = await redis_mgr.get_hash("user:session:99")
    print(f"User Session: {session}")

    # 5. ปิด Connection
    await redis_mgr.close()

if __name__ == "__main__":
    asyncio.run(main())
```
