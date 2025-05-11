import plotly.express as px
import pandas as pd
from db.models import OrganizationStatistics, OrganizationTypeStatistics
from db.db import get_analysis_db
from sqlalchemy.orm import Session


class SimpleCharts:
    @staticmethod
    def get_chars(top_n: int) -> str:
        session: Session = next(get_analysis_db())

        # ---- Top N Organizations ----
        org_stats = (
            session.query(OrganizationStatistics)
            .order_by(OrganizationStatistics.quantity.desc())
            .limit(top_n)
            .all()
        )

        df_orgs = pd.DataFrame(
            [(org.organization_name, org.quantity) for org in org_stats],
            columns=["Organization", "Studies"],
        )

        fig_bar = px.bar(
            df_orgs,
            x="Organization",
            y="Studies",
            title=f"Top {top_n} Organizations by Study Count",
            text_auto=True,
            color_discrete_sequence=["#1f77b4"],
        )
        fig_bar.update_layout(xaxis_tickangle=-45)

        fig_pie = px.pie(
            df_orgs,
            names="Organization",
            values="Studies",
            title=f"Share of Studies in Top {top_n} Organizations",
            color_discrete_sequence=px.colors.sequential.Blues,
        )

        # ---- Studies by Organization Type ----
        org_type_stats = (
            session.query(OrganizationTypeStatistics)
            .order_by(OrganizationTypeStatistics.quantity_studies.desc())
            .all()
        )

        df_type_studies = pd.DataFrame(
            [(row.organization_type, row.quantity_studies) for row in org_type_stats],
            columns=["Organization Type", "Total Studies"],
        )

        fig_organization_type_1 = px.bar(
            df_type_studies,
            x="Organization Type",
            y="Total Studies",
            title="Total Studies per Organization Type",
            text_auto=True,
            color_discrete_sequence=["#2ca02c"],
        )

        # ---- Unique Orgs by Type ----
        df_type_orgs = pd.DataFrame(
            [
                (row.organization_type, row.quantity_organizations)
                for row in org_type_stats
            ],
            columns=["Organization Type", "Unique Organizations"],
        )

        fig_organization_type_2 = px.bar(
            df_type_orgs,
            x="Organization Type",
            y="Unique Organizations",
            title="Unique Organizations per Type",
            text_auto=True,
            color_discrete_sequence=["#d62728"],
        )

        # ---- Scatter Plot: 2 measures vs 1 dimension ----
        df_scatter = pd.DataFrame(
            [
                (
                    row.organization_type,
                    row.quantity_studies,
                    row.quantity_organizations,
                )
                for row in org_type_stats
            ],
            columns=["Organization Type", "Total Studies", "Unique Organizations"],
        )

        fig_scatter = px.scatter(
            df_scatter,
            x="Total Studies",
            y="Unique Organizations",
            text="Organization Type",
            title="Studies vs Unique Organizations per Type",
            color="Organization Type",
            size_max=60,
        )
        fig_scatter.update_traces(textposition="top center")

        # ---- HTML Template ----
        html = f"""
        <html>
        <head>
            <title>Analytics Dashboard</title>
            <style>
                .grid {{
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                }}
                .chart {{
                    width: 48%;
                    min-width: 300px;
                    margin-bottom: 40px;
                }}
                .fullwidth {{
                    width: 98%;
                    margin: 0 auto 40px auto;
                }}
            </style>
        </head>
        <body>
            <h1>📊 Simple Analytics Dashboard</h1>
            <p>Showing top {top_n} organizations. Try changing <code>?top=15</code> in URL.</p>

            <div class="grid">
                <div class="chart">
                {fig_bar.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
                <div class="chart">
                {fig_pie.to_html(full_html=False, include_plotlyjs=False)}
                </div>
            </div>

            <div class="grid">
                <div class="chart">
                    {fig_organization_type_1.to_html(full_html=False, include_plotlyjs=False)}
                </div>
                <div class="chart">
                    {fig_organization_type_2.to_html(full_html=False, include_plotlyjs=False)}
                </div>
            </div>

            <div class="fullwidth">
                {fig_scatter.to_html(full_html=False, include_plotlyjs=False)}
            </div>
        </body>
        </html>
        """

        return html
