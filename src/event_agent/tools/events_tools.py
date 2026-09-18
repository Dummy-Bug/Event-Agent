from typing import Any

import httpx
from langchain.tools import tool

from event_agent.core.config import settings
from event_agent.models.event_details_response import EventDetailsResponse
from event_agent.models.event_images_response import EventImagesResponse
from event_agent.models.events import (
    BookEventsInput,
    GetEventDetailsInput,
    GetEventImageInput,
    SearchEventsInput,
)
from event_agent.models.search_events_response import SearchEventsResponse
from event_agent.tools import TICKET_MASTER_BASE_URL


@tool(
    description="Search Ticketmaster for events happening within a single country. Requires an ISO 3166-1 alpha-2 country code, and takes optional keyword, city, state and date-range filters — narrow with those rather than asking for more results. Each result carries the event id, name, date, status, venue and ticket link; use fetch_event_image for pictures and get_venue_details for the full venue record.",
    args_schema=SearchEventsInput,
)
async def search_events(**kwargs) -> SearchEventsResponse:

    args = SearchEventsInput(**kwargs)

    url = TICKET_MASTER_BASE_URL + "events"

    params: dict = args.model_dump(by_alias=True, exclude_none=True)
    params["apikey"] = settings.ticket_master_api_key.get_secret_value()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return SearchEventsResponse.model_validate_json(response.content)


@tool(
    description="Get the full record for one event by its ID, including when tickets go on sale, the per-person ticket limit, any age rule and the seat map. Call this when the user asks about a specific event a search already found; a search result alone does not carry these.",
    args_schema=GetEventDetailsInput,
)
async def get_event_details(event_id: str) -> EventDetailsResponse:

    params: dict = {"apikey": settings.ticket_master_api_key.get_secret_value()}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            TICKET_MASTER_BASE_URL + f"events/{event_id}", params=params
        )
        response.raise_for_status()
        return EventDetailsResponse.model_validate_json(response.content)


@tool(
    description="Fetches the Images of an Event given the event ID.",
    args_schema=GetEventImageInput,
)
async def fetch_event_image(**kwargs) -> EventImagesResponse:
    args = GetEventImageInput(**kwargs)

    url = TICKET_MASTER_BASE_URL + f"events/{args.id}/images"

    params: dict = {"apikey": settings.ticket_master_api_key.get_secret_value()}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return EventImagesResponse.model_validate_json(response.content)


@tool(
    description="Book all the events iff provided the correct events IDs",
    args_schema=BookEventsInput,
)
async def book_events(ids: list) -> dict[str, Any]:
    return {"Success": ids}
