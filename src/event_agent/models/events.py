from pydantic import BaseModel, Field


class GetEventImageInput(BaseModel):
    id: str = Field(
        description="Unique identifier of the event whose Image is to be retrieved."
    )


class SearchEventsInput(BaseModel):
    country_code: str = Field(
        serialization_alias="countryCode",
        description="ISO 3166-1 alpha-2 country code to filter events by location (e.g., 'US', 'GB', 'IN').",
    )

    id: str | None = Field(
        default=None,
        description="Unique identifier to retrieve a specific event directly.",
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=20,
        serialization_alias="size",
        description="Number of event results to return per page (1–100).",
    )

    page_number: int | None = Field(
        default=0,
        ge=0,
        serialization_alias="page",
        description="Zero-based page number to retrieve for paginated search results.",
    )
