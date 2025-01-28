from sqlalchemy import Column, Integer, String, Boolean, Float, ARRAY
from app.core.database import Base

class Space(Base):
    __tablename__ = "spaces"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_hour = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    location = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    amenities = Column(ARRAY(String), nullable=True)
    image_url = Column(String, nullable=True)