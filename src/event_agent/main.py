import asyncio
import uuid

from langchain_core.runnables import RunnableConfig

from event_agent.agent import build_agent
from event_agent.models.provider import default_provider


async def main():
    provider = default_provider()
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


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
