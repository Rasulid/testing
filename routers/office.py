
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from starlette.responses import Response

import database
import schemas
from crud import office as crud_office

router = APIRouter()

@router.get("/", response_model=List[schemas.Office])
async def read_offices(location: str = None, db: AsyncSession = Depends(database.get_db)):
    return await crud_office.get_offices(db, location=location)


@router.get("/{office_id}", response_model=schemas.Office)
async def get_office_by_id(office_id: int, db: AsyncSession = Depends(database.get_db)):
    office_data = await crud_office.get_office_by_id(db, office_id)
    if not office_data:
        raise HTTPException(status_code=404, detail="Office not found")
    return office_data


@router.post("/", response_model=schemas.Office)
async def create_office(office: schemas.OfficeCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud_office.create_office(db, office)


@router.put("/{office_id}", response_model=schemas.Office)
async def update_office(office_id: int, office: schemas.OfficeCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud_office.update_office(db, office_id, office)


@router.delete("/{office_id}")
async def delete_office(office_id: int, db: AsyncSession = Depends(database.get_db)):
    res = await crud_office.delete_office(db, office_id)
    if not res:
        raise HTTPException(status_code=404, detail="Office not found")
    return Response(status_code=204)