from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from jose import JWTError, jwt

from lws_backend.config import config
from lws_backend.database import Session, get_managed_session
from lws_backend.core.config import JWT_ENCODE_SECRET_KEY, ALGORITHM
from lws_backend.crud.users import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


async def check_user_auth(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_managed_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        return (None, credentials_exception)
    try:
        payload = jwt.decode(token, config.get(JWT_ENCODE_SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        expiry_date: int = payload.get("exp")
        if username is None:
            return (None, credentials_exception)
    except JWTError:
        return (None, credentials_exception)
    if datetime.utcfromtimestamp(expiry_date) < datetime.utcnow():
        return (None,  token_expired_exception)

    user = get_user_by_username(db, username)

    if user is None:
        return (None, credentials_exception)

    return user.access, None
