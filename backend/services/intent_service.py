import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def detect_intent_llm(text: str) -> str:
    prompt = f"""
    Classify the user input.

    Return JSON ONLY like:
    {{"intent": "task"}}

    Allowed intents:
    task, event, plan, note, unknown

    Input: "{text}"
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw = response.text.strip()

        print("RAW:", raw)  # debug

        # Remove markdown ```json ```
        raw = re.sub(r"```json|```", "", raw).strip()

        # Parse JSON safely
        data = json.loads(raw)
        intent = data.get("intent", "").lower()

        if intent in ["task", "event", "note", "plan"]:
            return intent

    except Exception as e:
        print("LLM error:", e)

    return "unknown"
