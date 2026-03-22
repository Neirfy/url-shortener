from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Fastapi variables
    """

    FASTAPI_TITLE: str
    FASTAPI_VERSION: str
    FASTAPI_DESCRIPTION: str
    FASTAPI_API_V1_PATH: str
    FASTAPI_DOCS_URL: str
    FASTAPI_REDOCS_URL: str
    FASTAPI_OPENAPI_URL: str

    """
    Postgres variables
    """

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
            query={"async_fallback": "true"},
        )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
