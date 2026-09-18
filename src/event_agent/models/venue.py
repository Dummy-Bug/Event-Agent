from pydantic import BaseModel, Field


class VenueDetailsInput(BaseModel):
    venue_id: str = Field(
        description="Unique identifier of the venue whose details are to be fetched"
    )


class VenueSearchInput(BaseModel):
    country_code: str = Field(
        serialization_alias="countryCode",
        description="ISO 3166-1 alpha-2 country code to search venues in (e.g., 'US', 'GB', 'IN').",
    )

    keyword: str | None = Field(
        default=None,
        description="Free text to match against the venue name (e.g., 'Sphere', 'Madison Square Garden'). Also the way to search a city, since city is not a supported filter here.",
    )

    state_code: str | None = Field(
        default=None,
        serialization_alias="stateCode",
        description="State or province code to narrow the search to (e.g., 'NV', 'WA'). Only meaningful for countries that have them.",
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=20,
        serialization_alias="size",
        description="Number of venue results to return per page (1–20). Ask for the fewest that answer the question.",
    )

    page_number: int = Field(
        default=0,
        ge=0,
        serialization_alias="page",
        description="Zero-based page number to retrieve for paginated search results.",
    )
