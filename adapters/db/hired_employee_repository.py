from adapters.db.mssql_connection import MSSQLConnection
from domain.ports import HiredEmployeeRepositoryPort
from typing import List

class HiredEmployeeRepository(HiredEmployeeRepositoryPort):
    async def insert_hired_employees(self, employees: List[dict]) -> dict:
        inserted = 0
        already_exists = 0
        errors = 0

        async with MSSQLConnection() as conn:
            async with conn.cursor() as cur:
                for i, emp in enumerate(employees):
                    try:
                        await cur.execute("SELECT 1 FROM hired_employees WHERE id = ?", (emp["id"],))
                        if await cur.fetchone():
                            already_exists += 1
                            continue
                        await cur.execute(
                            "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (?, ?, ?, ?, ?)",
                            (emp["id"], emp["name"], emp["datetime"], emp["department_id"], emp["job_id"])
                        )
                        inserted += 1

                        if (inserted + already_exists) % 50 == 0:
                            await conn.commit()

                    except Exception:
                        errors += 1

                await conn.commit()

        return {
            "hired_employees": {
                "inserted": inserted,
                "already_exists": already_exists,
                "errors": errors
            }
        }