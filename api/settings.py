import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import dotenv_values

config = {
    **dotenv_values("config/.env.local"),
    **dotenv_values("config/.env"),
    **os.environ,  # override loaded values with environment variables
}


class Settings(BaseSettings):  # type: ignore[misc]
    # db settings
    db_user: str | None = config.get("MAIN_POSTGRES_USER")
    db_password: str | None = config.get("MAIN_POSTGRES_USER")
    db_name: str | None = config.get("MAIN_POSTGRES_USER")

    DATABASE_URL: str = f"postgresql://{db_user}:{db_password}@main-db:5432/{db_name}"
    model_config = SettingsConfigDict()


settings = Settings()
