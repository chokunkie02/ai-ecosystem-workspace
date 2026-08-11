"""
MinIO Object Storage Manager Client Library
Provides helper class MinIOManager for S3 bucket management, object uploads/downloads, and presigned URLs.
"""

import io
import os
from datetime import timedelta
from typing import Optional, Union, List, BinaryIO
from minio import Minio
from minio.error import S3Error


class MinIOManager:
    """
    MinIO Object Storage Manager for handling buckets, file transfers, and presigned URLs.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        secure: Optional[bool] = None,
    ):
        """
        Initialize MinIO Client from arguments or environment variables.
        """
        self.endpoint = endpoint or os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.access_key = access_key or os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = secret_key or os.getenv("MINIO_SECRET_KEY", "minioadmin")
        
        if secure is None:
            secure_env = os.getenv("MINIO_SECURE", "false").lower()
            self.secure = secure_env in ("true", "1", "yes")
        else:
            self.secure = secure

        self.client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure,
        )

    def ensure_bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if bucket exists; if not, create it.
        Returns True if bucket exists or was created successfully.
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            return True
        except S3Error as err:
            print(f"[MinIOManager] Error ensuring bucket {bucket_name}: {err}")
            return False

    def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file_data: Union[str, bytes, BinaryIO],
        content_type: str = "application/octet-stream",
    ) -> str:
        """
        Upload string, bytes, or file-like object to specified bucket.
        """
        self.ensure_bucket_exists(bucket_name)

        if isinstance(file_data, str):
            # If string is a valid existing local file path, upload from file path
            if os.path.isfile(file_data):
                self.client.fput_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    file_path=file_data,
                    content_type=content_type,
                )
                return f"{bucket_name}/{object_name}"
            else:
                data_bytes = file_data.encode("utf-8")
                stream = io.BytesIO(data_bytes)
                length = len(data_bytes)
        elif isinstance(file_data, bytes):
            stream = io.BytesIO(file_data)
            length = len(file_data)
        elif hasattr(file_data, "read"):
            # Binary stream
            file_data.seek(0, os.SEEK_END)
            length = file_data.tell()
            file_data.seek(0)
            stream = file_data
        else:
            raise ValueError("Unsupported file_data type. Must be file path, bytes, or stream.")

        self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=stream,
            length=length,
            content_type=content_type,
        )
        return f"{bucket_name}/{object_name}"

    def download_file(
        self, bucket_name: str, object_name: str, destination_path: Optional[str] = None
    ) -> bytes:
        """
        Download an object from bucket. If destination_path is provided, writes to file.
        Returns the object bytes.
        """
        response = None
        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            if destination_path:
                os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
                with open(destination_path, "wb") as f:
                    f.write(data)
            return data
        finally:
            if response:
                response.close()
                response.release_conn()

    def get_presigned_url(
        self, bucket_name: str, object_name: str, expires_seconds: int = 3600
    ) -> str:
        """
        Generate a presigned GET URL for downloading an object.
        """
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(seconds=expires_seconds),
        )
        return url

    def list_objects(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        List all object names in specified bucket with optional prefix filter.
        """
        if not self.client.bucket_exists(bucket_name):
            return []
        objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]

    def delete_object(self, bucket_name: str, object_name: str) -> bool:
        """
        Delete object from bucket.
        """
        try:
            self.client.remove_object(bucket_name, object_name)
            return True
        except S3Error as err:
            print(f"[MinIOManager] Error deleting object {object_name}: {err}")
            return False
