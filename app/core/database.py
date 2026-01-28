import asyncpg
from app.core.config import settings
from typing import Optional

class Database:
    pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def get_connection(self) -> asyncpg.Connection:
        if not self.pool:
             await self.connect()
        return self.pool.acquire()

db = Database()

async def get_db_pool():
    if not db.pool:
        await db.connect()
    return db.pool
