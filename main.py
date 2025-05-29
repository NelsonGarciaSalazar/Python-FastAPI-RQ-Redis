from fastapi import FastAPI, Request
from interfaces.api import departments, jobs, hired_employees, task_status, report
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="HR Processing API",
    description="Processes HR CSVs into Azure SQL",
    version="1.0"
)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "HR Processing API is running"}

app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(hired_employees.router)
app.include_router(task_status.router)
app.include_router(report.router)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "body": exc.body})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc)})