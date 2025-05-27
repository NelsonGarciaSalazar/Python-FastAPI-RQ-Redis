from fastapi import APIRouter
from redis import Redis
from rq.job import Job
import os

router = APIRouter()

@router.get("/tasks/{task_id}/status")
def get_task_status(task_id: str):
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    try:
        job = Job.fetch(task_id, connection=redis_conn)
        return {
            "id": job.id,
            "status": job.get_status(),
            "result": job.return_value() if job.is_finished else None
        }
    except Exception as e:
        return {"error": str(e)}
