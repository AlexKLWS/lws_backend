from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


def prepare_database(database_url: str):
    engine = create_engine(database_url)
    Session.configure(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()