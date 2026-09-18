from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"
PROMPT_DIR = Path(__file__).resolve().parents[3] / "prompts"


class Settings(BaseSettings):
    ticket_master_api_key: SecretStr = Field(validation_alias="TICKET_MASTER_API_KEY")

    google_api_key: SecretStr | None = Field(
        default=None, validation_alias="GOOGLE_API_KEY"
    )
    groq_api_key: SecretStr | None = Field(
        default=None, validation_alias="GROQ_API_KEY"
    )
    open_router_api_key: SecretStr | None = Field(
        default=None, validation_alias="OPEN_ROUTER_API_KEY"
    )

    prompts_directory: Path = PROMPT_DIR

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
