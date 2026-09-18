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
    Provider(
        name="Google",
        model="gemini-3.6-flash",
        dialect="google_genai",
        api_key=settings.google_api_key,
    ),
]


def available_providers(providers: list[Provider] | None = None) -> list[Provider]:
    """Only the providers holding a key, in declaration order."""
    candidates = PROVIDERS if providers is None else providers
    return [provider for provider in candidates if provider.is_configured]


def provider_names(providers: list[Provider] | None = None) -> list[str]:
    """The names to offer a user. One that cannot authenticate is never offered."""
    return [provider.name for provider in available_providers(providers)]


def default_provider(providers: list[Provider] | None = None) -> Provider:
    """The first configured provider. Declaration order is the preference order."""
    available = available_providers(providers)
    if not available:
        candidates = PROVIDERS if providers is None else providers
        wanted = ", ".join(provider.name for provider in candidates)
        raise NoProviderConfiguredError(
            f"No model provider is configured. Add an API key to .env for one of: {wanted}"
        )

    return available[0]


def select_provider(
    name: str | None = None, providers: list[Provider] | None = None
) -> Provider:
    """Find a configured provider by name, case-insensitively.

    Anything blank or unrecognized gets the default, so a mistyped answer still
    starts a session rather than ending one.
    """
    if name and name.strip():
        for provider in available_providers(providers):
            if provider.name.lower() == name.strip().lower():
                return provider

    return default_provider(providers)
