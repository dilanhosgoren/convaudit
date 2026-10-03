import hashlib
import os
import sqlite3
import time
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "convaudit.db")


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(password: str, salt: str) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    )
    return digest.hex()


def init_auth_tables() -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                first_name TEXT DEFAULT '',
                last_name TEXT DEFAULT '',
                plan TEXT NOT NULL DEFAULT 'free',
                avatar_path TEXT DEFAULT '',
                token_version INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bridge_nonces (
                nonce TEXT PRIMARY KEY,
                exp INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cols = conn.execute("PRAGMA table_info(users)").fetchall()
        col_names = {c[1] for c in cols}
        if "plan" not in col_names:
            conn.execute("ALTER TABLE users ADD COLUMN plan TEXT NOT NULL DEFAULT 'free'")
        if "first_name" not in col_names:
            conn.execute("ALTER TABLE users ADD COLUMN first_name TEXT DEFAULT ''")
        if "last_name" not in col_names:
            conn.execute("ALTER TABLE users ADD COLUMN last_name TEXT DEFAULT ''")
        if "avatar_path" not in col_names:
            conn.execute("ALTER TABLE users ADD COLUMN avatar_path TEXT DEFAULT ''")
        if "token_version" not in col_names:
            conn.execute("ALTER TABLE users ADD COLUMN token_version INTEGER NOT NULL DEFAULT 0")
        conn.commit()
    finally:
        conn.close()


def register_user(
    email: str, password: str, first_name: str = "", last_name: str = ""
) -> tuple[bool, str]:
    normalized = (email or "").strip().lower()
    if "@" not in normalized or "." not in normalized:
        return False, "Geçerli bir e-posta girin."

    if len(password or "") < 6:
        return False, "Şifre en az 6 karakter olmalı."

    salt = os.urandom(16).hex()
    password_hash = _hash_password(password, salt)
    first_name = (first_name or "").strip()[:40]
    last_name = (last_name or "").strip()[:40]

    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash, salt, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
            (normalized, password_hash, salt, first_name, last_name),
        )
        conn.commit()
        return True, "Kayıt başarılı."
    except sqlite3.IntegrityError:
        return False, "Bu e-posta zaten kayıtlı."
    finally:
        conn.close()


def login_user(email: str, password: str) -> tuple[bool, Optional[dict], str]:
    normalized = (email or "").strip().lower()

    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, email, password_hash, salt, first_name, last_name, plan, avatar_path, token_version FROM users WHERE email = ?",
            (normalized,),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return False, None, "E-posta veya şifre hatalı."

    expected = row["password_hash"]
    actual = _hash_password(password or "", row["salt"])

    if expected != actual:
        return False, None, "E-posta veya şifre hatalı."

    return (
        True,
        {
            "id": row["id"],
            "email": row["email"],
            "first_name": row["first_name"] or "",
            "last_name": row["last_name"] or "",
            "plan": row["plan"],
            "avatar_path": row["avatar_path"] or "",
            "token_version": int(row["token_version"] or 0),
        },
        "Giriş başarılı.",
    )


def get_user_by_email(email: str) -> Optional[dict]:
    normalized = (email or "").strip().lower()
    if not normalized:
        return None

    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, email, first_name, last_name, plan, avatar_path, token_version FROM users WHERE email = ?",
            (normalized,),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "email": row["email"],
        "first_name": row["first_name"] or "",
        "last_name": row["last_name"] or "",
        "plan": row["plan"],
        "avatar_path": row["avatar_path"] or "",
        "token_version": int(row["token_version"] or 0),
    }


def get_user_account_info(user_id: int) -> Optional[dict]:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, email, first_name, last_name, plan, created_at FROM users WHERE id = ?",
            (int(user_id),),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "email": row["email"],
        "first_name": row["first_name"] or "",
        "last_name": row["last_name"] or "",
        "plan": row["plan"],
        "created_at": row["created_at"] or "",
    }


def consume_bridge_nonce(nonce: str, exp: int) -> bool:
    clean_nonce = (nonce or "").strip()
    if not clean_nonce:
        return False

    now = int(time.time())
    conn = _connect()
    try:
        conn.execute("DELETE FROM bridge_nonces WHERE exp <= ?", (now,))
        conn.execute("INSERT INTO bridge_nonces (nonce, exp) VALUES (?, ?)", (clean_nonce, int(exp)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def bump_user_token_version(user_id: int) -> None:
    conn = _connect()
    try:
        conn.execute(
            "UPDATE users SET token_version = COALESCE(token_version, 0) + 1 WHERE id = ?",
            (user_id,),
        )
        conn.commit()
    finally:
        conn.close()


def upgrade_user_plan(user_id: int, plan: str = "premium") -> None:
    conn = _connect()
    try:
        conn.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
        conn.commit()
    finally:
        conn.close()


def update_user_avatar(user_id: int, avatar_path: str) -> None:
    conn = _connect()
    try:
        conn.execute(
            "UPDATE users SET avatar_path = ? WHERE id = ?",
            (avatar_path, user_id),
        )
        conn.commit()
    finally:
        conn.close()
