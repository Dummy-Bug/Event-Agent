from datetime import UTC, datetime

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from event_agent.models.model_response import Response
from event_agent.models.provider import NoProviderConfiguredError, Provider
from event_agent.prompts import build_system_prompt
from event_agent.tools.events_tools import (
    book_events,
    fetch_event_image,
    get_event_details,
    search_events,
)
from event_agent.tools.venue_tools import get_venue_details, search_venues

TOOLS = [
    search_events,
    get_event_details,
    fetch_event_image,
    search_venues,
    get_venue_details,
    book_events,
]


def build_agent(provider: Provider):
    """Build an agent that talks through one provider.

    provider.dialect picks the dialect the client writes (LangChain spells that
    parameter model_provider, though it only selects a class), base_url picks the
    host it is posted to, and the model string is that host's own name for it.
    """
    if provider.api_key is None:
        raise NoProviderConfiguredError(
            f"{provider.name} has no API key. Add one to .env to use it."
        )

    kwargs: dict = {
        "model": provider.model,
        "model_provider": provider.dialect,
        "api_key": provider.api_key.get_secret_value(),
    }
    if provider.base_url is not None:
        kwargs["base_url"] = provider.base_url

    @dynamic_prompt
    def system_prompt(request: ModelRequest) -> str:
        return build_system_prompt(
            agent_name="Claudia",
            tools=TOOLS,
            current_time=datetime.now(UTC).isoformat(timespec="seconds"),
        )

    return create_agent(
        model=init_chat_model(**kwargs),
        tools=TOOLS,
        checkpointer=InMemorySaver(),
        middleware=[system_prompt],
        response_format=Response,
    )
