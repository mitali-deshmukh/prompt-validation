from pathlib import Path
from jinja2 import Template

PROMPT_ROOT = Path("prompts")

def load_prompt(prompt_key: str, version: int) -> str:
    path = PROMPT_ROOT / prompt_key / f"v{version}.txt"
    return path.read_text(encoding="utf-8")

def render_prompt(template_text: str, variables: dict) -> str:
    return Template(template_text).render(**variables)
