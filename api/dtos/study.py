from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StudyBaseDTO(BaseModel):  # type: ignore[misc]
    title: str | None = None
    organization_name: str | None = None
    organization_type: str | None = None


class StudyCreateDTO(StudyBaseDTO):
    pass


class StudyUpdateDTO(StudyBaseDTO):
    pass


class StudyResponseDTO(StudyBaseDTO):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
