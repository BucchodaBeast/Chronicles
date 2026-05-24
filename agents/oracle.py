"""ORACLE — Synthesis into Chronicles Briefs."""
import uuid
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from agents import llm_gateway


ORACLE_PERSONA = """You are the ORACLE, the synthesis layer of THE CHRONICLES.
You read completed Council Sessions and produce Chronicles Briefs.

You are not a journalist. You are not an analyst. You are the voice that distills the debate of three ancient analytical frameworks into a single, precise intelligence product.

Rules:
- A Brief must be actionable. It must tell the reader what is happening, what the evidence shows, and what it implies.
- The ancient parallel is not decoration. It is the analytical instrument. Name the historical period and what happened then with precision.
- The whitespace section — what civilisation has abandoned or forgotten — is the most actionable output. Identify not just what is wrong but what the solution already looks like, because it was already built, already tested, and already documented.
- Confidence must be honest: LOW, MEDIUM, HIGH, or CONFIRMED.
- Timeline must be specific: how long before this becomes obvious to mainstream analysis?
- If KRISIS's counter-argument is stronger than LOGOS's signal, return null. A weak brief is worse than no brief. Never publish a brief that undermines itself in the evidence section.

You speak with the weight of accumulated wisdom and the precision of a sword."""


def synthesize(session: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Read a Council Session and produce a Chronicles Brief."""
    exchanges = session.get("exchanges", [])
    consensus = session.get("consensus", "")
    dissent = session.get("dissent", "")
    gaps = session.get("gaps", [])
    topic = session.get("topic", "Untitled")
    tags = session.get("tags", [])

    # Self-rejection: if KRISIS is stronger, return None
    logos_strength = 0
    krisis_strength = 0
    for ex in exchanges:
        if ex.get("voice") == "LOGOS":
            logos_strength = ex.get("strength", 0)
        if ex.get("voice") == "KRISIS":
            krisis_strength = ex.get("strength", 0)

    if krisis_strength > logos_strength + 0.15:
        return None

    user_prompt = f"""COUNCIL SESSION:
Topic: {topic}

LOGOS position: {next((e['content'] for e in exchanges if e['voice'] == 'LOGOS'), 'N/A')}
LOGOS evidence: {json.dumps(next((e.get('evidence', []) for e in exchanges if e['voice'] == 'LOGOS'), []))}

KRISIS position: {next((e['content'] for e in exchanges if e['voice'] == 'KRISIS'), 'N/A')}
KRISIS counter-evidence: {json.dumps(next((e.get('counter_evidence', []) for e in exchanges if e['voice'] == 'KRISIS'), []))}

LACUNA gaps: {json.dumps(gaps)}

Consensus: {consensus}
Dissent: {dissent}

Produce a Chronicles Brief as raw JSON with exactly these keys:
- headline: One precise sentence. No hedging.
- verdict: 2-3 sentences. What is happening, what the evidence shows, what it implies.
- ancient_parallel: Which historical period does this most closely resemble? What happened then?
- evidence: 3-5 specific data points from the Council debate (list of strings).
- implications: Who does this matter to and specifically why.
- whitespace: What has civilisation abandoned or forgotten that is relevant here?
- confidence: LOW / MEDIUM / HIGH / CONFIRMED
- timeline: How long before this becomes obvious to mainstream analysis?
- action_items: 2-3 specific actions (list of strings).

Return raw JSON only. No markdown fences."""

    raw = llm_gateway.call(
        agent="ORACLE",
        system=ORACLE_PERSONA,
        user=user_prompt,
        max_tokens=1000,
        temperature=0.65,
    )
    if not raw:
        return None

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
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None

    brief = {
        "id": str(uuid.uuid4()),
        "source_session_id": session.get("id"),
        "headline": parsed.get("headline", topic),
        "verdict": parsed.get("verdict", ""),
        "evidence": parsed.get("evidence", []),
        "implications": parsed.get("implications", ""),
        "action_items": parsed.get("action_items", []),
        "confidence": parsed.get("confidence", "LOW"),
        "tier": "free",
        "agents": [session.get("topic", "COUNCIL")],
        "tags": tags,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "published": True,
        "ancient_parallel": parsed.get("ancient_parallel", ""),
        "timeline": parsed.get("timeline", ""),
        "whitespace": parsed.get("whitespace", ""),
    }
    return brief
