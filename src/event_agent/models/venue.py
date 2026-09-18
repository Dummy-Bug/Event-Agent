from pydantic import BaseModel, Field


class VenueDetailsInput(BaseModel):
    id: str = Field(
        description="Unique identifier of the venue whose details are to be fetched"
    )


class VenueSearch(BaseModel):
    country_code: str = Field(
        description="ISO 3166-1 alpha-2 country code to search venues in (e.g., 'US', 'GB', 'IN')."
    )

    id: str | None = Field(
        default=None,
        description="Unique identifier to retrieve a specific venue directly.",
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of venue results to return per page (1–100).",
    )

    page_number: int | None = Field(
        default=1, ge=1, description="Page number to retrieve for paginated results."
    )
