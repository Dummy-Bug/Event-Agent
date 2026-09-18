from pydantic import BaseModel, Field


class GetEventImageInput(BaseModel):
    event_id: str = Field(
        description="Unique identifier of the event whose Image is to be retrieved."
    )


class GetEventDetailsInput(BaseModel):
    event_id: str = Field(
        description="Unique identifier of the event to look up, as returned by search_events."
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

    keyword: str | None = Field(
        default=None,
        description="Free text to match against event, performer and venue names (e.g., 'Eagles', 'Hamilton'). Use this whenever the user names something specific.",
    )

    city: str | None = Field(
        default=None,
        description="City name to narrow the search to (e.g., 'Seattle', 'Las Vegas'). Use the plain name, not an airport or metro code.",
    )

    state_code: str | None = Field(
        default=None,
        serialization_alias="stateCode",
        description="State or province code to narrow the search to (e.g., 'NV', 'WA'). Only meaningful for countries that have them.",
    )

    start_date_time: str | None = Field(
        default=None,
        serialization_alias="startDateTime",
        description="Earliest event start, as UTC ISO 8601 with no fractional seconds: YYYY-MM-DDTHH:MM:SSZ (e.g., '2026-10-01T00:00:00Z').",
    )

    end_date_time: str | None = Field(
        default=None,
        serialization_alias="endDateTime",
        description="Latest event start, as UTC ISO 8601 with no fractional seconds: YYYY-MM-DDTHH:MM:SSZ (e.g., '2026-10-31T23:59:59Z').",
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=20,
        serialization_alias="size",
        description="Number of event results to return per page (1–20). Ask for the fewest that answer the question; narrow with keyword, city and dates rather than requesting more results.",
    )

    page_number: int | None = Field(
        default=0,
        ge=0,
        serialization_alias="page",
        description="Zero-based page number to retrieve for paginated search results.",
    )


class BookEventsInput(BaseModel):
    ids: list = Field(
        default_factory=list,
        description="Unique identifiers of all the Events to be booked",
    )
