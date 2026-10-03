import json
import json
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


def init_history_tables() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                audit_type TEXT NOT NULL,
                target TEXT NOT NULL,
                lang TEXT NOT NULL,
                overall_score INTEGER DEFAULT 0,
                improvement_range TEXT DEFAULT '-',
                priority_focus TEXT DEFAULT '-',
                summary TEXT DEFAULT '',
                analysis_level TEXT NOT NULL DEFAULT 'full',
                payload_json TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        cols = conn.execute("PRAGMA table_info(analysis_history)").fetchall()
        col_names = {c[1] for c in cols}
        if "analysis_level" not in col_names:
            conn.execute("ALTER TABLE analysis_history ADD COLUMN analysis_level TEXT NOT NULL DEFAULT 'full'")
        if "criteria_json" not in col_names:
            conn.execute("ALTER TABLE analysis_history ADD COLUMN criteria_json TEXT")
        conn.commit()
    finally:
        conn.close()


def save_analysis(
    user_id: int,
    audit_type: str,
    target: str,
    lang: str,
    audit_data: dict,
    analysis_level: str = "full",
) -> int:
    scores = audit_data.get("scores", {})
    impact = audit_data.get("impact", {})
    criteria = audit_data.get("criteria", {})

    conn = _connect()
    try:
        cursor = conn.execute(
            """
            INSERT INTO analysis_history (
                user_id, audit_type, target, lang,
                overall_score, improvement_range, priority_focus, summary,
                analysis_level, payload_json, criteria_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                audit_type,
                (target or "-").strip(),
                lang,
                int(scores.get("overall", 0) or 0),
                impact.get("improvement_range", "-"),
                impact.get("priority_focus", "-"),
                audit_data.get("summary", ""),
                (analysis_level or "full").strip().lower(),
                json.dumps(audit_data, ensure_ascii=False),
                json.dumps(criteria, ensure_ascii=False) if criteria else None,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)
    finally:
        conn.close()


def get_user_history(
    user_id: int,
    limit: int = 20,
    analysis_level: str | None = None,
) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        if analysis_level in {"preview", "full"}:
            rows = conn.execute(
                """
                SELECT id, audit_type, target, lang, overall_score, improvement_range,
                       priority_focus, summary, analysis_level, created_at
                FROM analysis_history
                WHERE user_id = ? AND analysis_level = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, analysis_level, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, audit_type, target, lang, overall_score, improvement_range,
                       priority_focus, summary, analysis_level, created_at
                FROM analysis_history
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
    finally:
        conn.close()

    return [dict(row) for row in rows]


def get_history_detail(history_id: int, user_id: int) -> dict[str, Any] | None:
    conn = _connect()
    try:
        row = conn.execute(
            """
            SELECT id, audit_type, target, lang, analysis_level, payload_json, created_at
            FROM analysis_history
            WHERE id = ? AND user_id = ?
            """,
            (history_id, user_id),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    payload = json.loads(row["payload_json"])
    result = dict(row)
    result["payload"] = payload
    return result


def get_latest_analysis_for_target(
    user_id: int,
    audit_type: str,
    target: str,
) -> dict[str, Any] | None:
    conn = _connect()
    try:
        row = conn.execute(
            """
            SELECT id, audit_type, target, lang, analysis_level, payload_json, created_at
            FROM analysis_history
            WHERE user_id = ? AND audit_type = ? AND target = ? AND analysis_level = 'full'
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id, audit_type, (target or "-").strip()),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    result = dict(row)
    result["payload"] = json.loads(row["payload_json"])
    return result


def get_previous_analysis_for_target(
    user_id: int,
    audit_type: str,
    target: str,
    current_id: int,
) -> dict[str, Any] | None:
    conn = _connect()
    try:
        row = conn.execute(
            """
            SELECT id, audit_type, target, lang, analysis_level, payload_json, created_at
            FROM analysis_history
            WHERE user_id = ? AND audit_type = ? AND target = ? AND id < ? AND analysis_level = 'full'
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id, audit_type, (target or "-").strip(), current_id),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    result = dict(row)
    result["payload"] = json.loads(row["payload_json"])
    return result


def get_target_full_history(
    user_id: int,
    audit_type: str,
    target: str,
    limit: int = 8,
) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        rows = conn.execute(
            """
            SELECT id, overall_score, created_at
            FROM analysis_history
            WHERE user_id = ? AND audit_type = ? AND target = ? AND analysis_level = 'full'
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, audit_type, (target or "-").strip(), limit),
        ).fetchall()
    finally:
        conn.close()

    return [dict(row) for row in rows]
