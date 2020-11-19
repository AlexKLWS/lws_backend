from typing import Optional
from datetime import timedelta, datetime
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from lws_backend.pydantic_models.token import Token
from lws_backend.database import Session, get_managed_session
from lws_backend.config import config
from lws_backend.core.config import JWT_ENCODE_SECRET_KEY, ALGORITHM, TOKEN_LIFETIME
from lws_backend.core.verify_password import verify_password
from lws_backend.crud.users import get_user_by_username

router = APIRouter()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, config.get(JWT_ENCODE_SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt


@router.post("", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_managed_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=config.get(TOKEN_LIFETIME))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
