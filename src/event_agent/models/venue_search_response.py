from pydantic import Field

from event_agent.models.search_events_response import (
    City,
    Country,
    Page,
    State,
    TicketmasterModel,
)


class VenueSearchResult(TicketmasterModel):
    id: str
    name: str | None = None
    url: str | None = None
    city: City | None = None
    state: State | None = None
    country: Country | None = None


class VenueSearchEmbedded(TicketmasterModel):
    venues: list[VenueSearchResult] = Field(default_factory=list)


class VenueSearchResponse(TicketmasterModel):
    embedded: VenueSearchEmbedded | None = Field(default=None, alias="_embedded")
    page: Page | None = None
