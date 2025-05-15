from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from db.db import get_db
from db.models import Study, User
from dtos.study import StudyCreateDTO, StudyUpdateDTO, StudyResponseDTO
from utils.security import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/studies",
    tags=["studies"],
)


@router.post("/", response_model=StudyResponseDTO, status_code=status.HTTP_201_CREATED)  # type: ignore[misc]
async def create_study(
    study_data: StudyCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Study:
    new_study = Study(
        id=str(uuid.uuid4()),
        title=study_data.title,
        organization_name=study_data.organization_name,
        organization_type=study_data.organization_type,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_study)
    db.commit()
    db.refresh(new_study)

    return new_study


@router.get("/", response_model=List[StudyResponseDTO])  # type: ignore[misc]
async def get_studies(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    organization_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[Study]:
    query = db.query(Study)

    if title:
        query = query.filter(Study.title.ilike(f"%{title}%"))

    if organization_name:
        query = query.filter(Study.organization_name.ilike(f"%{organization_name}%"))

    studies: list[Study] = query.offset(skip).limit(limit).all()

    return studies


@router.get("/{study_id}", response_model=StudyResponseDTO)  # type: ignore[misc]
async def get_study(
    study_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Study:
    study = db.query(Study).filter(Study.id == study_id).first()

    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )

    return study


@router.put("/{study_id}", response_model=StudyResponseDTO)  # type: ignore[misc]
async def update_study(
    study_id: str,
    study_data: StudyUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Study:
    study = db.query(Study).filter(Study.id == study_id).first()

    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )

    update_data = study_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(study, key, value)

    study.updated_at = datetime.now()

    db.commit()
    db.refresh(study)

    return study


@router.delete("/{study_id}", status_code=status.HTTP_204_NO_CONTENT)  # type: ignore[misc]
async def delete_study(
    study_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> None:
    study = db.query(Study).filter(Study.id == study_id).first()

    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study not found"
        )

    db.delete(study)
    db.commit()
