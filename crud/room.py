from http.client import HTTPResponse

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_rooms(db: AsyncSession, office_id: int = None, capacity: int = None):
    query = select(models.Room)
    if office_id:
        query = query.filter(models.Room.office_id == office_id)
    if capacity:
        query = query.filter(models.Room.capacity >= capacity)
    result = await db.execute(query)
    return result.scalars().all()


async def create_room(db: AsyncSession, room_data: schemas.RoomCreate):
    # Преобразуем Pydantic объект в словарь
    room_dict = room_data.model_dump()

    result = await db.execute(select(models.Office).where(models.Office.id == room_dict["office_id"]))
    office = result.scalar_one_or_none()
    if not office:
        raise HTTPException(status_code=400, detail="Office with this ID does not exist")

    new_room = models.Room(**room_dict)
    db.add(new_room)

    await db.commit()
    await db.refresh(new_room)

    return new_room

async def delete_room(db: AsyncSession, room_id: int):
    db_room = await db.get(models.Room, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room with this ID does not exist")
    print(db_room)
    if db_room:
        await db.delete(db_room)
        await db.commit()
    return db_room