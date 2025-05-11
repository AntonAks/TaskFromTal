from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StudyBase(BaseModel):  # type: ignore[misc]
    title: Optional[str] = None
    organization_name: Optional[str] = None
    organization_type: Optional[str] = None


class StudyCreate(StudyBase):
    pass


class StudyUpdate(StudyBase):
    pass


class StudyResponse(StudyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
