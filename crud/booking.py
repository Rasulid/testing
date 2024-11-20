from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

import models
import schemas


async def get_bookings(db: AsyncSession, user_id: int = None, room_id: int = None, start_time: datetime = None,
                       end_time: datetime = None):
    query = select(models.Booking)
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    if room_id:
        query = query.filter(models.Booking.room_id == room_id)
    if start_time and end_time:
        query = query.filter(
            and_(models.Booking.start_time >= start_time, models.Booking.end_time <= end_time)
        )
    result = await db.execute(query)
    return result.scalars().all()


from datetime import timezone

async def create_booking(db: AsyncSession, booking: schemas.BookingCreate):
    naive_start_time = booking.start_time.replace(tzinfo=None)
    naive_end_time = booking.end_time.replace(tzinfo=None)

    query = select(models.Booking).filter(
        and_(
            models.Booking.room_id == booking.room_id,
            models.Booking.start_time < naive_end_time,
            models.Booking.end_time > naive_start_time,
        )
    )
    result = await db.execute(query)
    if result.scalars().first():
        raise ValueError("The room is already booked for the given time period.")

    # Create a new booking with UTC-aware times
    db_booking = models.Booking(
        room_id=booking.room_id,
        user_id=booking.user_id,
        start_time=naive_start_time,
        end_time=naive_end_time,
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


async def delete_booking(db: AsyncSession, booking_id: int):
    db_booking = await db.get(models.Booking, booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Room with this ID does not exist")
    if db_booking:
        await db.delete(db_booking)
        await db.commit()
    return db_booking