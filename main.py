from fastapi import FastAPI
from interfaces.api import departments
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="HR Processing API",
    description="Processes HR CSVs into Azure SQL",
    version="1.0"
)

app.include_router(departments.router)
