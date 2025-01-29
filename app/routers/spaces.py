from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app.models.bookings import Booking
from app.schemas.spaces import Space
from app.models.spaces import Space as SpaceModel
from app.core.dependencies import get_db

router = APIRouter(prefix="/spaces", tags=["spaces"])

@router.get("", response_model=List[Space])
def get_spaces(db: Session = Depends(get_db)):
    """
    Devuelve una lista de espacios activos.
    """
    spaces = db.query(SpaceModel).filter(SpaceModel.is_active == True).order_by(SpaceModel.name).all()
    print(spaces)
    return spaces

@router.get("/{space_id}/availability")
def check_availability(space_id: str, start_time: str, end_time: str, db: Session = Depends(get_db)):
    """
    Verifica si un espacio está disponible en un rango de tiempo.
    """
    conflicts = db.query(Booking).filter(
        Booking.space_id == space_id,
        Booking.status != "cancelled",
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).all()

    if conflicts:
        return {"available": False}  # Espacio no disponible
    return {"available": True}  # Espacio disponible
