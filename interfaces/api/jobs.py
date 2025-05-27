from fastapi import APIRouter, BackgroundTasks
from application.background import run_jobs_processing

router = APIRouter()

@router.post("/process/jobs")
async def process_jobs(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_jobs_processing)
    return {"message": "Jobs processing started in the background."}
