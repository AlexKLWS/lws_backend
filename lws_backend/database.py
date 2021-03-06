from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


def prepare_database(database_url: str):
    engine = create_engine(database_url, pool_recycle=3600, pool_pre_ping=True)
    Session.configure(autocommit=False, autoflush=False, bind=engine)
    Session.configure(autocommit=False, autoflush=True, bind=engine)
    Base.metadata.create_all(engine)


# Dependency
def get_managed_session(autocommit=True):
    db = Session()
    try:
        yield db
        if autocommit:
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
