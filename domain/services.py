from domain.models import Department
from domain.ports import DepartmentRepositoryPort
from adapters.storage.azure_blob_client import AzureBlobClient

async def process_departments_csv(repo: DepartmentRepositoryPort, blob_client: AzureBlobClient, blob_name: str):
    rows = blob_client.download_csv(blob_name)
    departments = [Department(id=int(r[0]), department=r[1]) for r in rows]
    return await repo.insert_departments(departments)
