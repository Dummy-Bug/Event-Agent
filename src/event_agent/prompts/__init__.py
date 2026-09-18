from jinja2 import Environment, FileSystemLoader, select_autoescape

from event_agent.core.config import settings

_env = Environment(
    loader=FileSystemLoader(settings.prompts_directory),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _render_template(*, template_name: str, **context):
    return _env.get_template(template_name).render(context)


def build_system_prompt(*, agent_name: str, extra_guidance: str | None = None) -> str:
    return _render_template(
        template_name="system.jinja",
        agent_name=agent_name,
        extra_guidance=extra_guidance,
    )


def build_greetings(agent_name: str) -> str:
    return _render_template(
        template_name="greetings.jinja",
        agent_name=agent_name,
    )
