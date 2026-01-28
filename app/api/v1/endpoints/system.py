from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import socket
import asyncpg
from app.core.database import get_db_pool
from app.core.config import settings
from app.api.v1.schemas.system import HealthResponse, RootResponse, EndpointInfo

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health(pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        async with pool.acquire() as conn:
            await conn.execute('SELECT 1')
        
        return {
            'status': 'healthy',
            'database': 'connected',
            'hostname': socket.gethostname(),
            'db_host': settings.DB_HOST
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'status': 'unhealthy',
                'error': str(e),
                'hostname': socket.gethostname()
            }
        )

@router.get("/", response_model=RootResponse)
async def index():
    return {
        'message': 'Application API',
        'version': '1.0.0',
        'hostname': socket.gethostname(),
        'endpoints': [
            {'method': 'GET', 'path': '/health', 'description': 'Health check'},
            {'method': 'GET', 'path': '/api/users', 'description': 'List all users'},
            {'method': 'GET', 'path': '/api/users/<id>', 'description': 'Get user by ID'},
            {'method': 'POST', 'path': '/api/users', 'description': 'Create new user'},
            {'method': 'DELETE', 'path': '/api/users/<id>', 'description': 'Delete user'}
        ]
    }
