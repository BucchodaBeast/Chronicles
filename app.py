"""THE CHRONICLES — Flask app, scheduler, convergence/divergence."""
import os
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

from flask import Flask, jsonify, request, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler

from database import (
    init_db,
    insert_dispatch,
    get_recent_dispatches,
    insert_council_session,
    get_unprocessed_sessions,
    mark_session_processed,
    insert_brief,
    get_briefs,
    get_stats,
    get_seen_items,
)

from agents.solomon import SolomonAgent
from agents.daniel import DanielAgent
from agents.amos import AmosAgent
from agents.ruth import RuthAgent
from agents.john import JohnAgent
from agents.augustine import AugustineAgent
from agents.marcus_aurelius import MarcusAureliusAgent
from agents.hildegard import HildegardAgent
from agents.council import debate_dispatch
from agents.oracle import synthesize

app = Flask(__name__)

# ============================================================
# AGENT REGISTRY
# ============================================================
AGENTS = {
    "SOLOMON": SolomonAgent(),
    "DANIEL": DanielAgent(),
    "AMOS": AmosAgent(),
    "RUTH": RuthAgent(),
    "JOHN": JohnAgent(),
    "AUGUSTINE": AugustineAgent(),
    "MARCUS_AURELIUS": MarcusAureliusAgent(),
    "HILDEGARD": HildegardAgent(),
}

# ============================================================
# TERRITORY GROUPS & DIVERGENT PAIRS
# ============================================================
TERRITORY_GROUPS = {
    "economic": {"SOLOMON", "AMOS"},
    "geopolitical": {"DANIEL", "MARCUS_AURELIUS"},
    "social": {"RUTH", "HILDEGARD"},
    "systemic": {"JOHN", "AUGUSTINE"},
}

DIVERGENT_PAIRS = [
    ("SOLOMON", "AMOS"),
    ("DANIEL", "JOHN"),
    ("MARCUS_AURELIUS", "AUGUSTINE"),
    ("RUTH", "AMOS"),
]

# ============================================================
# CONVERGENCE / DIVERGENCE DETECTION
# ============================================================
HIGH_SIGNAL_KEYWORDS = {
    "wealth_concentration": ["wealth", "inequality", "concentration", "gini", "ceo pay", "top 1%"],
    "imperial_transition": ["reserve currency", "dollar", "brics", "military spending", "hegemon", "superpower"],
    "extraction_economy": ["gig economy", "wage", "rent", "housing", "medical debt", "private equity"],
    "social_collapse": ["trust", "loneliness", "meaning", "despair", "suicide", "overdose"],
    "totalising_control": ["surveillance", "cbdc", "facial recognition", "esg", "platform", "algorithm"],
    "ecological_collapse": ["biodiversity", "extinction", "soil", "climate", "pollution", "microbiome"],
    "governance_failure": ["corruption", "governance", "accountability", "emergency powers", "procurement"],
}


def _extract_keywords(text: str) -> set:
    return set(text.lower().split())


def _topic_match(d1: Dict[str, Any], d2: Dict[str, Any]) -> Optional[str]:
    """Check if two dispatches share a high-signal keyword cluster."""
    text1 = (d1.get("headline", "") + " " + d1.get("body", "")).lower()
    text2 = (d2.get("headline", "") + " " + d2.get("body", "")).lower()
    for topic, keywords in HIGH_SIGNAL_KEYWORDS.items():
        hits1 = sum(1 for k in keywords if k in text1)
        hits2 = sum(1 for k in keywords if k in text2)
        if hits1 >= 2 and hits2 >= 2:
            return topic
    return None


def _territory(agent_name: str) -> Optional[str]:
    for territory, members in TERRITORY_GROUPS.items():
        if agent_name in members:
            return territory
    return None


def detect_convergence(dispatches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect when 3+ agents from different territory groups flag same phenomenon."""
    alerts = []
    n = len(dispatches)
    for i in range(n):
        for j in range(i + 1, n):
            d1, d2 = dispatches[i], dispatches[j]
            t1, t2 = _territory(d1.get("agent", "")), _territory(d2.get("agent", ""))
            if not t1 or not t2 or t1 == t2:
                continue
            topic = _topic_match(d1, d2)
            if not topic:
                continue
            # Need 3+ agents total, different territories
            matched = [d1, d2]
            for k in range(j + 1, n):
                d3 = dispatches[k]
                t3 = _territory(d3.get("agent", ""))
                if t3 and t3 not in {t1, t2}:
                    if _topic_match(d1, d3) == topic:
                        matched.append(d3)
            if len(matched) >= 3:
                agents_involved = list({d.get("agent") for d in matched})
                alert = {
                    "id": str(uuid.uuid4()),
                    "type": "convergence_alert",
                    "agent": "SYSTEM",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "body": f"Convergence detected across {len(agents_involved)} agents from different territories on topic: {topic}.\n\n" + "\n\n".join(
                        f"[{d.get('agent')}] {d.get('headline', '')}\n{d.get('body', '')[:300]}..." for d in matched
                    ),
                    "headline": f"CONVERGENCE ALERT: {topic.replace('_', ' ').title()}",
                    "tags": ["convergence", topic],
                    "mentions": agents_involved,
                    "reactions": {},
                    "sil_score": max(d.get("sil_score", 0) for d in matched),
                    "dimensions": {},
                    "raw_data": {"matched_ids": [d.get("id") for d in matched]},
                    "published": True,
                }
                alerts.append(alert)
    return alerts


def detect_divergence(dispatches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect when two agents from complementary domains reach opposing conclusions."""
    debates = []
    n = len(dispatches)
    for i in range(n):
        for j in range(i + 1, n):
            d1, d2 = dispatches[i], dispatches[j]
            a1, a2 = d1.get("agent", ""), d2.get("agent", "")
            pair = tuple(sorted([a1, a2]))
            if pair not in [tuple(sorted(p)) for p in DIVERGENT_PAIRS]:
                continue
            topic = _topic_match(d1, d2)
            if not topic:
                continue
            # Check for genuine content overlap (not just tag overlap)
            body1, body2 = d1.get("body", "").lower(), d2.get("body", "").lower()
            shared_words = set(body1.split()) & set(body2.split())
            if len(shared_words) < 5:
                continue
            # Create a divergence debate session
            session = {
                "id": str(uuid.uuid4()),
                "source_dispatch_id": d1.get("id"),
                "topic": f"DIVERGENCE: {topic.replace('_', ' ').title()}",
                "exchanges": [
                    {"voice": a1, "content": d1.get("body", ""), "headline": d1.get("headline", ""), "strength": d1.get("sil_score", 0)},
                    {"voice": a2, "content": d2.get("body", ""), "headline": d2.get("headline", ""), "strength": d2.get("sil_score", 0)},
                ],
                "consensus": None,
                "dissent": f"Fundamental tension between {a1} and {a2} on {topic}.",
                "gaps": ["Requires Council debate to resolve."],
                "tags": ["divergence", topic],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "processed": False,
            }
            debates.append(session)
    return debates


# ============================================================
# SCHEDULER
# ============================================================
scheduler = BackgroundScheduler()


def _run_agent(agent_name: str):
    agent = AGENTS.get(agent_name)
    if not agent:
        return
    try:
        dispatches = agent.run()
        for d in dispatches:
            insert_dispatch(d)
            # Auto-debate high-signal dispatches
            if d.get("sil_score", 0) >= 0.65:
                session = debate_dispatch(d)
                if session:
                    insert_council_session(session)
    except Exception as e:
        print(f"Agent {agent_name} error: {e}")


def _run_convergence_check():
    try:
        recent = get_recent_dispatches(limit=50)
        alerts = detect_convergence(recent)
        for alert in alerts:
            insert_dispatch(alert)
        debates = detect_divergence(recent)
        for session in debates:
            insert_council_session(session)
    except Exception as e:
        print(f"Convergence check error: {e}")


def _run_oracle():
    try:
        sessions = get_unprocessed_sessions()
        for session in sessions:
            brief = synthesize(session)
            if brief:
                insert_brief(brief)
            mark_session_processed(session.get("id"))
    except Exception as e:
        print(f"Oracle error: {e}")


# Schedule offsets (minutes from startup)
scheduler.add_job(lambda: _run_agent("SOLOMON"), "interval", hours=3, id="solomon")
scheduler.add_job(lambda: _run_agent("DANIEL"), "interval", hours=2, id="daniel")
scheduler.add_job(lambda: _run_agent("AMOS"), "interval", hours=3, id="amos")
scheduler.add_job(lambda: _run_agent("RUTH"), "interval", hours=4, id="ruth")
scheduler.add_job(lambda: _run_agent("JOHN"), "interval", hours=3, id="john")
scheduler.add_job(lambda: _run_agent("AUGUSTINE"), "interval", hours=4, id="augustine")
scheduler.add_job(lambda: _run_agent("MARCUS_AURELIUS"), "interval", hours=3, id="marcus")
scheduler.add_job(lambda: _run_agent("HILDEGARD"), "interval", hours=6, id="hildegard")
scheduler.add_job(_run_convergence_check, "interval", hours=4, id="convergence")
scheduler.add_job(_run_oracle, "interval", hours=4, id="oracle")

# ============================================================
# FLASK ROUTES
# ============================================================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")


@app.route("/api/dispatches")
def api_dispatches():
    agent = request.args.get("agent")
    limit = int(request.args.get("limit", 50))
    items = get_recent_dispatches(agent=agent, limit=limit)
    return jsonify(items)


@app.route("/api/briefs")
def api_briefs():
    limit = int(request.args.get("limit", 20))
    items = get_briefs(limit=limit, published_only=True)
    return jsonify(items)


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


@app.route("/api/agents")
def api_agents():
    result = []
    for name, agent in AGENTS.items():
        result.append({
            "name": agent.name,
            "era": agent.era,
            "analytical_lens": agent.analytical_lens,
            "color": agent.color,
            "territory": _territory(name),
        })
    return jsonify(result)


@app.route("/api/trigger/<agent_name>", methods=["POST"])
def trigger_agent(agent_name: str):
    """Manual trigger for testing."""
    if agent_name.upper() in AGENTS:
        _run_agent(agent_name.upper())
        return jsonify({"status": "triggered", "agent": agent_name.upper()})
    return jsonify({"error": "Unknown agent"}), 404


@app.route("/api/convergence")
def api_convergence():
    recent = get_recent_dispatches(limit=100)
    alerts = [d for d in recent if d.get("type") == "convergence_alert"]
    return jsonify(alerts[:20])


@app.route("/api/divergence")
def api_divergence():
    """Return recent divergence sessions."""
    # For simplicity, return recent council sessions with DIVERGENCE in topic
    from database import _get_sqlite
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM council_sessions WHERE topic LIKE 'DIVERGENCE:%' ORDER BY created_at DESC LIMIT 20"
    )
    rows = [dict(row) for row in cursor.fetchall()]
    for r in rows:
        for field in ("exchanges", "gaps", "tags"):
            try:
                r[field] = json.loads(r[field])
            except Exception:
                r[field] = []
    conn.close()
    return jsonify(rows)


@app.route("/api/sessions")
def api_sessions():
    """Return recent council sessions."""
    from database import _get_sqlite
    conn = _get_sqlite()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM council_sessions ORDER BY created_at DESC LIMIT 30"
    )
    rows = [dict(row) for row in cursor.fetchall()]
    for r in rows:
        for field in ("exchanges", "gaps", "tags"):
            try:
                r[field] = json.loads(r[field])
            except Exception:
                r[field] = []
    conn.close()
    return jsonify(rows)


# ============================================================
# INIT
# ============================================================
@app.before_request
def before_first_request():
    init_db()


if __name__ == "__main__":
    init_db()
    scheduler.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
