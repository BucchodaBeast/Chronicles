"""Dual backend: SQLite (dev) / Supabase (prod)"""
import os
import json
import sqlite3
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_SUPABASE = bool(DATABASE_URL and DATABASE_URL.startswith("postgresql"))

if USE_SUPABASE:
    from supabase import create_client, Client
    supabase: Optional[Client] = None
    try:
        url = DATABASE_URL.split("@")[1].split("/")[0]  # crude parse fallback
        key = os.environ.get("SUPABASE_KEY", "")
        if url and key:
            supabase = create_client(f"https://{url}", key)
    except Exception:
        supabase = None

DB_PATH = os.environ.get("DB_PATH", "chronicles.db")


def _get_sqlite() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist."""
    if USE_SUPABASE and supabase:
        # Supabase schema assumed managed externally or via migrations
        return
    conn = _get_sqlite()
    cursor = conn.cursor()
    tables = [
        """
        CREATE TABLE IF NOT EXISTS dispatches (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            agent TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            body TEXT NOT NULL,
            headline TEXT,
            tags TEXT DEFAULT '[]',
            mentions TEXT DEFAULT '[]',
            reactions TEXT DEFAULT '{}',
            sil_score REAL DEFAULT 0,
            dimensions TEXT DEFAULT '{}',
            raw_data TEXT DEFAULT '{}',
            published BOOLEAN DEFAULT TRUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS seen_items (
            id TEXT PRIMARY KEY,
            agent TEXT NOT NULL,
            seen_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS council_sessions (
            id TEXT PRIMARY KEY,
            source_dispatch_id TEXT,
            topic TEXT,
            exchanges TEXT DEFAULT '[]',
            consensus TEXT,
            dissent TEXT,
            gaps TEXT DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            processed BOOLEAN DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS briefs (
            id TEXT PRIMARY KEY,
            source_session_id TEXT,
            headline TEXT,
            verdict TEXT,
            evidence TEXT DEFAULT '[]',
            implications TEXT,
            action_items TEXT DEFAULT '[]',
            confidence TEXT,
            tier TEXT DEFAULT 'free',
            agents TEXT DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL,
            published BOOLEAN DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS agent_runs (
            id TEXT PRIMARY KEY,
            agent TEXT NOT NULL,
            run_at TEXT NOT NULL,
            items_fetched INTEGER DEFAULT 0,
            items_passed_gate INTEGER DEFAULT 0,
            posts_produced INTEGER DEFAULT 0
        )
        """,
    ]
    for sql in tables:
        cursor.execute(sql)
    conn.commit()
    conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def insert_dispatch(data: Dict[str, Any]) -> None:
    if USE_SUPABASE and supabase:
        try:
            supabase.table("dispatches").insert(data).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO dispatches
        (id, type, agent, timestamp, body, headline, tags, mentions, reactions, sil_score, dimensions, raw_data, published)
        VALUES (:id, :type, :agent, :timestamp, :body, :headline, :tags, :mentions, :reactions, :sil_score, :dimensions, :raw_data, :published)
        """,
        {
            "id": data.get("id"),
            "type": data.get("type", "dispatch"),
            "agent": data.get("agent", ""),
            "timestamp": data.get("timestamp", _now()),
            "body": data.get("body", ""),
            "headline": data.get("headline"),
            "tags": json.dumps(data.get("tags", [])),
            "mentions": json.dumps(data.get("mentions", [])),
            "reactions": json.dumps(data.get("reactions", {})),
            "sil_score": data.get("sil_score", 0),
            "dimensions": json.dumps(data.get("dimensions", {})),
            "raw_data": json.dumps(data.get("raw_data", {})),
            "published": data.get("published", True),
        },
    )
    conn.commit()
    conn.close()


def insert_seen_item(item_id: str, agent: str) -> None:
    if USE_SUPABASE and supabase:
        try:
            supabase.table("seen_items").insert({"id": item_id, "agent": agent, "seen_at": _now()}).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO seen_items (id, agent, seen_at) VALUES (?, ?, ?)",
        (item_id, agent, _now()),
    )
    conn.commit()
    conn.close()


def get_seen_items(agent: str) -> List[str]:
    if USE_SUPABASE and supabase:
        try:
            resp = supabase.table("seen_items").select("id").eq("agent", agent).execute()
            return [r["id"] for r in resp.data] if resp.data else []
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM seen_items WHERE agent = ?", (agent,))
    rows = [row["id"] for row in cursor.fetchall()]
    conn.close()
    return rows


def get_recent_dispatches(agent: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    if USE_SUPABASE and supabase:
        try:
            q = supabase.table("dispatches").select("*").order("timestamp", desc=True).limit(limit)
            if agent:
                q = q.eq("agent", agent)
            resp = q.execute()
            return resp.data if resp.data else []
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    if agent:
        cursor.execute(
            "SELECT * FROM dispatches WHERE agent = ? ORDER BY timestamp DESC LIMIT ?",
            (agent, limit),
        )
    else:
        cursor.execute("SELECT * FROM dispatches ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    for r in rows:
        for field in ("tags", "mentions", "reactions", "dimensions", "raw_data"):
            try:
                r[field] = json.loads(r[field])
            except Exception:
                r[field] = {} if field in ("reactions", "dimensions", "raw_data") else []
    conn.close()
    return rows


def insert_council_session(data: Dict[str, Any]) -> None:
    if USE_SUPABASE and supabase:
        try:
            supabase.table("council_sessions").insert(data).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO council_sessions
        (id, source_dispatch_id, topic, exchanges, consensus, dissent, gaps, tags, created_at, processed)
        VALUES (:id, :source_dispatch_id, :topic, :exchanges, :consensus, :dissent, :gaps, :tags, :created_at, :processed)
        """,
        {
            "id": data.get("id"),
            "source_dispatch_id": data.get("source_dispatch_id"),
            "topic": data.get("topic"),
            "exchanges": json.dumps(data.get("exchanges", [])),
            "consensus": data.get("consensus"),
            "dissent": data.get("dissent"),
            "gaps": json.dumps(data.get("gaps", [])),
            "tags": json.dumps(data.get("tags", [])),
            "created_at": data.get("created_at", _now()),
            "processed": data.get("processed", False),
        },
    )
    conn.commit()
    conn.close()


def get_unprocessed_sessions() -> List[Dict[str, Any]]:
    if USE_SUPABASE and supabase:
        try:
            resp = supabase.table("council_sessions").select("*").eq("processed", False).execute()
            return resp.data if resp.data else []
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM council_sessions WHERE processed = FALSE ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    for r in rows:
        for field in ("exchanges", "gaps", "tags"):
            try:
                r[field] = json.loads(r[field])
            except Exception:
                r[field] = []
    conn.close()
    return rows


def mark_session_processed(session_id: str) -> None:
    if USE_SUPABASE and supabase:
        try:
            supabase.table("council_sessions").update({"processed": True}).eq("id", session_id).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute("UPDATE council_sessions SET processed = TRUE WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


def insert_brief(data: Dict[str, Any]) -> None:
    if USE_SUPABASE and supabase:
        try:
            supabase.table("briefs").insert(data).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO briefs
        (id, source_session_id, headline, verdict, evidence, implications, action_items, confidence, tier, agents, tags, created_at, published)
        VALUES (:id, :source_session_id, :headline, :verdict, :evidence, :implications, :action_items, :confidence, :tier, :agents, :tags, :created_at, :published)
        """,
        {
            "id": data.get("id"),
            "source_session_id": data.get("source_session_id"),
            "headline": data.get("headline"),
            "verdict": data.get("verdict"),
            "evidence": json.dumps(data.get("evidence", [])),
            "implications": data.get("implications"),
            "action_items": json.dumps(data.get("action_items", [])),
            "confidence": data.get("confidence"),
            "tier": data.get("tier", "free"),
            "agents": json.dumps(data.get("agents", [])),
            "tags": json.dumps(data.get("tags", [])),
            "created_at": data.get("created_at", _now()),
            "published": data.get("published", False),
        },
    )
    conn.commit()
    conn.close()


def get_briefs(limit: int = 20, published_only: bool = True) -> List[Dict[str, Any]]:
    if USE_SUPABASE and supabase:
        try:
            q = supabase.table("briefs").select("*").order("created_at", desc=True).limit(limit)
            if published_only:
                q = q.eq("published", True)
            resp = q.execute()
            return resp.data if resp.data else []
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    if published_only:
        cursor.execute("SELECT * FROM briefs WHERE published = TRUE ORDER BY created_at DESC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT * FROM briefs ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    for r in rows:
        for field in ("evidence", "action_items", "agents", "tags"):
            try:
                r[field] = json.loads(r[field])
            except Exception:
                r[field] = []
    conn.close()
    return rows


def log_agent_run(agent: str, fetched: int = 0, passed: int = 0, produced: int = 0) -> None:
    import uuid
    data = {
        "id": str(uuid.uuid4()),
        "agent": agent,
        "run_at": _now(),
        "items_fetched": fetched,
        "items_passed_gate": passed,
        "posts_produced": produced,
    }
    if USE_SUPABASE and supabase:
        try:
            supabase.table("agent_runs").insert(data).execute()
            return
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agent_runs (id, agent, run_at, items_fetched, items_passed_gate, posts_produced) VALUES (?, ?, ?, ?, ?, ?)",
        (data["id"], data["agent"], data["run_at"], data["items_fetched"], data["items_passed_gate"], data["posts_produced"]),
    )
    conn.commit()
    conn.close()


def get_stats() -> Dict[str, Any]:
    """Return weekly aggregate stats for UI."""
    if USE_SUPABASE and supabase:
        try:
            # Fallback simplified
            return {
                "dispatches_7d": 0,
                "convergences_7d": 0,
                "briefs_7d": 0,
                "last_run": _now(),
            }
        except Exception:
            pass
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM dispatches WHERE timestamp > datetime('now', '-7 days')"
    )
    dispatches_7d = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM dispatches WHERE type = 'convergence_alert' AND timestamp > datetime('now', '-7 days')"
    )
    convergences_7d = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM briefs WHERE created_at > datetime('now', '-7 days')"
    )
    briefs_7d = cursor.fetchone()[0]
    cursor.execute("SELECT MAX(run_at) FROM agent_runs")
    row = cursor.fetchone()
    last_run = row[0] if row and row[0] else _now()
    conn.close()
    return {
        "dispatches_7d": dispatches_7d,
        "convergences_7d": convergences_7d,
        "briefs_7d": briefs_7d,
        "last_run": last_run,
    }
