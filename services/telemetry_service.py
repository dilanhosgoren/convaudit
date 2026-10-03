import os
import sqlite3
from typing import Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "convaudit.db")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_telemetry_tables() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                user_id INTEGER,
                email TEXT,
                meta_json TEXT DEFAULT '{}',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context TEXT NOT NULL,
                error_text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry_metrics (
                metric_key TEXT PRIMARY KEY,
                metric_value INTEGER NOT NULL DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def log_event(event_name: str, user_id: int | None = None, email: str | None = None, meta_json: str = "{}") -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO telemetry_events (event_name, user_id, email, meta_json)
            VALUES (?, ?, ?, ?)
            """,
            (event_name, user_id, email, meta_json or "{}"),
        )
        conn.commit()
    finally:
        conn.close()


def log_error(context: str, error_text: str) -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO telemetry_errors (context, error_text)
            VALUES (?, ?)
            """,
            ((context or "unknown").strip() or "unknown", (error_text or "-").strip() or "-"),
        )
        conn.commit()
    finally:
        conn.close()


def increment_metric(metric_key: str, amount: int = 1) -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO telemetry_metrics (metric_key, metric_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(metric_key) DO UPDATE SET
                metric_value = metric_value + excluded.metric_value,
                updated_at = CURRENT_TIMESTAMP
            """,
            ((metric_key or "").strip(), int(amount or 0)),
        )
        conn.commit()
    finally:
        conn.close()


def get_metrics_map() -> dict[str, int]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT metric_key, metric_value
            FROM telemetry_metrics
            """
        ).fetchall()
    finally:
        conn.close()
    return {str(r["metric_key"]): int(r["metric_value"] or 0) for r in rows}


def get_error_context_counts(limit: int = 5) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT context, COUNT(*) AS cnt
            FROM telemetry_errors
            GROUP BY context
            ORDER BY cnt DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def get_recent_errors(limit: int = 8) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT context, error_text, created_at
            FROM telemetry_errors
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def clear_telemetry() -> None:
    conn = _connect()
    try:
        conn.execute("DELETE FROM telemetry_events")
        conn.execute("DELETE FROM telemetry_errors")
        conn.execute("DELETE FROM telemetry_metrics")
        conn.commit()
    finally:
        conn.close()
