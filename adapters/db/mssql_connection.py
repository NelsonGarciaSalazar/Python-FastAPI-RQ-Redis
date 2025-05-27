import aioodbc
import os

class MSSQLConnection:
    def __init__(self):
        self.dsn = os.getenv("AZURE_SQL_CONNECTION_STRING")

    async def __aenter__(self):
        self.conn = await aioodbc.connect(dsn=self.dsn, autocommit=True)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()
