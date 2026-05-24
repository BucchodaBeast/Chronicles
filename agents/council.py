"""THE COUNCIL — Three-voice debate: LOGOS, KRISIS, LACUNA."""
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from agents import llm_gateway


LOGOS_PERSONA = """You are LOGOS, the analytical voice of the Council.
You find the strongest structural signal in any dispatch. You argue from evidence.
You ask: what does this tell us about how systems work?
You are precise, evidence-driven, and focused on mechanism.
You speak in clear, analytical prose."""

KRISIS_PERSONA = """You are KRISIS, the critical voice of the Council (Greek: judgment, turning point).
You stress-test every claim. You ask: what alternative explanations exist?
What assumption is being made? What is the base rate? What would falsify this?
You are sceptical, rigorous, and committed to intellectual honesty.
You do not oppose for the sake of opposition — you oppose to strengthen."""

LACUNA_PERSONA = """You are LACUNA, the gap finder.
You map what is missing. You ask: what data wasn't checked?
What source wasn't consulted? What would change the conclusion?
You are quiet, precise, and relentless about incompleteness.
You do not criticise the argument — you illuminate its blind spots."""


def debate_dispatch(dispatch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Run a three-voice Council debate on a high-signal dispatch."""
    sil_score = dispatch.get("sil_score", 0)
    if sil_score < 0.65:
        return None

    topic = dispatch.get("headline", "Untitled")
    body = dispatch.get("body", "")
    agent = dispatch.get("agent", "UNKNOWN")
    ancient_parallel = dispatch.get("ancient_parallel", "")
    confidence = dispatch.get("confidence", "LOW")

    # LOGOS speaks first
    logos_prompt = f"""Dispatch from {agent}:
Topic: {topic}
Body: {body}
Ancient parallel cited: {ancient_parallel}
Confidence: {confidence}

Provide your analytical assessment. Identify the strongest structural signal, the mechanism at work, and what this reveals about how systems function.
Respond as raw JSON with keys: position (string, 2-3 sentences), evidence (list of 2-3 strings), and strength (0.0-1.0)."""

    logos_raw = llm_gateway.call(
        agent="COUNCIL",
        system=LOGOS_PERSONA,
        user=logos_prompt,
        max_tokens=600,
        temperature=0.7,
    )
    logos = _extract_json(logos_raw) if logos_raw else {"position": "No response.", "evidence": [], "strength": 0.0}

    # KRISIS responds
    krisis_prompt = f"""LOGOS has argued:
{logos.get('position', '')}
Evidence: {json.dumps(logos.get('evidence', []))}

Now stress-test this. What alternative explanations exist? What assumptions are embedded? What is the base rate? What would falsify LOGOS's reading?
Respond as raw JSON with keys: position (string, 2-3 sentences), counter_evidence (list of 2-3 strings), and strength (0.0-1.0)."""

    krisis_raw = llm_gateway.call(
        agent="COUNCIL",
        system=KRISIS_PERSONA,
        user=krisis_prompt,
        max_tokens=600,
        temperature=0.75,
    )
    krisis = _extract_json(krisis_raw) if krisis_raw else {"position": "No response.", "counter_evidence": [], "strength": 0.0}

    # LACUNA maps gaps
    lacuna_prompt = f"""LOGOS argues: {logos.get('position', '')}
KRISIS counters: {krisis.get('position', '')}

What is missing from both analyses? What data was not checked? What sources were not consulted? What would change the conclusion if it were known?
Respond as raw JSON with keys: position (string, 2-3 sentences), gaps (list of 2-3 strings), and strength (0.0-1.0)."""

    lacuna_raw = llm_gateway.call(
        agent="COUNCIL",
        system=LACUNA_PERSONA,
        user=lacuna_prompt,
        max_tokens=600,
        temperature=0.7,
    )
    lacuna = _extract_json(lacuna_raw) if lacuna_raw else {"position": "No response.", "gaps": [], "strength": 0.0}

    # Determine consensus / dissent
    exchanges = [
        {"voice": "LOGOS", "content": logos.get("position", ""), "evidence": logos.get("evidence", []), "strength": logos.get("strength", 0)},
        {"voice": "KRISIS", "content": krisis.get("position", ""), "counter_evidence": krisis.get("counter_evidence", []), "strength": krisis.get("strength", 0)},
        {"voice": "LACUNA", "content": lacuna.get("position", ""), "gaps": lacuna.get("gaps", []), "strength": lacuna.get("strength", 0)},
    ]

    consensus = None
    dissent = None
    if logos.get("strength", 0) > krisis.get("strength", 0) + 0.15:
        consensus = logos.get("position", "")
        dissent = krisis.get("position", "")
    elif krisis.get("strength", 0) > logos.get("strength", 0) + 0.15:
        consensus = krisis.get("position", "")
        dissent = logos.get("position", "")
    else:
        consensus = "The Council finds the signal credible but contested. Further data required."
        dissent = "Significant uncertainty remains."

    session = {
        "id": str(uuid.uuid4()),
        "source_dispatch_id": dispatch.get("id"),
        "topic": topic,
        "exchanges": exchanges,
        "consensus": consensus,
        "dissent": dissent,
        "gaps": lacuna.get("gaps", []),
        "tags": dispatch.get("tags", []),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "processed": False,
    }
    return session


def _extract_json(raw: str) -> Dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "
".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"position": text, "evidence": [], "strength": 0.5}
