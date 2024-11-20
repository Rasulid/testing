from fastapi import FastAPI
from routers import office, room, booking, user, auth

app = FastAPI()

app.include_router(user.router)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(office.router, prefix="/offices", tags=["Offices"])
app.include_router(room.router, prefix="/rooms", tags=["Rooms"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])