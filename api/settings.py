import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import dotenv_values

config = {
    **dotenv_values("config/.env.local"),
    **dotenv_values("config/.env"),
    **os.environ,  # override loaded values with environment variables
}

TESTING = os.environ.get("TESTING", "").lower() == "true"


class Settings(BaseSettings):  # type: ignore[misc]
    # main db settings
    main_db_user: str | None = config.get("MAIN_POSTGRES_USER")
    main_db_password: str | None = config.get("MAIN_POSTGRES_PASSWORD")
    main_db_name: str | None = config.get("MAIN_POSTGRES_DB")

    # analysis db settings
    analysis_db_user: str | None = config.get("ANALYSIS_POSTGRES_USER")
    analysis_db_password: str | None = config.get("ANALYSIS_POSTGRES_PASSWORD")
    analysis_db_name: str | None = config.get("ANALYSIS_POSTGRES_DB")

    MAIN_DATABASE_URL: str = (
        "sqlite:///test_db/test.db"
        if TESTING
        else f"postgresql://{main_db_user}:{main_db_password}@main-db:5432/{main_db_name}"
    )

    ANALYSIS_DATABASE_URL: str = (
        "sqlite:///test_db/test.db"
        if TESTING
        else f"postgresql://{analysis_db_user}:{analysis_db_password}@analysis-db:5432/{analysis_db_name}"
    )

    model_config = SettingsConfigDict()


settings = Settings()
