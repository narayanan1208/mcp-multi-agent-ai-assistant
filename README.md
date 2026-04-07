# 🚀 MCP Multi-Agent AI Assistant

## 🧠 Overview

This project implements a **Multi-Agent AI System** powered by a lightweight implementation of the **Model Context Protocol (MCP)**.

The system intelligently manages:

* 📋 Tasks
* 📅 Schedules
* 📝 Notes

It demonstrates **agent orchestration, tool abstraction, and multi-step workflows** in a scalable and modular architecture.

---

## 🏗️ Architecture

User Input → Main Agent → MCP Client → MCP Server → Tools → Database

### 🔹 Components

* **Main Agent (Coordinator)**
  Routes user intent to appropriate sub-agents

* **Sub Agents**

  * Task Agent
  * Calendar Agent
  * Notes Agent
  * Planner Agent (multi-step workflow)

* **MCP Layer**

  * MCP Server (tool registry)
  * MCP Client (agent interface)
  * MCP Tool Interface (`execute(action, params)`)

* **Database**

  * SQLite (persistent storage for tasks, events, notes)

---

## ⚙️ Key Features

### ✅ Multi-Agent Coordination

Specialized agents collaborate to handle complex user requests.

### ✅ MCP-Based Tool Abstraction

Implements a structured interface between agents and tools:

```json
{
  "tool": "db",
  "action": "save_task",
  "params": {"task": "Prepare slides"}
}
```

### ✅ Multi-Step Workflows

Supports intelligent workflows like:

👉 **"Plan my day"**

* Fetch tasks
* Fetch events
* Combine results into a structured plan

### ✅ Modular & Extensible Design

* Easily plug in new tools (e.g., email, reminders, APIs)
* Scalable architecture using MCP principles

---

## 🧪 Demo Commands

Try these:

```
add task prepare slides
schedule meeting tomorrow at 5pm
add note buy groceries
plan my day
```

---

## 🖥️ API Usage

### Endpoint

```
POST /chat
```

### Example

```bash
curl -X POST http://localhost:8000/chat -d "input=add task finish project"
```

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## ☁️ Deployment

Deploy easily using:

* Docker
* Google Cloud Run

