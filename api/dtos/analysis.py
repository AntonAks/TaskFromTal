from pydantic import BaseModel, ConfigDict


class OrganisationTypeDTO(BaseModel):  # type: ignore[misc]
    organization_type: str | None = None
    quantity_studies: int | None = None
    quantity_organizations: int | None = None


class OrganisationStudyDTO(BaseModel):  # type: ignore[misc]
    organization_name: str | None = None
    quantity: int | None = None


class AnalysisResponseStudyByOrg(OrganisationStudyDTO):
    model_config = ConfigDict(from_attributes=True)


class AnalysisResponseOrgByType(OrganisationTypeDTO):
    model_config = ConfigDict(from_attributes=True)
