from abc import ABC, abstractmethod
from typing import List
from domain.models import Department

class DepartmentRepositoryPort(ABC):
    @abstractmethod
    async def insert_departments(self, departments: List[Department]) -> dict:
        pass
