"""Live calls against Ticketmaster's Discovery API for the venue tools."""

import httpx
import pytest

from event_agent.models.events import SearchEventsInput
from event_agent.models.venue import VenueDetailsInput
from event_agent.tools.events_tools import search_events
from event_agent.tools.venue_tools import get_venue_details

COUNTRY = "US"
UNKNOWN_ID = "NOT_A_REAL_TICKETMASTER_ID"


@pytest.fixture(scope="module")
async def live_venue_id(anyio_backend) -> str:
    """A venue id taken from a live event, rather than one hard-coded here."""
    payload = SearchEventsInput(country_code=COUNTRY, page_size=5)

    response = await search_events.ainvoke(payload.model_dump())

    assert response.embedded is not None
    for event in response.embedded.events:
        if event.embedded is not None and event.embedded.venues:
            return event.embedded.venues[0].id

    pytest.fail("no event in the search carried an embedded venue")


@pytest.mark.anyio
async def test_get_venue_details_returns_the_requested_venue(live_venue_id: str):
    """The id asked for comes back, with the fields every venue in a 120-sample sweep had."""
    payload = VenueDetailsInput(id=live_venue_id)

    response = await get_venue_details.ainvoke(payload.model_dump())

    assert response.id == live_venue_id
    assert response.name
    assert response.url
    assert response.timezone
    assert response.postal_code

    assert response.city is not None
    assert response.city.name
    assert response.state is not None
    assert response.state.state_code

    assert response.model_extra is None, "a venue should drop what it does not declare"


@pytest.mark.anyio
async def test_get_venue_details_raises_on_an_unknown_venue():
    """A 404 surfaces as an httpx error rather than as an empty model."""
    with pytest.raises(httpx.HTTPStatusError) as caught:
        await get_venue_details.ainvoke({"id": UNKNOWN_ID})

    assert caught.value.response.status_code == 404
