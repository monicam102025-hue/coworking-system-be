from fastapi import FastAPI
from app.routers import users, auth, bookings, spaces, dashboard

from app.core.database import create_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

create_tables()

#app.include_router(users.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(spaces.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Welcome to the API"}