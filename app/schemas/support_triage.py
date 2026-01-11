from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

Category = Literal[
    "Billing",
    "Login",
    "Bug",
    "FeatureRequest",
    "Account",
    "Performance",
    "Security",
    "Other",
]

Priority = Literal["P0", "P1", "P2", "P3"]
Sentiment = Literal["Angry", "Frustrated", "Neutral", "Positive"]
Team = Literal["Support", "Engineering", "Billing", "Security"]
Language = Literal["en", "es", "fr", "de", "hi", "other"]

class Ticket(StrictBaseModel):
    title: str = Field(min_length=1, max_length=80)
    summary: str = Field(min_length=1, max_length=240)
    category: Category
    priority: Priority
    sentiment: Sentiment
    language: Language

class Routing(StrictBaseModel):
    team: Team
    tags: list[str] = Field(default_factory=list, max_length=12)
    needs_human: bool

class Actions(StrictBaseModel):
    checklist: list[str] = Field(default_factory=list, max_length=8)

class ReplyDraft(StrictBaseModel):
    short_reply: str = Field(min_length=1, max_length=280)
    long_reply: str = Field(min_length=1, max_length=1200)

class Compliance(StrictBaseModel):
    pii_detected: bool
    pii_fields: list[Literal["email", "phone", "address", "card", "ssn", "other"]] = Field(default_factory=list)

class SupportTriageOutput(StrictBaseModel):
    trace_id: str
    ticket: Ticket
    routing: Routing
    actions: Actions
    reply_draft: ReplyDraft
    compliance: Compliance
