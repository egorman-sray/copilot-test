"""Application configuration using Pydantic BaseSettings."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ResolveServiceConfig(BaseModel):
    """Configuration for the resolve service."""

    api_url: str = "https://staging.app.dev.esgbook.com/api"
    api_path: str = "entities/lookup"
    timeout: int = 30

    @property
    def full_url(self) -> str:
        """Get the full API URL including path."""
        return f"{self.api_url.rstrip('/')}/{self.api_path.lstrip('/')}"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    resolve_service: ResolveServiceConfig = ResolveServiceConfig()
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )
