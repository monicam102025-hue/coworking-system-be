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
        .order_by(func.count(Booking.id).desc())  # Ordenar por cantidad de reservas
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
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0

    # Espacios activos
    active_spaces = db.query(func.count(Space.id)).filter(Space.is_active == True).scalar() or 0

    # Duración promedio de reservas (en horas)
    booking_durations = db.query(Booking.start_time, Booking.end_time).all()
    if booking_durations:
        avg_duration = sum(
            (end_time - start_time).total_seconds() / 3600
            for start_time, end_time in booking_durations
        ) / len(booking_durations)
    else:
        avg_duration = 0

    # Tasa de ocupación: (total horas reservadas / total horas disponibles) * 100
    total_hours_reserved = sum(
        (end_time - start_time).total_seconds() / 3600
        for start_time, end_time in booking_durations
    )
    total_available_hours = active_spaces * 24  # Asume 24 horas disponibles por día por espacio
    occupancy_rate = (total_hours_reserved / total_available_hours * 100) if total_available_hours else 0

    return {
        "totalBookings": total_bookings,
        "activeSpaces": active_spaces,
        "averageBookingDuration": round(avg_duration, 1),
        "occupancyRate": round(occupancy_rate, 1),
    }