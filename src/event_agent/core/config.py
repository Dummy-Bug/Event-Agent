from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ticket_master_api_key: SecretStr = Field(validation_alias="TICKET_MASTER_API_KEY")
    ticket_master_base_url: str = Field(
        default="https://app.ticketmaster.com/discovery/v2/",
        validation_alias="TICKET_MASTER_BASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
