# core/validator.py

from __future__ import annotations

import json
from typing import Any, Type

from pydantic import BaseModel, ValidationError


class ParseError(Exception):
    """Raised when the model output is not valid JSON."""
    pass


def parse_json_strict(raw: str) -> Any:
    """
    Parse a raw LLM string as strict JSON.

    Rules:
    - Must be valid JSON with no leading/trailing non-whitespace text.
    - No markdown fences, no commentary.
    """
    if raw is None:
        raise ParseError("No output to parse")

    raw = raw.strip()
    if not raw:
        raise ParseError("Empty output")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ParseError(f"Invalid JSON: {e.msg} at line {e.lineno} col {e.colno}") from e


def validate(model: Type[BaseModel], payload: Any) -> BaseModel:
    """
    Validate parsed JSON payload against a Pydantic model.
    Raises ValidationError if invalid.
    """
    return model.model_validate(payload)


def format_validation_errors(e: ValidationError) -> list[dict[str, Any]]:
    """
    Convert Pydantic ValidationError into a stable, JSON-friendly shape.
    Useful for logging and for repair prompts.
    """
    issues: list[dict[str, Any]] = []
    for err in e.errors():
        issues.append(
            {
                "loc": list(err.get("loc", [])),
                "msg": err.get("msg", ""),
                "type": err.get("type", ""),
                "input": err.get("input", None),
            }
        )
    return issues
