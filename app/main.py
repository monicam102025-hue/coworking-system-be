from fastapi import FastAPI
from app.routers import users, auth, bookings, spaces
from app.core.database import create_tables

app = FastAPI()

create_tables()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(spaces.router)

@app.get("/")
def root():
    return {"message": "Welcome to the API"}