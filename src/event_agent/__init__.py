import asyncio
import sys


def main() -> None:
    from event_agent.main import start_agent
    from event_agent.models.provider import NoProviderConfiguredError

    print("Hello from event-agent!")
    try:
        asyncio.run(start_agent())
    except NoProviderConfiguredError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from None
    except KeyboardInterrupt:
        print()
