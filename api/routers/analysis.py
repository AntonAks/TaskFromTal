from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Literal
from dtos.analysis import AnalysisResponseStudyByOrg, AnalysisResponseOrgByType
from db.db import get_analysis_db
from db.models import OrganizationStatistics, OrganizationTypeStatistics

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.get("/studies_by_org", response_model=List[AnalysisResponseStudyByOrg])  # type: ignore[misc]
async def get_studies_by_org(
    skip: int = 0,
    limit: int = 100,
    organization_name: Optional[str] = None,
    sort_order: Optional[Literal["asc", "desc"]] = Query(
        "desc",
        description="Sort order by quantity: 'asc' for ascending, 'desc' for descending",
    ),
    db: Session = Depends(get_analysis_db),
) -> list[OrganizationStatistics]:
    query = db.query(OrganizationStatistics)

    if organization_name:
        query = query.filter(
            OrganizationStatistics.organization_name.ilike(f"%{organization_name}%")
        )

    if sort_order:
        if sort_order == "desc":
            query = query.order_by(OrganizationStatistics.quantity.desc())
        else:
            query = query.order_by(OrganizationStatistics.quantity.asc())

    studies_by_org: list[OrganizationStatistics] = query.offset(skip).limit(limit).all()
    return studies_by_org


@router.get("/org_types", response_model=List[AnalysisResponseOrgByType])  # type: ignore[misc]
async def get_org_types(
    skip: int = 0,
    limit: int = 100,
    organization_type: Optional[str] = None,
    db: Session = Depends(get_analysis_db),
) -> list[OrganizationTypeStatistics]:
    query = db.query(OrganizationTypeStatistics)

    if organization_type:
        query = query.filter(
            OrganizationTypeStatistics.organization_name.ilike(f"%{organization_type}%")
        )

    org_types: list[OrganizationTypeStatistics] = query.offset(skip).limit(limit).all()
    return org_types
