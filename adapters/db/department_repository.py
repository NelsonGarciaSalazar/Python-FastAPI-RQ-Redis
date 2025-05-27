from adapters.db.mssql_connection import MSSQLConnection
from domain.models import Department
from domain.ports import DepartmentRepositoryPort
from typing import List

class DepartmentRepository(DepartmentRepositoryPort):
    async def insert_departments(self, departments: List[Department]) -> dict:
        processed = len(departments)
        inserted = 0
        already_exists = 0
        errors = 0

        async with MSSQLConnection() as conn:
            async with conn.cursor() as cur:
                for dep in departments:
                    try:
                        await cur.execute("SELECT 1 FROM departments WHERE id = ?", (dep.id,))
                        if await cur.fetchone():
                            already_exists += 1
                            continue
                        await cur.execute("INSERT INTO departments (id, department) VALUES (?, ?)", (dep.id, dep.department))
                        inserted += 1
                    except Exception:
                        errors += 1

        return {
            "departments": {
                "processed": processed,
                "inserted": inserted,
                "already_exists": already_exists,
                "errors": errors
            }
        }
