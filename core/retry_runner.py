import time
from typing import Any, Callable, Type

from pydantic import BaseModel, ValidationError

from core.validator import parse_json_strict, ParseError, validate, format_validation_errors
from core.repair import build_repair_prompt

ModelCall = Callable[[str], str]

def run_with_retries(
    *,
    model_call: ModelCall,
    initial_prompt: str,
    schema_json: str,
    output_model: Type[BaseModel],
    trace_id: str,
    max_attempts: int = 3,
) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    prompt = initial_prompt

    for i in range(1, max_attempts + 1):
        t0 = time.time()
        raw = model_call(prompt)
        attempt_latency_ms = int((time.time() - t0) * 1000)

        parsed = None
        issues: list[dict[str, Any]] = []
        ok = False
        validated_obj = None

        try:
            parsed = parse_json_strict(raw)
            validated_obj = validate(output_model, parsed)
            ok = True
        except ParseError as e:
            issues = [{"loc": ["__json__"], "msg": str(e), "type": "json_parse_failed", "input": None}]
        except ValidationError as e:
            issues = format_validation_errors(e)

        attempts.append(
            {
                "attempt": i,
                "latency_ms": attempt_latency_ms,
                "raw": raw,
                "parsed_json": parsed,
                "ok": ok,
                "issues": issues,
            }
        )

        if ok and validated_obj is not None:
            return {"ok": True, "validated": validated_obj, "attempts": attempts}

        prompt = build_repair_prompt(
            schema_json=schema_json,
            rendered_prompt=initial_prompt,
            previous_raw=raw,
            issues=issues,
        )

    return {"ok": False, "validated": None, "attempts": attempts}
