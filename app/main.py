from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import db
from app.api.v1.endpoints import users, system
import os
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(
    title="Modernized API",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(system.router, tags=["System"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
