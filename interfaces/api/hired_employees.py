from fastapi import APIRouter, Query
from adapters.storage.azure_blob_client import AzureBlobClient
import os
from redis import Redis
from rq import Queue

router = APIRouter()

@router.post("/process/hired_employees")
def process_hired_employees(start: int = Query(0), limit: int = Query(1000)):
    blob_client = AzureBlobClient()
    rows = blob_client.download_csv("hired_employees.csv")
    subset = rows[start:start+limit]

    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    q = Queue(connection=redis_conn)

    job = q.enqueue(
        "application.tasks.process_hired_employees_batch",
        subset,
        job_timeout=600  # segundos = 10 minutos
    )

    return {"message": "Batch enqueued.", "task_id": job.id, "start": start, "limit": limit}
