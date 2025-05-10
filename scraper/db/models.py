from uuid import uuid4
from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, DateTime, UUID
from db.db import Base


class Study(Base):
    __tablename__ = 'studies'
    id: Mapped[str] = mapped_column(String(1024), primary_key=True)
    title: Mapped[str] = mapped_column(String(1024), nullable=True)
    organization_name: Mapped[str] = mapped_column(String(1024), nullable=True)
    organization_type: Mapped[str] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,  default=datetime.now)
