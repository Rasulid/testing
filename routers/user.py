from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from starlette import status

import database
import schemas
from crud import user as user_crud
from routers.auth import oauth2_scheme

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate,
                      db: AsyncSession = Depends(database.get_db),
                      ):
    return await user_crud.create_user(db, user)

@router.get("/", response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 10,
                    db: AsyncSession = Depends(database.get_db),
                    auth: str = Depends(oauth2_scheme)):
    return await user_crud.get_users(db, skip, limit)

@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(database.get_db),
                   auth: str = Depends(oauth2_scheme)):
    return await user_crud.get_user(db, user_id)

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user_update: schemas.UserUpdate,
                      db: AsyncSession = Depends(database.get_db),
                      auth: str = Depends(oauth2_scheme)):
    return await user_crud.update_user(db, user_id, user_update)

@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db),
                      auth: str = Depends(oauth2_scheme)):
    return await user_crud.delete_user(db, user_id)