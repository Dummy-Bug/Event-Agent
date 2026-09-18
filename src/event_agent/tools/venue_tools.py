import httpx
from langchain.tools import tool

from event_agent.core.config import settings
from event_agent.models.venue import VenueDetailsInput, VenueSearchInput
from event_agent.models.venue_details_response import VenueDetailsResponse
from event_agent.models.venue_search_response import VenueSearchResponse
from event_agent.tools import TICKET_MASTER_BASE_URL


@tool(
    description="Search Ticketmaster for venues within a single country, by name. Requires an ISO 3166-1 alpha-2 country code, and takes optional keyword and state filters. Use this to find a venue's ID when the user names a place rather than an event; note that a city is searched through keyword, not a city filter.",
    args_schema=VenueSearchInput,
)
async def search_venues(**kwargs) -> VenueSearchResponse:
    args = VenueSearchInput(**kwargs)

    url = TICKET_MASTER_BASE_URL + "venues"

    params: dict = args.model_dump(by_alias=True, exclude_none=True)
    params["apikey"] = settings.ticket_master_api_key.get_secret_value()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return VenueSearchResponse.model_validate_json(response.content)


@tool(
    description="Get details for a specific venue using the unique identifier for the venue.",
    args_schema=VenueDetailsInput,
)
async def get_venue_details(venue_id: str) -> VenueDetailsResponse:
    url = TICKET_MASTER_BASE_URL + f"venues/{venue_id}"

    params: dict = {"apikey": settings.ticket_master_api_key.get_secret_value()}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return VenueDetailsResponse.model_validate_json(response.content)
