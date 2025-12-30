"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Deezer Stats"
    debug: bool = False

    # Database
    database_url: str = "postgresql://localhost:5432/deezer_stats"

    # Deezer API
    deezer_app_id: str = ""
    deezer_app_secret: str = ""
    deezer_redirect_uri: str = "http://localhost:8000/auth/callback"


settings = Settings()
