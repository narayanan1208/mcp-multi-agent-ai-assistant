from state.session_store import SessionStore
from mcp.client import MCPClient
from mcp.setup import setup_mcp
from agents.planner_agent import PlannerAgent
from datetime import datetime
from services.intent_service import detect_intent_llm

session = SessionStore()


def is_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except:
        return False


def is_greeting(text):
    greetings = ["hi", "hello", "hey", "hii"]
    return text.lower().strip() in greetings


def is_view_plan_intent(text: str) -> bool:
    normalized = text.lower().strip()

    if "plan" in normalized:
        return True

    if "schedule" in normalized:
        # viewing schedule, not creating event
        if "my" in normalized or "show" in normalized:
            return True

    return False


class MainAgent:
    def __init__(self):
        self.client = MCPClient(setup_mcp())

    def handle(self, text):

        # Greeting
        if is_greeting(text):
            return {
                "type": "welcome",
                "message": "Hi 👋 I'm your Smart Assistant!\nYou can type anything or choose an option below 👇",
                "options": [
                    "Add a task",
                    "Schedule an event",
                    "Add a note",
                    "Plan my day",
                ],
            }

        normalized = text.lower().strip()

        # BUTTON -> INTENT SELECTION
        button_map = {
            "add a task": "task_input",
            "schedule an event": "event_input",
            "add a note": "note_input",
        }

        # Reset session if new flow starts
        if normalized in button_map or normalized == "plan my day":
            session.clear()

        # Handle task/event/note buttons
        if normalized in button_map:
            session.set("pending", button_map[normalized])

            prompts = {
                "task_input": "What task would you like to add?",
                "event_input": "What event would you like to schedule?",
                "note_input": "What note would you like to save?",
            }

            return prompts[button_map[normalized]]

        # Handle plan button
        if normalized == "plan my day":
            dates = self.client.call("db", "get_dates", {})
            dates = sorted(dates)

            if not dates:
                return "📭 No plans found yet.\nTry adding a task or event first!"

            session.set("pending", "plan_date")
            return {"type": "date_buttons", "options": dates}

        # USER ENTERS CONTENT AFTER BUTTON
        input_to_date_map = {
            "task_input": "task_date",
            "event_input": "event_date",
            "note_input": "note_date",
        }

        if session.get("pending") in input_to_date_map:
            session.set("pending", input_to_date_map[session.get("pending")])
            session.set("content", text)
            return {"type": "date_selection"}

        # DATE HANDLING
        if session.get("pending") == "task_date" and is_date(text):
            self.client.call(
                "db", "save_task", {"task": session.get("content"), "date": text}
            )
            session.clear()
            return f"✅ Task saved for {text}"

        if session.get("pending") == "event_date" and is_date(text):
            self.client.call(
                "db", "save_event", {"event": session.get("content"), "date": text}
            )
            session.clear()
            return f"✅ Event saved for {text}"

        if session.get("pending") == "note_date" and is_date(text):
            self.client.call(
                "db", "save_note", {"note": session.get("content"), "date": text}
            )
            session.clear()
            return f"✅ Note saved for {text}"

        if session.get("pending") == "plan_date" and is_date(text):
            session.clear()
            return PlannerAgent().handle_by_date(text)

        # Global date fallback
        if is_date(text):
            return PlannerAgent().handle_by_date(text)

        # Quick keyword plan detention
        if is_view_plan_intent(text):
            dates = self.client.call("db", "get_dates", {})
            dates = sorted(dates)

            if not dates:
                return "📭 No plans found yet.\nTry adding a task or event first!"

            session.set("pending", "plan_date")
            return {"type": "date_buttons", "options": dates}

        # FALLBACK -> LLM INTENT
        intent = detect_intent_llm(text)

        intent_to_pending = {
            "task": "task_date",
            "event": "event_date",
            "note": "note_date",
        }

        if intent in intent_to_pending:
            session.set("pending", intent_to_pending[intent])
            session.set("content", text)
            return {"type": "date_selection"}

        if intent == "plan":
            dates = self.client.call("db", "get_dates", {})
            dates = sorted(dates)

            if not dates:
                return "📭 No plans found yet.\nTry adding a task or event first!"

            session.set("pending", "plan_date")
            return {"type": "date_buttons", "options": dates}

        return "Try something like 'prepare slides' or 'meeting tomorrow'"
