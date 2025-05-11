from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, DateTime
from db.db import Base


class Study(Base):  # type: ignore[misc]
    __tablename__ = "studies"
    id: Mapped[str] = mapped_column(String(1024), primary_key=True)
    title: Mapped[str] = mapped_column(String(1024), nullable=True)
    organization_name: Mapped[str] = mapped_column(String(1024), nullable=True)
    organization_type: Mapped[str] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )


class OrganizationStatistics(Base):  # type: ignore[misc]
    __tablename__ = "organization_statistics"
    organization_name: Mapped[str] = mapped_column(
        String(1024), nullable=False, primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer)


class OrganizationTypeStatistics(Base):  # type: ignore[misc]
    __tablename__ = "organization_type_statistics"
    organization_type: Mapped[str] = mapped_column(
        String(1024), nullable=False, primary_key=True
    )
    quantity_studies: Mapped[int] = mapped_column(Integer)
    quantity_organizations: Mapped[int] = mapped_column(Integer)
