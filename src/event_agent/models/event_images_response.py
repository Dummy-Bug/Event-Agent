from pydantic import Field

from event_agent.models.search_events_response import Image, TicketmasterModel


class EventImagesResponse(TicketmasterModel):
    id: str
    images: list[Image] = Field(default_factory=list)
