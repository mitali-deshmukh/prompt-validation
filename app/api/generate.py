import time
import uuid
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas.support_triage import SupportTriageOutput
from core.renderer import load_prompt, render_prompt
from core.retry_runner import run_with_retries
from core.groq_client import GroqLLM

router = APIRouter()

llm = GroqLLM()


class GenerateRequest(BaseModel):
    prompt_key: str = Field(default="support_triage")
    prompt_version: int = Field(default=1)

    subject: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=4000)

    customer_tier: str | None = None
    product_area: str | None = None


@router.post("/v1/generate", response_model=SupportTriageOutput)
def generate(req: GenerateRequest):
    trace_id = str(uuid.uuid4())
    start = time.time()

    try:
        template_text = load_prompt(req.prompt_key, req.prompt_version)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={"trace_id": trace_id, "error": "prompt_not_found"})

    schema_json = json.dumps(SupportTriageOutput.model_json_schema(), ensure_ascii=False)

    variables = {
        "subject": req.subject,
        "message": req.message,
        "customer_tier": req.customer_tier,
        "product_area": req.product_area,
        "schema_json": schema_json,
    }

    rendered_prompt = render_prompt(template_text, variables)

    def model_call(prompt: str) -> str:
        return llm.chat_json(prompt)

    result = run_with_retries(
        model_call=model_call,
        initial_prompt=rendered_prompt,
        schema_json=schema_json,
        output_model=SupportTriageOutput,
        trace_id=trace_id,
        max_attempts=3,
    )

    if not result["ok"]:
        raise HTTPException(
            status_code=422,
            detail={
                "trace_id": trace_id,
                "error": "all_attempts_failed",
                "attempts": result["attempts"],
            },
        )

    _latency_ms = int((time.time() - start) * 1000)
    _ = _latency_ms

    return result["validated"]