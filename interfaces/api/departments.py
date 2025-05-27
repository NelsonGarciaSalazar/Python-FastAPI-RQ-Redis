from fastapi import APIRouter
from adapters.db.department_repository import DepartmentRepository
from adapters.storage.azure_blob_client import AzureBlobClient
from domain.services import process_departments_csv

router = APIRouter()

@router.post("/process/departments")
async def process_departments():
    blob_client = AzureBlobClient()
    repo = DepartmentRepository()
    result = await process_departments_csv(repo, blob_client, "departments.csv")
    return result
