import pytest

from event_agent.models.events import GetEventImageInput, SearchEventsInput
from event_agent.tools.events_tools import fetch_event_image, search_events


@pytest.mark.anyio
async def test_search_events_live_api():
    """Test calling the search_events tool against Ticketmaster's live endpoint."""
    payload = SearchEventsInput(country_code="US", page_size=2)

    response = await search_events(payload)

    assert response.page is not None
    assert response.embedded is not None
    assert response.page.size == 2
    assert response.page.number == 0
    assert len(response.embedded.events) <= 2


@pytest.mark.anyio
async def test_fetch_events_image_live_api():
    """Test calling the fetch_event_image tool against Ticketmaster's live endpoint."""
    event_id = "1AvjZ_aGkU6vXnK"
    payload = GetEventImageInput(id=event_id)

    response = await fetch_event_image(payload)

    assert response.id == event_id
