from abc import ABC, abstractmethod
from typing import List
from domain.models import Department
from domain.models import Job
from domain.models import HiredEmployee

class DepartmentRepositoryPort(ABC):
    @abstractmethod
    async def insert_departments(self, departments: List[Department]) -> dict:
        pass

class JobRepositoryPort(ABC):
    @abstractmethod
    async def insert_jobs(self, jobs: List[Job]) -> dict:
        pass

class HiredEmployeeRepositoryPort(ABC):
    @abstractmethod
    async def insert_hired_employees(self, employees: List[HiredEmployee]) -> dict:
        pass
