from contextlib import contextmanager

from lws_backend.database import Session


@contextmanager
def managed_session(db: Session, autocommit=True):
    try:
        yield db
        if autocommit:
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.remove()
