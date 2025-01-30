from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.bookings import Booking
from app.models.users import User
from app.models.spaces import Space
from app.schemas.bookings import Booking as BookingSchema, BookingCreate, BookingUpdate
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("")
def get_bookings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookings = db.query(Booking).join(Space, Booking.space_id == Space.id).filter(Booking.user_id == current_user.id).all()

    return [
        {
            "id": booking.id,
            "space": {
                "id": booking.space.id,
                "name": booking.space.name,
                "price_per_hour": booking.space.price_per_hour,
            },
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "status": booking.status,
            "total_price": booking.total_price,
        }
        for booking in bookings
    ]


@router.post("", response_model=BookingSchema)
def create_booking(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Crea una nueva reserva para un espacio.
    """
    space = db.query(Space).filter(Space.id == booking.space_id).first()
    if not space:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")

    # Validar conflictos de horarios
    conflicts = db.query(Booking).filter(
        Booking.space_id == booking.space_id,
        Booking.status != "cancelled",
        Booking.start_time < booking.end_time,
        Booking.end_time > booking.start_time
    ).all()

    if conflicts:
        raise HTTPException(status_code=400, detail="Espacio no disponible en este horario")

    # Crear reserva
    new_booking = Booking(
        user_id=current_user.id,
        space_id=booking.space_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        total_price=booking.total_price,
        status=booking.status,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@router.put("/{booking_id}", response_model=BookingSchema)
def update_booking(booking_id: str, booking_update: BookingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Busca la reserva

    
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Itera sobre los campos enviados en el request
    for key, value in booking_update.dict(exclude_unset=True).items():
        if value is not None:  # Asegúrate de no asignar valores None
            setattr(booking, key, value)

    # Guarda los cambios
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}", response_model=dict)
def delete_booking(booking_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}


