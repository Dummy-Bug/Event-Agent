from pydantic import BaseModel, Field


class EventImage(BaseModel):
    id: str = Field(
        description="Unique identifier of the event whose Image is to be retrieved."
    )


class SearchEventsInput(BaseModel):
    # Required
    country_code: str = Field(
        description="ISO 3166-1 alpha-2 country code to filter events by location (e.g., 'US', 'GB', 'IN')."
    )

    # Optional Filters
    id: str | None = Field(
        default=None,
        description="Unique identifier to retrieve a specific event directly.",
    )

    # Pagination
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of event results to return per page (1–100).",
    )

    page_number: int | None = Field(
        default=1,
        ge=1,
        description="Page number to retrieve for paginated search results.",
    )
