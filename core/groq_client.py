import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
class GroqLLM:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def chat_json(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Return only a single JSON object. No extra text.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_completion_tokens=900,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content or "{}"
