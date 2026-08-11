"""
Redis Caching & State Manager Client Library
Provides helper class RedisCacheManager for asynchronous cache getting/setting, TTL management, and JSON payload handling.
"""

import json
import os
from typing import Any, Optional, Dict, List
import redis.asyncio as aioredis


class RedisCacheManager:
    """
    Async Redis Cache Manager for handling connection pooling, key-value storage, and JSON serialization.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: int = 0,
        password: Optional[str] = None,
        key_prefix: str = "app:",
    ):
        """
        Initialize Redis Async Client settings.
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.db = db
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.key_prefix = key_prefix
        self._redis: Optional[aioredis.Redis] = None

    async def get_client(self) -> aioredis.Redis:
        """
        Get or initialize active Redis connection.
        """
        if self._redis is None:
            self._redis = aioredis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,
            )
        return self._redis

    def _format_key(self, key: str) -> str:
        """
        Apply prefix to key if not already prefixed.
        """
        if self.key_prefix and not key.startswith(self.key_prefix):
            return f"{self.key_prefix}{key}"
        return key

    async def set(
        self, key: str, value: Any, expire_seconds: Optional[int] = None
    ) -> bool:
        """
        Set key with optional expiration TTL in seconds. Serializes dicts/lists to JSON strings.
        """
        client = await self.get_client()
        full_key = self._format_key(key)

        if isinstance(value, (dict, list)):
            encoded_value = json.dumps(value)
        else:
            encoded_value = str(value)

        if expire_seconds:
            await client.setex(full_key, expire_seconds, encoded_value)
        else:
            await client.set(full_key, encoded_value)
        return True

    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get key value from Redis. Decodes JSON string automatically if valid JSON structure.
        """
        client = await self.get_client()
        full_key = self._format_key(key)
        raw_val = await client.get(full_key)

        if raw_val is None:
            return default

        try:
            return json.loads(raw_val)
        except (json.JSONDecodeError, TypeError):
            return raw_val

    async def delete(self, key: str) -> bool:
        """
        Delete key from Redis cache.
        """
        client = await self.get_client()
        full_key = self._format_key(key)
        res = await client.delete(full_key)
        return res > 0

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis cache.
        """
        client = await self.get_client()
        full_key = self._format_key(key)
        count = await client.exists(full_key)
        return count > 0

    async def set_hash(self, name: str, mapping: Dict[str, Any]) -> bool:
        """
        Set fields in a Redis Hash.
        """
        client = await self.get_client()
        full_key = self._format_key(name)
        serialized_mapping = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
            for k, v in mapping.items()
        }
        await client.hset(full_key, mapping=serialized_mapping)
        return True

    async def get_hash(self, name: str) -> Dict[str, Any]:
        """
        Get all fields from a Redis Hash.
        """
        client = await self.get_client()
        full_key = self._format_key(name)
        raw_dict = await client.hgetall(full_key)
        
        result = {}
        for k, v in raw_dict.items():
            try:
                result[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                result[k] = v
        return result

    async def list_keys(self, pattern: str = "*") -> List[str]:
        """
        List keys matching pattern.
        """
        client = await self.get_client()
        full_pattern = self._format_key(pattern)
        return await client.keys(full_pattern)

    async def close(self):
        """
        Close active Redis connection.
        """
        if self._redis:
            await self._redis.aclose()
            self._redis = None
