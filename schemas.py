from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from pydantic.v1 import root_validator


class OAuth2PasswordRequestFormEmail(BaseModel):
    email: str
    password: str
    scope: str = ""
    client_id: str = None
    client_secret: str = None


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(BaseModel):
    hashed_password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# Office Schemas
class OfficeBase(BaseModel):
    name: str
    location: str

class OfficeCreate(OfficeBase):
    pass

class Office(OfficeBase):
    id: int

    class Config:
        orm_mode = True

class OfficeIDResponse(BaseModel):
    id: int

# Room Schemas
class RoomBase(BaseModel):
    name: str
    capacity: Optional[int] = 0
    office_id: int

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

# Booking Schemas
class BookingBase(BaseModel):
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime

    @root_validator
    def validate_time(cls, values):
        start_time = values.get('start_time')
        end_time = values.get('end_time')
        if start_time and end_time and start_time >= end_time:
            raise ValueError("end_time must be greater than start_time")
        return values

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True