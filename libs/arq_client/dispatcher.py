"""
ARQ Task Dispatcher Client Library
Provides helper class TaskDispatcher for enqueuing async background tasks into ARQ Redis queues and tracking job execution status.
"""

import os
from typing import Any, Dict, Optional
from arq.connections import RedisSettings, ArqRedis, create_pool
from arq.jobs import Job, JobStatus


class TaskDispatcher:
    """
    ARQ Task Dispatcher for enqueuing background tasks and querying job execution states.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None,
        database: int = 0,
    ):
        """
        Initialize RedisSettings for ARQ connection.
        """
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port or int(os.getenv("REDIS_PORT", 6379))
        self.password = password or os.getenv("REDIS_PASSWORD", None)
        self.database = database

        self.redis_settings = RedisSettings(
            host=self.host,
            port=self.port,
            password=self.password,
            database=self.database,
        )
        self._pool: Optional[ArqRedis] = None

    async def get_pool(self) -> ArqRedis:
        """
        Get or create ARQ Redis pool instance.
        """
        if self._pool is None:
            self._pool = await create_pool(self.redis_settings)
        return self._pool

    async def enqueue_job(
        self,
        function_name: str,
        *args: Any,
        _job_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Enqueue a task by name into ARQ queue. Returns dict with job_id and status.
        """
        pool = await self.get_pool()
        job: Optional[Job] = await pool.enqueue_job(
            function_name, *args, _job_id=_job_id, **kwargs
        )
        if job:
            return {
                "job_id": job.job_id,
                "function": function_name,
                "status": "queued",
            }
        return None

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Query status and result of a job by job_id.
        """
        pool = await self.get_pool()
        job = Job(job_id, pool)
        status = await job.status()

        result = None
        if status == JobStatus.complete:
            try:
                info = await job.result_info()
                result = info.result if info else None
            except Exception as e:
                result = f"Error retrieving result: {e}"

        return {
            "job_id": job_id,
            "status": status.value if hasattr(status, "value") else str(status),
            "result": result,
        }

    async def close(self):
        """
        Close active ARQ Redis pool connection.
        """
        if self._pool:
            await self._pool.aclose()
            self._pool = None
