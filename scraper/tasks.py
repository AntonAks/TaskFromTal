import asyncio
from data_parser import StudyCollector
from db.models import Study
from db.db import get_db
from sqlalchemy.orm import Session


class DummyTestTask:
    @classmethod
    async def collect(cls) -> None:
        while True:
            print(f"Task {cls.__name__} started!")
            await asyncio.sleep(60)
            print(f"Task {cls.__name__} finished!")
            await asyncio.sleep(600)


class CollectStudiesTask:

    @classmethod
    async def collect(cls) -> None:

        collector = StudyCollector()

        initial_dto_list = collector.get_dto_list(pageSize=1000)
        next_page_token = initial_dto_list.next_page_token
        while True:
            print(f"Task {cls.__name__} started!")
            _only_studies_list = []
            new_dto_list = collector.get_dto_list(
                pageSize=1000, pageToken=next_page_token
            )

            _only_studies_list = new_dto_list.studies

            if initial_dto_list is not None:
                _only_studies_list.extend(initial_dto_list.studies)

            session: Session = next(get_db())

            existing_ids = {
                row[0]
                for row in session.query(Study.id)
                .filter(Study.id.in_([dto.id for dto in _only_studies_list]))
                .all()
            }

            bulk = [
                Study(
                    id=_dto.id,
                    title=_dto.title,
                    organization_name=_dto.organization.name,
                    organization_type=_dto.organization.type,
                )
                for _dto in _only_studies_list
                if _dto.id not in existing_ids
            ]
            session.bulk_save_objects(bulk)
            session.commit()

            # Overwrite
            initial_dto_list = None
            next_page_token = new_dto_list.next_page_token

            print(f"{len(bulk)} records were stored.")
            print(f"Task {cls.__name__} finished!")
            await asyncio.sleep(120)
