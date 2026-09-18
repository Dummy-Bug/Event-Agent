import httpx
from langchain.tools import tool

from event_agent.core.config import settings
from event_agent.models.venue import VenueDetailsInput
from event_agent.models.venue_details_response import VenueDetailsResponse
from event_agent.tools import TICKET_MASTER_BASE_URL


@tool(
    description="Get details for a specific venue using the unique identifier for the venue.",
    args_schema=VenueDetailsInput,
)
async def get_venue_details(id: str) -> VenueDetailsResponse:
    url = TICKET_MASTER_BASE_URL + f"venues/{id}"

    params: dict = {"apikey": settings.ticket_master_api_key.get_secret_value()}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return VenueDetailsResponse.model_validate_json(response.content)
