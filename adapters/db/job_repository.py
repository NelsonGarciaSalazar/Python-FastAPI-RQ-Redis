from adapters.db.mssql_connection import MSSQLConnection
from domain.models import Job
from domain.ports import JobRepositoryPort
from typing import List

class JobRepository(JobRepositoryPort):
    async def insert_jobs(self, jobs: List[Job]) -> dict:
        processed = len(jobs)
        inserted = 0
        already_exists = 0
        errors = 0

        async with MSSQLConnection() as conn:
            async with conn.cursor() as cur:
                for job in jobs:
                    try:
                        await cur.execute("SELECT 1 FROM jobs WHERE id = ?", (job.id,))
                        if await cur.fetchone():
                            already_exists += 1
                            continue
                        await cur.execute("INSERT INTO jobs (id, job) VALUES (?, ?)", (job.id, job.job))
                        inserted += 1
                    except Exception:
                        errors += 1

        return {
            "jobs": {
                "processed": processed,
                "inserted": inserted,
                "already_exists": already_exists,
                "errors": errors
            }
        }
