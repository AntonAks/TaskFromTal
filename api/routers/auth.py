from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from datetime import timedelta

from db.db import get_db

from db.models import User
from dtos.auth import UserCreate, UserResponse, Token, AuthDTO
from utils.security import (
    authenticate_user,
    create_access_token,
    register_user,
)
from settings import settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)  # type: ignore[misc]
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    db_user_by_username = (
        db.query(User).filter(User.username == user_data.username).first()
    )
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    db_user_by_email = db.query(User).filter(User.email == user_data.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user = register_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        is_admin=user_data.is_admin,
    )

    return user


@router.post("/login", response_model=Token)  # type: ignore[misc]
async def login_for_access_token(
    form_data: AuthDTO = Depends(), db: Session = Depends(get_db)
) -> Any:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "is_admin": user.is_admin},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
