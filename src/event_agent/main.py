import asyncio
import uuid

from langchain_core.runnables import RunnableConfig

from event_agent.agent import build_agent
from event_agent.models.provider import (
    Provider,
    default_provider,
    provider_names,
    select_provider,
)


async def ask_for_provider() -> Provider:

    names = provider_names()
    fallback = default_provider()

    if len(names) == 1:
        return fallback

    print("Providers:")
    for position, name in enumerate(names, start=1):
        print(f"  {position}. {name}")

    answer = await asyncio.to_thread(input, "Choose a Provider -> ")

    if answer.strip().isdigit():
        position = int(answer.strip())
        answer = names[position - 1] if 1 <= position <= len(names) else ""

    return select_provider(answer)


async def start_agent():
    provider = await ask_for_provider()
    print(f"Using {provider.name}.\n")

    agent = build_agent(provider)

    config = RunnableConfig(configurable={"thread_id": str(uuid.uuid7())})

    while True:
        user_text = await asyncio.to_thread(input, "User -> ")
        if user_text.lower() in ["q", "quit", "exit"]:
            break

        response = await agent.ainvoke(
            input={"messages": [{"role": "user", "content": user_text}]},
            config=config,
        )

        print("Agent ->", response["messages"][-1].text)
