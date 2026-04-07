import sqlite3


class DBTool:
    def __init__(self):
        self.conn = sqlite3.connect("assistant.db", check_same_thread=False)
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT,date TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS events (event TEXT,date TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS notes (note TEXT,date TEXT)")
        c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT
        )
        """)
        self.conn.commit()

    def execute(self, a, p):
        c = self.conn.cursor()
        if a == "save_task":
            c.execute("INSERT INTO tasks VALUES (?,?)", (p["task"], p["date"]))
        elif a == "save_event":
            c.execute("INSERT INTO events VALUES (?,?)", (p["event"], p["date"]))
        elif a == "save_note":
            c.execute("INSERT INTO notes VALUES (?,?)", (p["note"], p["date"]))
        elif a == "get_dates":
            t = c.execute("SELECT DISTINCT date FROM tasks").fetchall()
            e = c.execute("SELECT DISTINCT date FROM events").fetchall()
            n = c.execute("SELECT DISTINCT date FROM notes").fetchall()
            return list(set([x[0] for x in t + e + n]))
        elif a == "get_tasks_by_date":
            return c.execute(
                "SELECT task FROM tasks WHERE date=?", (p["date"],)
            ).fetchall()
        elif a == "get_events_by_date":
            return c.execute(
                "SELECT event FROM events WHERE date=?", (p["date"],)
            ).fetchall()
        elif a == "get_notes_by_date":
            return c.execute(
                "SELECT note FROM notes WHERE date=?", (p["date"],)
            ).fetchall()
        elif a == "save_chat":
            c.execute(
                "INSERT INTO chat_history (role, message) VALUES (?, ?)",
                (p["role"], p["message"]),
            )
        elif a == "get_chat":
            return c.execute(
                "SELECT role, message FROM chat_history ORDER BY id"
            ).fetchall()
        elif a == "clear_chat":
            c.execute("DELETE FROM chat_history")
        self.conn.commit()
        return {"ok": True}
