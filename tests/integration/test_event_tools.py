"""Live calls against Ticketmaster's Discovery API for the event tools."""

import httpx
import pytest

from event_agent.models.events import GetEventImageInput, SearchEventsInput
from event_agent.models.search_events_response import Event
from event_agent.tools.events_tools import fetch_event_image, search_events

COUNTRY = "US"
UNKNOWN_ID = "NOT_A_REAL_TICKETMASTER_ID"


@pytest.fixture(scope="module")
async def live_event(anyio_backend) -> Event:
    """One real event from the live API, so no test has to hard-code an id that rots."""
    payload = SearchEventsInput(country_code=COUNTRY, page_size=1)

    response = await search_events.ainvoke(payload.model_dump())

    assert response.embedded is not None, "the search returned no events to test with"
    return response.embedded.events[0]


@pytest.mark.anyio
async def test_search_events_returns_the_requested_page():
    """The page block echoes the request back, and every venue is in the country asked for."""
    payload = SearchEventsInput(country_code=COUNTRY, page_size=2, page_number=1)

    response = await search_events.ainvoke(payload.model_dump())

    assert response.page is not None
    assert response.page.size == 2
    assert response.page.number == 1

    assert response.embedded is not None
    assert 0 < len(response.embedded.events) <= 2

    checked = 0
    for event in response.embedded.events:
        assert event.model_extra is None, "an event should drop what it does not declare"
        if event.embedded is None:
            continue
        for venue in event.embedded.venues:
            if venue.country is None:
                continue
            assert venue.country.country_code == COUNTRY
            checked += 1

    assert checked > 0, "no event carried an embedded venue to check the filter against"


@pytest.mark.anyio
async def test_fetch_event_image_returns_images_for_a_real_event(live_event: Event):
    """The images endpoint answers for the same id the search handed back."""
    payload = GetEventImageInput(event_id=live_event.id)

    response = await fetch_event_image.ainvoke(payload.model_dump())

    assert response.id == live_event.id
    assert response.images, "a live event is expected to carry at least one image"

    for image in response.images:
        assert image.url.startswith("http")


@pytest.mark.anyio
async def test_fetch_event_image_raises_on_an_unknown_event():
    """A 404 surfaces as an httpx error rather than as an empty model."""
    payload = GetEventImageInput(event_id=UNKNOWN_ID)

    with pytest.raises(httpx.HTTPStatusError) as caught:
        await fetch_event_image.ainvoke(payload.model_dump())

    assert caught.value.response.status_code == 404
