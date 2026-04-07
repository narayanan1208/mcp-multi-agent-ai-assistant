from mcp.client import MCPClient
from mcp.setup import setup_mcp


class PlannerAgent:
    def __init__(self):
        self.client = MCPClient(setup_mcp())

    def handle_by_date(self, d):
        t = self.client.call("db", "get_tasks_by_date", {"date": d})
        e = self.client.call("db", "get_events_by_date", {"date": d})
        n = self.client.call("db", "get_notes_by_date", {"date": d})

        response = f"📅 Plan for {d}\n\n"

        # Events
        if e:
            response += "🗓 Events:\n"
            for x in e:
                response += f"- {x[0]}\n"
            response += "\n"

        # Tasks
        if t:
            response += "✅ Tasks:\n"
            for x in t:
                response += f"- {x[0]}\n"

        # Notes
        if n:
            response += "\n📝 Notes:\n"
            for x in n:
                response += f"- {x[0]}\n"

        return response.strip()
