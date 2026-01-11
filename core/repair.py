import json
from typing import Any

def build_repair_prompt(
    schema_json: str,
    rendered_prompt: str,
    previous_raw: str,
    issues: list[dict[str, Any]],
) -> str:
    return (
        "You are fixing a JSON output to match a schema.\n"
        "Rules:\n"
        "- Output a single JSON object only.\n"
        "- Do not add keys not in the schema.\n"
        "- Fix types, enums, missing fields, and length limits.\n\n"
        "Original task prompt:\n"
        f"{rendered_prompt}\n\n"
        "Schema (JSON Schema):\n"
        f"{schema_json}\n\n"
        "Previous invalid output:\n"
        f"{previous_raw}\n\n"
        "Validation issues:\n"
        f"{json.dumps(issues, ensure_ascii=False)}\n\n"
        "Return corrected JSON only."
    )
