# LLM Prompt and Output Validation Service

A production-style FastAPI service that enforces **structured, safe, and deterministic LLM outputs** using
versioned prompts, strict schema validation, and automated retry with repair prompts.

This service acts as a gatekeeper between your application and an LLM.



## Why this exists

LLMs are powerful but unreliable at interfaces. They often return:
- Invalid JSON
- Extra fields
- Wrong enum values
- Overly verbose or unsafe output

This service solves that by enforcing **contracts** on LLM output, similar to how APIs enforce schemas.



## Core Features

- **Versioned prompts**
  - Prompts are stored and referenced by `prompt_key` and `prompt_version`
  - Old versions remain immutable for reproducibility

- **Strict schema enforcement**
  - Uses Pydantic models as the single source of truth
  - Enforces required fields, enums, length limits
  - Forbids extra keys

- **Deterministic retry and repair**
  - Automatically retries failed generations
  - Feeds validation errors back to the model for correction
  - Hard fails after a fixed number of attempts

- **Observability**
  - Trace IDs per request
  - Logs prompt versions, validation failures, and latency
  - Easy to extend with OpenTelemetry

- **Pluggable LLM backend**
  - Currently implemented with Groq
  - Can be swapped without touching core logic



## Example Use Case: Support Ticket Triage

Input:
- Free-form customer message

Output (guaranteed):
- Categorized ticket
- Priority and sentiment
- Routing decision
- Action checklist
- Customer reply draft
- Compliance signals

This makes the service usable as a standalone API for any support system.

