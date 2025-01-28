from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.bookings import Booking
from app.models.spaces import Space
from app.core.dependencies import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/space-stats")
def get_space_stats(db: Session = Depends(get_db)):
    """
    Devuelve estadísticas de los espacios más populares.
    """
    space_stats = (
        db.query(Space.name, func.count(Booking.id).label("bookings"))
        .join(Booking, Booking.space_id == Space.id, isouter=True)
        .group_by(Space.name)
        .order_by(Space.name)
        .all()
    )
    return [{"name": stat.name, "bookings": stat.bookings or 0} for stat in space_stats]

@router.get("/hourly-stats")
def get_hourly_stats(db: Session = Depends(get_db)):
    """
    Devuelve estadísticas de reservas por hora.
    """
    hourly_stats = (
        db.query(func.extract("hour", Booking.start_time).label("hour"), func.count(Booking.id).label("bookings"))
        .group_by(func.extract("hour", Booking.start_time))
        .order_by(func.extract("hour", Booking.start_time))
        .all()
    )
    return [{"hour": int(stat.hour), "bookings": stat.bookings} for stat in hourly_stats]

@router.get("/status-stats")
def get_status_stats(db: Session = Depends(get_db)):
    """
    Devuelve la distribución de reservas por estado.
    """
    status_stats = (
        db.query(Booking.status, func.count(Booking.id).label("count"))
        .group_by(Booking.status)
        .all()
    )
    return [{"status": stat.status, "count": stat.count} for stat in status_stats]

@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Devuelve métricas generales para el dashboard.
    """
    # Total de reservas
    total_bookings = db.query(func.count(Booking.id)).scalar()

    # Espacios activos
    active_spaces = db.query(func.count(Space.id)).filter(Space.is_active == True).scalar()

    # Duración promedio de reservas
    booking_durations = db.query(Booking.start_time, Booking.end_time).all()
    if booking_durations:
        avg_duration = sum(
            (end_time - start_time).total_seconds() / 3600
            for start_time, end_time in booking_durations
        ) / len(booking_durations)
    else:
        avg_duration = 0

    return {
        "total_bookings": total_bookings,
        "active_spaces": active_spaces,
        "average_booking_duration": round(avg_duration, 1),
    }