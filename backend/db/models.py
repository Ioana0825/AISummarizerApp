from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    fileType = Column(String, nullable=False)
    filePath = Column(String, nullable=False)
    status = Column(String, default="pending")
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))
