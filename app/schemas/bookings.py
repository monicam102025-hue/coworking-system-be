from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    space_id: str
    start_time: datetime
    end_time: datetime
    status: str
    total_price: float

class BookingCreate(BookingBase):
    space_id: str
    start_time: datetime
    end_time: datetime

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    total_price: Optional[float] = None

    class Config:
        orm_mode = True

class Booking(BookingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
