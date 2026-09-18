"""Checks on how the tools present themselves to a model. No network."""

import pytest
from pydantic import ValidationError

from event_agent.models.events import GetEventImageInput, SearchEventsInput
from event_agent.models.venue import VenueDetailsInput
from event_agent.tools.events_tools import fetch_event_image, search_events
from event_agent.tools.venue_tools import get_venue_details

TOOLS = [
    (search_events, "search_events", SearchEventsInput),
    (fetch_event_image, "fetch_event_image", GetEventImageInput),
    (get_venue_details, "get_venue_details", VenueDetailsInput),
]

# The upper bound Ticketmaster is asked for, as declared on SearchEventsInput.page_size.
PAGE_SIZE_MAX = 20


@pytest.mark.parametrize(("tool", "name", "schema"), TOOLS)
def test_tool_is_wired_up(tool, name, schema):
    """Each tool keeps its name, description and input model, and is async only."""
    assert tool.name == name
    assert tool.args_schema is schema
    assert tool.description.strip()

    # A model sees one argument per field, not a nested input object.
    assert set(tool.args) == set(schema.model_fields)

    # Defined with async def, so only the async path is wired up.
    assert tool.coroutine is not None
    assert tool.func is None


@pytest.mark.parametrize(
    ("bad_args", "bad_field"),
    [
        ({}, "country_code"),
        ({"country_code": "US", "page_size": PAGE_SIZE_MAX + 1}, "page_size"),
    ],
)
def test_search_events_rejects_bad_arguments(bad_args, bad_field):
    """Bad arguments fail against args_schema before any request is made."""
    with pytest.raises(ValidationError) as caught:
        SearchEventsInput(**bad_args)

    assert caught.value.errors()[0]["loc"] == (bad_field,)


def test_search_events_input_serialises_to_ticketmaster_parameter_names():
    """Ticketmaster expects countryCode, size and page rather than the field names."""
    payload = SearchEventsInput(country_code="US", page_size=2, page_number=1)

    params = payload.model_dump(by_alias=True, exclude_none=True)

    assert params == {"countryCode": "US", "size": 2, "page": 1}
