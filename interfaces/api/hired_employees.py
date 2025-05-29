import os
from redis import Redis
from rq import Queue
from fastapi import APIRouter, Query, BackgroundTasks
from adapters.storage.azure_blob_client import AzureBlobClient
from application.tasks import process_hired_employees_batch

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

@router.post("/process/hired_employees/v2")
async def process_hired_employees_v2(
    background_tasks: BackgroundTasks,
    start: int = Query(0),
    limit: int = Query(1000)
):
    blob_client = AzureBlobClient()
    rows = blob_client.download_csv("hired_employees.csv")
    subset = rows[start:start+limit]

    background_tasks.add_task(process_hired_employees_batch, subset)

    return {
        "message": "Batch started in background.",
        "start": start,
        "limit": limit
    }