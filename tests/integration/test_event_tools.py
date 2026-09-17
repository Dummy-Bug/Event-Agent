import json

import pytest

from event_agent.models.events import SearchEventsInput
from event_agent.tools.events_tools import search_events


@pytest.mark.anyio
async def test_search_events_live_api():
    """Test calling the search_events tool against Ticketmaster's live endpoint."""
    payload = SearchEventsInput(country_code="US", page_size=2)

    response = await search_events(payload)
    body = json.loads(response)

    assert body["page"]["size"] == 2
    assert body["page"]["number"] == 0
    assert len(body["_embedded"]["events"]) <= 2
