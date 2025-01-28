from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, Token
from app.schemas.auth import UserBase, AuthResponse
from app.models.users import User
from app.core.dependencies import get_current_user, revoked_tokens, oauth2_scheme
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me", response_model=UserBase)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name
    }

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    
    new_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=AuthResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"user":UserBase(**user.__dict__), "access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """
    Endpoint para cerrar sesión. Agrega el token JWT actual a una lista de tokens revocados.
    """
    revoked_tokens.add(token)
    return {"message": "Successfully logged out"}


@router.get("/session")
def get_session(current_user: User = Depends(get_current_user)):
    """
    Devuelve la información del usuario actual si está autenticado.
    """
    return {"user": {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name}}