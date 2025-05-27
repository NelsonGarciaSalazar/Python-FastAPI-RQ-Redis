from domain.models import Department
from domain.ports import DepartmentRepositoryPort
from domain.models import Job
from domain.ports import JobRepositoryPort
from domain.models import HiredEmployee
from adapters.storage.azure_blob_client import AzureBlobClient
from typing import List

async def process_departments_csv(repo: DepartmentRepositoryPort, blob_client: AzureBlobClient, blob_name: str):
    rows = blob_client.download_csv(blob_name)
    departments = [Department(id=int(r[0]), department=r[1]) for r in rows]
    return await repo.insert_departments(departments)

async def process_jobs_csv(repo: JobRepositoryPort, blob_client: AzureBlobClient, blob_name: str):
    rows = blob_client.download_csv(blob_name)
    jobs = [Job(id=int(r[0]), job=r[1]) for r in rows]
    return await repo.insert_jobs(jobs)

def split_batches(rows: list, batch_size: int):
    for i in range(0, len(rows), batch_size):
        yield rows[i:i+batch_size]

def map_to_hired_employees(rows: list) -> List[HiredEmployee]:
    employees = []
    for r in rows:
        try:
            employees.append(HiredEmployee(
                id=int(r[0]),
                name=r[1],
                datetime=r[2],
                department_id=int(r[3]),
                job_id=int(r[4])
            ))
        except (ValueError, IndexError) as e:
            continue  # Skip malformed row
    return employees
