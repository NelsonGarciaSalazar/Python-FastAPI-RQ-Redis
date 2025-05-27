from pydantic import BaseModel

class Department(BaseModel):
    id: int
    department: str

class Job(BaseModel):
    id: int
    job: str
