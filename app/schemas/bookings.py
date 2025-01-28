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
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[str]

class Booking(BookingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
