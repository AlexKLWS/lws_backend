from lws_backend.database import Session
from lws_backend.database_models.users import User


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()
