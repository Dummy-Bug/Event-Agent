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

        async for chunk in agent.astream(
            {"messages": [{"role": "user", "content": user_text}]},
            stream_mode=["messages", "custom"],
            version="v2",
            config=config,
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                node = metadata["langgraph_node"]

                if node == "tools":
                    print(f"Tool Node: {node}")
                    print(f"Response from the Too Node : content_block {token.content_blocks}")
                    print("\n")
                    continue

                if token.tool_calls or token.tool_call_chunks:
                    print(f"Tool Call (internal): {token.tool_calls or token.tool_call_chunks}")
                    print("\n")
                    continue

                if token.content:
                    print(f"UI Text: {token.content}")
                    print("\n")
            elif chunk["type"] == "custom":
                print(f"Custom Event: {chunk['data']}")
                print("\n")


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
