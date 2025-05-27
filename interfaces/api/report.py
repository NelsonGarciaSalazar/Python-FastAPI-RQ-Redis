from fastapi import APIRouter
from adapters.db.mssql_connection import MSSQLConnection

router = APIRouter()

@router.get("/report/hired-per-quarter")
async def hired_per_quarter():
    query = """
        SELECT d.department, j.job,
            SUM(CASE WHEN MONTH(h.datetime) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN MONTH(h.datetime) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN MONTH(h.datetime) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN MONTH(h.datetime) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees h
        JOIN departments d ON d.id = h.department_id
        JOIN jobs j ON j.id = h.job_id
        WHERE YEAR(h.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job
    """

    async with MSSQLConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

    return [
        {
            "department": row[0],
            "job": row[1],
            "Q1": row[2],
            "Q2": row[3],
            "Q3": row[4],
            "Q4": row[5],
        }
        for row in rows
    ]

@router.get("/report/above-average-hiring")
async def departments_above_average():
    query = """
        SELECT d.id, d.department, COUNT(h.id) AS hired
        FROM hired_employees h
        JOIN departments d ON d.id = h.department_id
        WHERE YEAR(h.datetime) = 2021
        GROUP BY d.id, d.department
        HAVING COUNT(h.id) > (
            SELECT AVG(dept_count) FROM (
                SELECT COUNT(*) AS dept_count
                FROM hired_employees
                WHERE YEAR(datetime) = 2021
                GROUP BY department_id
            ) AS avg_sub
        )
        ORDER BY hired DESC
    """

    async with MSSQLConnection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

    return [
        {
            "id": row[0],
            "department": row[1],
            "hired": row[2]
        }
        for row in rows
    ]