import httpx

from event_agent.core.config import settings
from event_agent.models.events import SearchEventsInput


async def search_events(args: SearchEventsInput) -> str:
    url = settings.ticket_master_base_url + "events"

    params = args.model_dump(by_alias=True, exclude_none=True)
    params["apikey"] = settings.ticket_master_api_key.get_secret_value()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text
