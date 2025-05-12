# services/auth_service/routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from common.database import SessionLocal
from common.models import User, RoleEnum
from services.auth_service.schemas import UserCreate, UserRead, Token
from services.auth_service.internal_jwt import create_access_token, get_current_user
from typing import List

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(400, "Email ya registrado")
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=user_in.password,  # sin hash
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or user.password_hash != form_data.password:
        raise HTTPException(401, "Credenciales inválidas")
    token = create_access_token({"user_id": user.id, "role": user.role})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def read_me(current=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).get(current.user_id)
    return user


@router.get("/users", response_model=List[UserRead])
def list_users(current=Depends(get_current_user), db: Session = Depends(get_db)):
    if current.role != RoleEnum.admin.value:
        raise HTTPException(403, "Forbidden")
    return db.query(User).all()
