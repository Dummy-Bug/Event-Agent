from collections.abc import Sequence
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from langchain_core.tools import BaseTool

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=False,
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)


def _render_template(*, template_name: str, **context) -> str:
    return _env.get_template(template_name).render(context)


def build_system_prompt(
    *,
    agent_name: str,
    tools: Sequence[BaseTool],
    current_time: str,
    extra_guidance: str | None = None,
) -> str:
    return _render_template(
        template_name="system.jinja",
        agent_name=agent_name,
        tools=tools,
        current_time=current_time,
        extra_guidance=extra_guidance,
    )


def build_greetings(agent_name: str) -> str:
    return _render_template(
        template_name="greetings.jinja",
        agent_name=agent_name,
    )
