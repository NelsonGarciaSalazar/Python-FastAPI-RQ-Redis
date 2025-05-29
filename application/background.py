from domain.services import process_jobs_csv
from adapters.db.job_repository import JobRepository
from adapters.storage.azure_blob_client import AzureBlobClient

async def run_jobs_processing():
    blob_client = AzureBlobClient()
    repo = JobRepository()
    return await process_jobs_csv(repo, blob_client, "jobs.csv")

def process_hired_employees_batch(batch_rows: list) -> None:
    import asyncio
    from adapters.db.hired_employee_repository import HiredEmployeeRepository

    async def _run():
        employees = []
        error_ids = []

        for r in batch_rows:
            try:
                employees.append({
                    "id": int(r[0]),
                    "name": r[1],
                    "datetime": r[2],
                    "department_id": int(r[3]),
                    "job_id": int(r[4])
                })
            except (ValueError, IndexError):
                try:
                    error_ids.append(int(r[0]))
                except:
                    continue

        repo = HiredEmployeeRepository()
        result = await repo.insert_hired_employees(employees)
        result["hired_employees"]["error_ids"] = error_ids
        result["hired_employees"]["errors"] = len(error_ids) + result["hired_employees"].get("errors", 0)
        result["hired_employees"]["processed"] = len(batch_rows)

    asyncio.run(_run())

