from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import asyncpg
from app.core.database import get_db_pool
from app.api.v1.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.get("", response_model=Dict[str, Any])
async def get_users(pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM users ORDER BY id')
            users = [dict(row) for row in rows]
            return {'count': len(users), 'users': users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM users WHERE id = $1', user_id)
            if row:
                return dict(row)
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    'INSERT INTO users (name, email, department) VALUES ($1, $2, $3) RETURNING *',
                    user.name, user.email, user.department
                )
                return dict(row)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: int, pool: asyncpg.Pool = Depends(get_db_pool)):
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow('DELETE FROM users WHERE id = $1 RETURNING id', user_id)
            if row:
                return {'message': f'User {user_id} deleted'}
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))