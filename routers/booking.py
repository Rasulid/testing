from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from starlette import status
from starlette.responses import Response

from crud import booking as booking_crud
import database
import schemas
from routers.auth import oauth2_scheme, decode_jwt

router = APIRouter()


@router.get("/", response_model=List[schemas.Booking])
async def read_bookings(user_id: int = None, room_id: int = None, start_time: datetime = None,
                        end_time: datetime = None, db: AsyncSession = Depends(database.get_db),
                        auth: str = Depends(oauth2_scheme)):

    return await booking_crud.get_bookings(db, user_id=user_id, room_id=room_id, start_time=start_time, end_time=end_time)

@router.post("/", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate,
                         db: AsyncSession = Depends(database.get_db),
                         auth: str = Depends(oauth2_scheme)):
    if booking.room_id == 0 or booking.user_id == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        return await booking_crud.create_booking(db, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, db: AsyncSession = Depends(database.get_db),
                         auth: str = Depends(oauth2_scheme)):
    res = await booking_crud.delete_booking(db, booking_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)