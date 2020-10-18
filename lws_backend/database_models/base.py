from sqlalchemy import func, Column, Integer, DateTime

from lws_backend.database import Base


class DatabaseBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
