from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from starlette import status
from starlette.responses import Response

import database
import schemas
from crud import room as room_crud

router = APIRouter()

@router.get("/", response_model=List[schemas.Room])
async def read_rooms(office_id: int = None, capacity: int = None, db: AsyncSession = Depends(database.get_db)):
    return await room_crud.get_rooms(db, office_id=office_id, capacity=capacity)

@router.post("/", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: AsyncSession = Depends(database.get_db)):
    if room.office_id == 0:
        raise HTTPException(status_code=404, detail="Office not found")
    return await room_crud.create_room(db, room)

@router.delete("/{room_id}")
async def delete_room(room_id: int, db: AsyncSession = Depends(database.get_db)):
    res = await room_crud.delete_room(db, room_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)