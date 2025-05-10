from typing import Any, Tuple, Sequence

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from db.models import Study, OrganizationStatistics, OrganizationTypeStatistics
from db.db import get_main_db, get_analysis_db
from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct, Row


async def data_sync_task() -> None:
    org_stat_rows, org_type_stat_rows = await _update_organisation_statistics_data()
    await _update_analytics_data(org_stat_rows, org_type_stat_rows)


async def _update_organisation_statistics_data() -> tuple[
    Sequence[Row[tuple[str, Any]]], Sequence[Row[tuple[str, Any, Any]]]]:
    main_db_session: Session = next(get_main_db())

    query_organization_statistics = select(
        Study.organization_name,
        func.count(Study.id).label("quantity")
    ).group_by(Study.organization_name).order_by(func.count(Study.id).desc())

    organization_statistics_rows = main_db_session.execute(query_organization_statistics).all()

    query_organization_type_statistics = select(
        Study.organization_type,
        func.count(Study.id).label("quantity_studies"),
        func.count(distinct(Study.organization_name)).label("quantity_organizations")
    ).group_by(Study.organization_type).order_by(func.count(Study.id).desc())

    query_organization_type_statistics_rows = main_db_session.execute(query_organization_type_statistics).all()

    return organization_statistics_rows, query_organization_type_statistics_rows

async def _update_analytics_data(org_stat_rows, org_type_stat_rows) -> None:
    print("Bulk analytics update STARTED!")
    session: Session = next(get_analysis_db())

    try:
        with session.begin():

            # Bulk insert for OrganizationStatistics
            org_stat_data = [
                {"organization_name": org_name, "quantity": quantity}
                for org_name, quantity in org_stat_rows if org_name is not None
            ]

            if org_stat_data:
                _insert_query = pg_insert(OrganizationStatistics).values(org_stat_data)
                _insert_query = _insert_query.on_conflict_do_update(
                    index_elements=["organization_name"],
                    set_={"quantity": _insert_query.excluded.quantity}
                )
                session.execute(_insert_query)

            # Bulk insert for OrganizationTypeStatistics
            org_type_stat_data = [
                {
                    "organization_type": org_type,
                    "quantity_studies": quantity_studies,
                    "quantity_organizations": quantity_orgs
                }
                for org_type, quantity_studies, quantity_orgs in org_type_stat_rows if org_type is not None
            ]

            if org_type_stat_data:
                _insert_query = pg_insert(OrganizationTypeStatistics).values(org_type_stat_data)
                _insert_query = _insert_query.on_conflict_do_update(
                    index_elements=["organization_type"],
                    set_={
                        "quantity_studies": _insert_query.excluded.quantity_studies,
                        "quantity_organizations": _insert_query.excluded.quantity_organizations
                    }
                )
                session.execute(_insert_query)

        print("Bulk analytics update SUCCEEDED.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Bulk analytics update FAILED: {e}")


