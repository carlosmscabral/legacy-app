import logging
import sys
import os
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db
from app.api.v1.endpoints import users, system

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 STARTING APPLICATION LIFESPAN...")
    try:
        await db.connect()
        logger.info("✅ STARTUP SEQUENCE COMPLETE.")
    except Exception as e:
        logger.critical(f"💥 STARTUP FAILED: {str(e)}")
        # We don't exit(1) here to allow the process to stay alive enough for logs to flush
        # though Cloud Run will eventually kill it.
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 SHUTTING DOWN APPLICATION...")
    await db.disconnect()
    logger.info("👋 SHUTDOWN COMPLETE.")

app = FastAPI(
    title="Modernized API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(system.router, tags=["System"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

if __name__ == "__main__":
    logger.info("Starting local development server...")
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)