from sqlalchemy import Column, String, DateTime, Integer, Boolean
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
    fileSize = Column(Integer, nullable=True)  # file size in bytes
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))