from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from lws_backend.config import config
from lws_backend.database import Session, get_db
from lws_backend.core.config import JWT_ENCODE_SECRET_KEY, ALGORITHM
from lws_backend.crud.users import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def check_user_auth(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.get(JWT_ENCODE_SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
