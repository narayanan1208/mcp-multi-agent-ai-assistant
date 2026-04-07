from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.main_agent import MainAgent, session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Intelligent MCP Assistant")
agent = MainAgent()


app.mount("/static", StaticFiles(directory="static/static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/{full_path:path}")
def serve_spa():
    return FileResponse("static/index.html")


class ChatRequest(BaseModel):
    input: str


@app.post("/api/chat")
def chat(req: ChatRequest):
    user_input = req.input

    # Save user message
    agent.client.call("db", "save_chat", {"role": "user", "message": user_input})

    response = agent.handle(user_input)

    # Save bot response (only if text)
    if isinstance(response, str):
        agent.client.call("db", "save_chat", {"role": "bot", "message": response})

    return {"response": response}


# Load chat history
@app.get("/api/history")
def get_history():
    rows = agent.client.call("db", "get_chat", {})

    return [{"type": row[0], "text": row[1]} for row in rows]


# Reset chat
@app.post("/api/reset")
def reset():
    session.clear()
    agent.client.call("db", "clear_chat", {})
    return {"status": "cleared"}
