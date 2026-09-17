"""Response of Ticketmaster GET /discovery/v2/events/{id}/images, the fetch_event_image tool."""

from pydantic import Field

from event_agent.models.search_events_response import (
    Image,
    ResourceLinks,
    TicketmasterModel,
    TicketTextLines,
)


class EventImagesResponse(TicketmasterModel):
    id: str
    type: str | None = None
    name_origin: str | None = None
    images: list[Image] = Field(default_factory=list)
    ticket_text_lines: dict[str, TicketTextLines] | None = None
    links: ResourceLinks | None = Field(default=None, alias="_links")
