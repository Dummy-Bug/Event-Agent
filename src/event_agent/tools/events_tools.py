import httpx
from langchain.tools import tool

from event_agent.core.config import settings
from event_agent.models.event_images_response import EventImagesResponse
from event_agent.models.events import GetEventImageInput, SearchEventsInput
from event_agent.models.search_events_response import SearchEventsResponse


@tool(
    description="Search Ticketmaster for events happening within a single country. Requires an ISO 3166-1 alpha-2 country code.",
    args_schema=SearchEventsInput,
)
async def search_events(**kwargs) -> SearchEventsResponse:

    args = SearchEventsInput(**kwargs)

    url = settings.ticket_master_base_url + "events"

    params: dict = args.model_dump(by_alias=True, exclude_none=True)
    params["apikey"] = settings.ticket_master_api_key.get_secret_value()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return SearchEventsResponse.model_validate_json(response.content)


async def fetch_event_image(args: GetEventImageInput) -> EventImagesResponse:
    url = settings.ticket_master_base_url + f"events/{args.id}/images"

    params: dict = {"apikey": settings.ticket_master_api_key.get_secret_value()}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return EventImagesResponse.model_validate_json(response.content)
