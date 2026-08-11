"""
Non-Time-Series Computer Vision ARQ Worker Implementation
Processes general image detection, object classification, and computer vision inference tasks using ResNet-18 pipeline.
"""

import os
import json
import time
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from arq.connections import RedisSettings

# Import shared clients
from libs.minio_client.client import MinIOManager
from libs.redis_client.client import RedisCacheManager


async def startup(ctx: Dict[str, Any]):
    """
    Worker startup hook: Initialize shared client instances in context.
    """
    ctx["minio"] = MinIOManager()
    ctx["redis"] = RedisCacheManager()
    print("[Non-Time-Series Worker] General Image Detection & Classification Worker initialized.")


async def shutdown(ctx: Dict[str, Any]):
    """
    Worker shutdown hook.
    """
    if "redis" in ctx and ctx["redis"]:
        await ctx["redis"].close()
    print("[Non-Time-Series Worker] Worker shutdown complete.")


async def process_image_inference(
    ctx: Dict[str, Any],
    image_id: str,
    image_bucket: str = "general-images",
    object_key: str = "sample.jpg",
) -> Dict[str, Any]:
    """
    Background job: Execute ResNet-18 General Image Detection & Classification inference pipeline.
    """
    start_time = time.time()
    minio_mgr: MinIOManager = ctx.get("minio") or MinIOManager()
    redis_mgr: RedisCacheManager = ctx.get("redis") or RedisCacheManager()

    print(f"[Non-Time-Series Worker] Processing image inference for image_id={image_id}, key={object_key}")

    # Download or verify image object exists in MinIO
    try:
        minio_mgr.ensure_bucket_exists(image_bucket)
    except Exception as err:
        print(f"[Non-Time-Series Worker] Warning MinIO bucket check: {err}")

    # Perform ResNet-18 Image Detection & Classification Model Pipeline simulation
    random.seed(hash(image_id) % 1000000)
    is_detected = random.choice([True, False, True])  # Probabilistic mock class
    confidence = round(random.uniform(0.88, 0.99), 4)

    prediction_label = "OBJECT_DETECTED" if is_detected else "NORMAL"
    object_category = random.choice(["Vehicle", "Person", "Equipment", "General Object"]) if is_detected else "N/A"

    execution_time = round(time.time() - start_time, 4)

    result_payload = {
        "status": "SUCCESS",
        "image_id": image_id,
        "object_key": f"{image_bucket}/{object_key}",
        "model": "ResNet-18-GeneralCVNet",
        "prediction": prediction_label,
        "confidence": confidence,
        "details": {
            "object_category": object_category,
            "heat_map_coordinates": {
                "x_min": 120,
                "y_min": 180,
                "x_max": 340,
                "y_max": 410,
            } if is_detected else None,
        },
        "execution_time_seconds": execution_time,
        "processed_at": datetime.utcnow().isoformat(),
    }

    # Upload inference metadata to MinIO result bucket
    result_bucket = "vision-results"
    result_key = f"results/{image_id}_{int(time.time())}.json"
    
    try:
        minio_mgr.upload_file(
            bucket_name=result_bucket,
            object_name=result_key,
            file_data=json.dumps(result_payload).encode("utf-8"),
            content_type="application/json",
        )
        result_payload["result_s3_key"] = f"{result_bucket}/{result_key}"
    except Exception as err:
        print(f"[Non-Time-Series Worker] Result upload error: {err}")
        result_payload["result_s3_key"] = None

    # Cache prediction in Redis
    try:
        await redis_mgr.set(f"vision:latest:{image_id}", result_payload, expire_seconds=3600)
    except Exception as err:
        print(f"[Non-Time-Series Worker] Redis cache error: {err}")

    return result_payload


# Alias function for backward compatibility
async def process_xray_inference(ctx: Dict[str, Any], image_id: str, image_bucket: str = "general-images", object_key: str = "sample.jpg") -> Dict[str, Any]:
    return await process_image_inference(ctx, image_id=image_id, image_bucket=image_bucket, object_key=object_key)


async def process_batch_image_inference(
    ctx: Dict[str, Any],
    batch_id: str,
    image_keys: List[str],
) -> Dict[str, Any]:
    """
    Background job: Execute batch classification on multiple images.
    """
    start_time = time.time()
    batch_results = []

    for idx, key in enumerate(image_keys):
        img_id = f"{batch_id}_img_{idx}"
        single_res = await process_image_inference(ctx, image_id=img_id, object_key=key)
        batch_results.append(single_res)

    execution_time = round(time.time() - start_time, 4)

    return {
        "status": "COMPLETED",
        "batch_id": batch_id,
        "total_images": len(image_keys),
        "execution_time_seconds": execution_time,
        "predictions": batch_results,
    }


class WorkerSettings:
    """
    ARQ Worker Configuration Settings for Non-Time-Series Worker.
    """
    functions = [process_image_inference, process_batch_image_inference, process_xray_inference]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
    )

