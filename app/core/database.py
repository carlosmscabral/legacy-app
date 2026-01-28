import asyncpg
import logging
import sys
from app.core.config import settings
from typing import Optional

# Configure excruciating logging to stdout
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class Database:
    pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            host_val = settings.DB_HOST.strip()
            logger.info("INITIATING ALLOYDB CONNECTION ATTEMPT...")
            logger.info(f"Connection Parameters: host='{host_val}' (len={len(host_val)}), type={type(host_val)}, port={settings.DB_PORT}, user='{settings.DB_USER}'")
            try:
                self.pool = await asyncpg.create_pool(
                    user=settings.DB_USER.strip(),
                    password=settings.DB_PASSWORD.strip(),
                    database=settings.DB_NAME.strip(),
                    host=host_val,
                    port=settings.DB_PORT,
                    min_size=1,
                    max_size=10,
                    command_timeout=60.0
                )
                logger.info("✅ ALLOYDB CONNECTION POOL ESTABLISHED SUCCESSFULLY.")
                
                # --- AUTO-INITIALIZE TABLE ---
                async with self.pool.acquire() as conn:
                    logger.info("VERIFYING DATABASE SCHEMA...")
                    await conn.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            department VARCHAR(100) DEFAULT 'General',
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                        );
                    ''')
                    logger.info("✅ DATABASE SCHEMA IS READY.")
                # -----------------------------

            except Exception as e:
                logger.error(f"❌ FAILED TO CREATE ALLOYDB POOL: {str(e)}", exc_info=True)
                raise

    async def disconnect(self):
        if self.pool:
            logger.info("CLOSING ALLOYDB CONNECTION POOL...")
            await self.pool.close()
            logger.info("✅ ALLOYDB CONNECTION POOL CLOSED.")

    async def get_connection(self) -> asyncpg.Connection:
        if not self.pool:
             logger.warning("Connection requested but pool not initialized. Attempting connect().")
             await self.connect()
        logger.debug("Acquiring connection from pool...")
        return self.pool.acquire()

db = Database()

async def get_db_pool():
    if not db.pool:
        await db.connect()
    return db.pool