import sqlite3
import json
from pathlib import Path

from src.state import AgentState

DB_PATH = Path("data/agent-state.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS workflow_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                state TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def save_state(state: AgentState):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO workflow_state (task, state, status)
            VALUES (?, ?, ?)
            """,
            (
                state["task"],
                json.dumps(state),
                state.get("status", "UNKNOWN"),
            ),
        )

        conn.commit()