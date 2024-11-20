from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas



async def get_offices(db: AsyncSession, location: str = None):
    query = select(models.Office)
    if location:
        query = query.filter(models.Office.location == location)
    result = await db.execute(query)
    return result.scalars().all()


async def get_office_by_id(db: AsyncSession, office_id: int):
    result = await db.execute(select(models.Office).where(models.Office.id == office_id))
    return result.scalar_one_or_none()


async def create_office(db: AsyncSession, office: schemas.OfficeCreate):
    db_office = models.Office(**office.model_dump())
    db.add(db_office)
    await db.commit()
    await db.refresh(db_office)
    return db_office


async def update_office(db: AsyncSession, office_id: int, office: schemas.OfficeCreate):
    db_office = await db.get(models.Office, office_id)
    if db_office:
        for key, value in office.model_dump().items():
            setattr(db_office, key, value)
        await db.commit()
        await db.refresh(db_office)
    return db_office


async def delete_office(db: AsyncSession, office_id: int):
    db_office = await db.get(models.Office, office_id)
    if db_office:
        await db.delete(db_office)
        await db.commit()
    return db_office