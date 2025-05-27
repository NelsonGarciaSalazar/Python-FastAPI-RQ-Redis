from datetime import datetime
from typing import List

from pydantic import BaseModel

class Department(BaseModel):
    id: int
    department: str

class Job(BaseModel):
    id: int
    job: str

class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int
