from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from lws_backend.database import Base


class Icon(Base):
    __tablename__ = "icons"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    data = Column(String)
    height = Column(String)
    width = Column(String)
