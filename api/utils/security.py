from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.db import get_db
from db.models import User
from dtos.auth import TokenData
from settings import settings
import uuid

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 authentication configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


# Function to create a password hash
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Function to verify password against its hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Function to create a JWT token
def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    # Set token expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    # Create JWT token with secret key and HS256 algorithm
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


# Function to get the current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        user_id: str = payload.get("id")

        if username is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(
            username=username, user_id=user_id, is_admin=payload.get("is_admin", False)
        )
    except JWTError:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception

    return user


# Function to check if the user is active
async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Function to check if the user is an administrator
async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


# Function to authenticate a user
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    # Find the user in the database
    user = db.query(User).filter(User.username == username).first()

    # Check password if user is found
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


# Function to register a new user
def register_user(
    db: Session, username: str, email: str, password: str, is_admin: bool = False
) -> User:
    # Create a new user
    db_user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        is_admin=is_admin,
    )

    # Add user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
