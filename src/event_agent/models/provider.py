from dataclasses import dataclass

from pydantic import SecretStr

from event_agent.core.config import settings


class NoProviderConfiguredError(RuntimeError):
    """Raised when not one provider holds a key, so there is nothing to talk to."""


@dataclass(frozen=True)
class Provider:
    name: str
    model: str
    dialect: str
    api_key: SecretStr | None
    base_url: str | None = None

    @property
    def is_configured(self) -> bool:
        return self.api_key is not None


PROVIDERS: list[Provider] = [
    Provider(
        name="Google",
        model="gemini-3.6-flash",
        dialect="google_genai",
        api_key=settings.google_api_key,
    ),
    Provider(
        name="Open Router",
        model="deepseek/deepseek-v4-flash-0731:free",
        dialect="openai",
        api_key=settings.open_router_api_key,
        base_url="https://openrouter.ai/api/v1",
    ),
    Provider(
        name="Groq",
        model="openai/gpt-oss-20b",
        dialect="openai",
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    ),
]


def available_providers() -> list[Provider]:
    return [provider for provider in PROVIDERS if provider.is_configured]


def default_provider() -> Provider:
    available = available_providers()
    if not available:
        wanted = ", ".join(provider.name for provider in PROVIDERS)
        raise NoProviderConfiguredError(
            f"No model provider is configured. Add an API key to .env for one of: {wanted}"
        )

    return available[0]
