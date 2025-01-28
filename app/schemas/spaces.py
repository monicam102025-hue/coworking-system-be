from pydantic import BaseModel
from typing import List, Optional

class SpaceBase(BaseModel):
    name: str
    description: str
    capacity: int
    price_per_hour: float
    is_active: bool
    location: str
    address: str
    city: str
    amenities: List[str]
    image_url: Optional[str]

class Space(SpaceBase):
    id: str

    class Config:
        from_attributes = True