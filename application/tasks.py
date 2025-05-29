from adapters.db.hired_employee_repository import HiredEmployeeRepository

async def process_hired_employees_batch(batch_rows: list) -> dict:
    employees = []
    error_ids = []

    for r in batch_rows:
        try:
            employees.append(
                {
                    "id": int(r[0]),
                    "name": r[1],
                    "datetime": r[2],
                    "department_id": int(r[3]),
                    "job_id": int(r[4])
                }
            )
        except (ValueError, IndexError):
            try:
                error_ids.append(int(r[0]))
            except:
                continue

    repo = HiredEmployeeRepository()
    result = await repo.insert_hired_employees(employees)
    result["hired_employees"]["error_ids"] = error_ids
    result["hired_employees"]["errors"] = len(error_ids) + result["hired_employees"].get("errors", 0)
    result["hired_employees"]["processed"] = len(batch_rows)

    return result