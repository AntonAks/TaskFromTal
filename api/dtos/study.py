from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StudyBase(BaseModel):  # type: ignore[misc]
    title: str | None = None
    organization_name: str | None = None
    organization_type: str | None = None


class StudyCreate(StudyBase):
    pass


class StudyUpdate(StudyBase):
    pass


class StudyResponse(StudyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
