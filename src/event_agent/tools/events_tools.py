import httpx

from event_agent.core.config import settings
from event_agent.models.events import SearchEventsInput

BASE_URL = "https://app.ticketmaster.com/discovery/v2/"


async def search_events(args: SearchEventsInput) -> str:
    url = BASE_URL + "events"

    params = args.model_dump(exclude_none=True)
    params["apikey"] = settings.ticket_master_api_key.get_secret_value()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text
