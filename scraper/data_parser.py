from typing import Any

import requests
from pydantic import BaseModel, ConfigDict
from abc import abstractmethod


class BaseDTO(BaseModel):  # type: ignore[misc]
    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
        from_attributes=True,
    )


class ClinicalTrialsDTO(BaseModel):  # type: ignore[misc]
    pass


class ClinicalTrialsOrganizationDTO(ClinicalTrialsDTO):
    name: str | None = None
    type: str | None = None


class ClinicalTrialsStudyDTO(ClinicalTrialsDTO):
    id: str
    title: str | None = None
    organization: ClinicalTrialsOrganizationDTO | None = None


class ClinicalTrialsStudyListDTO(ClinicalTrialsDTO):
    studies: list[ClinicalTrialsStudyDTO] | None = []
    next_page_token: str | None = ""


class ClinicalSearchAreasDTO(ClinicalTrialsDTO):
    pass


class ClinicalTrialsCollector:
    def __init__(self) -> None:
        self.base_url = "https://clinicaltrials.gov/api/v2/"
        self.resource = "/version"

    def get_json_data(self, **kwargs: Any) -> dict[str, Any] | Any:
        response = requests.get(self.base_url + f"/{self.resource}", params=kwargs)
        return response.json()

    @abstractmethod
    def get_dto_list(self, **kwargs: Any) -> list[BaseModel]: ...


class StudyCollector(ClinicalTrialsCollector):
    def __init__(self) -> None:
        super().__init__()
        self.resource = "/studies"

    def get_total_count(self) -> int | Any:
        url = self.base_url + f"/{self.resource}?countTotal=true"
        response = requests.get(url)
        json_data = response.json()
        return json_data.get("totalCount")

    def get_dto_list(self, **kwargs: dict[str, Any]) -> ClinicalTrialsStudyListDTO:
        json_data = self.get_json_data(**kwargs)
        studies = json_data.get("studies")
        next_page_token = json_data.get("nextPageToken")
        dto_list: list[ClinicalTrialsStudyDTO] = []

        if studies is None:
            return ClinicalTrialsStudyListDTO(studies=dto_list, next_page_token="")

        for study in studies:
            protocol_section = study.get("protocolSection")
            if protocol_section is None:
                continue

            identification_module_item = protocol_section.get("identificationModule")
            organization = identification_module_item.get("organization")
            organization_dto = None

            if organization is not None:
                organization_dto = ClinicalTrialsOrganizationDTO(
                    name=organization.get("fullName"), type=organization.get("class")
                )

            _dto = ClinicalTrialsStudyDTO(
                id=identification_module_item.get("nctId"),
                title=identification_module_item.get("briefTitle"),
                organization=organization_dto,
            )

            dto_list.append(_dto)

        return ClinicalTrialsStudyListDTO(
            studies=dto_list, next_page_token=next_page_token
        )


class StudySearchAreasCollector(ClinicalTrialsCollector):
    def __init__(self) -> None:
        super().__init__()
        self.resource = "/studies/search-areas"
