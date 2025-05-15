from datetime import datetime


from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, DateTime, Boolean
from db.db import Base


class Study(Base):  # type: ignore[misc]
    __tablename__ = "studies"
    __table_args__ = {"extend_existing": True}
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
    __table_args__ = {"extend_existing": True}
    organization_name: Mapped[str] = mapped_column(
        String(1024), nullable=False, primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer)


class OrganizationTypeStatistics(Base):  # type: ignore[misc]
    __tablename__ = "organization_type_statistics"
    __table_args__ = {"extend_existing": True}
    organization_type: Mapped[str] = mapped_column(
        String(1024), nullable=False, primary_key=True
    )
    quantity_studies: Mapped[int] = mapped_column(Integer)
    quantity_organizations: Mapped[int] = mapped_column(Integer)


class User(Base):  # type: ignore[misc]
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(1024), primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
