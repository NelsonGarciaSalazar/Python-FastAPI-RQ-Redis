from domain.services import process_jobs_csv
from adapters.db.job_repository import JobRepository
from adapters.storage.azure_blob_client import AzureBlobClient

async def run_jobs_processing():
    blob_client = AzureBlobClient()
    repo = JobRepository()
    return await process_jobs_csv(repo, blob_client, "jobs.csv")
