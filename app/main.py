from fastapi import FastAPI
from app.api.generate import router as generate_router

app = FastAPI(title="LLM Prompt and Output Validation Service")

app.include_router(generate_router)

@app.get("/health")
def health():
    return {"ok": True}
