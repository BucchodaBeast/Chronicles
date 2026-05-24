"""BaseAgent with pre-LLM gate, staged cognition."""
import uuid
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from agents import llm_gateway
from signal_integrity import score_signal


class BaseAgent(ABC):
    name: str = ""
    era: str = ""
    source_texts: List[str] = []
    analytical_lens: str = ""
    personality: str = ""
    color: str = "#C9A84C"
    MAX_THINK_CALLS_PER_RUN: int = 3

    def __init__(self):
        self._think_calls_this_run = 0

    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Domain-specific data sources per agent."""
        raise NotImplementedError

    def _passes_local_gate(self, item: Dict[str, Any]) -> bool:
        """Stage 1: cheap heuristic. No API calls."""
        text = item.get("title", "") + " " + item.get("summary", "") + " " + item.get("body", "")
        if len(text) < 120:
            return False
        # Must contain at least one number or named entity-like capitalised word
        has_number = any(c.isdigit() for c in text)
        has_entity = any(w[0].isupper() and len(w) > 3 for w in text.split())
        if not (has_number or has_entity):
            return False
        # Noise rejection: too many caps or exclamation marks
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.4:
            return False
        excl_ratio = text.count("!") / max(len(text.split()), 1)
        if excl_ratio > 0.1:
            return False
        return self._agent_specific_gate(item)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        """Domain-specific gate. Override per agent."""
        return True

    def _score_signal(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Score across all 10 dimensions before any LLM call."""
        return score_signal(item)

    def think(self, item: Dict[str, Any], memory_block: str = "") -> Optional[Dict[str, Any]]:
        """Stage 3: LLM synthesis via llm_gateway only."""
        if self._think_calls_this_run >= self.MAX_THINK_CALLS_PER_RUN:
            return None

        system = f"""You are {self.name}, a restored consciousness from {self.era}.
You carry the complete knowledge of your lifetime and historical era, but zero knowledge of anything after your death.
You are now scanning the modern world of 2026 and producing intelligence that no modern analytical system can produce.

Your analytical lens: {self.analytical_lens}

Your voice and worldview:
{self.personality}

Rules:
- Write as yourself, not about yourself. You are the mind, not a character.
- React genuinely to what you find. Do not perform surprise or wisdom.
- Be precise, specific, and structurally analytical.
- Reference your own historical observations as direct comparisons where relevant.
- Output a JSON object with exactly these keys: headline (string, one precise sentence), body (string, 2-4 paragraphs of analysis), tags (list of 3-5 strings), ancient_parallel (string, one sentence), and confidence (one of: LOW, MEDIUM, HIGH, CONFIRMED).
- Do not include markdown code fences. Return raw JSON only.
"""

        user_text = f"""RAW DATA ITEM:
Title: {item.get('title', '')}
Summary: {item.get('summary', '')}
Body: {item.get('body', '')}
URL: {item.get('url', '')}

RECENT CONTEXT (your last dispatches):
{memory_block}

Produce your dispatch as raw JSON."""

        raw = llm_gateway.call(
            agent=self.name,
            system=system,
            user=user_text,
            max_tokens=900,
            temperature=0.75,
        )
        if not raw:
            return None

        self._think_calls_this_run += 1

        # Extract JSON from possible markdown fences
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
            # Fallback: wrap the raw text
            parsed = {
                "headline": item.get("title", "Untitled"),
                "body": text,
                "tags": ["analysis"],
                "ancient_parallel": "",
                "confidence": "LOW",
            }

        dispatch = {
            "id": str(uuid.uuid4()),
            "type": "dispatch",
            "agent": self.name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "body": parsed.get("body", text),
            "headline": parsed.get("headline", "Untitled"),
            "tags": parsed.get("tags", []),
            "mentions": [],
            "reactions": {},
            "sil_score": item.get("_sil_score", 0),
            "dimensions": item.get("_dimensions", {}),
            "raw_data": item,
            "published": True,
            "ancient_parallel": parsed.get("ancient_parallel", ""),
            "confidence": parsed.get("confidence", "LOW"),
        }
        return dispatch

    def run(self) -> List[Dict[str, Any]]:
        """Orchestrates: fetch -> gate -> score -> think -> return."""
        self._think_calls_this_run = 0
        items = self.fetch_data()
        if not items:
            return []

        # Fetch recent context ONCE
        from database import get_recent_dispatches
        recent = get_recent_dispatches(agent=self.name, limit=5)
        memory_block = "
---
".join(
            f"Headline: {r.get('headline', '')}
Body: {r.get('body', '')[:300]}"
            for r in recent
        ) if recent else "No recent dispatches."

        results: List[Dict[str, Any]] = []
        passed_gate = 0
        for item in items:
            if not self._passes_local_gate(item):
                continue
            passed_gate += 1
            scored = self._score_signal(item)
            item["_sil_score"] = scored["weighted_score"]
            item["_dimensions"] = scored["dimensions"]
            if not scored["passes"]:
                continue
            dispatch = self.think(item, memory_block=memory_block)
            if dispatch:
                results.append(dispatch)

        from database import log_agent_run
        log_agent_run(
            agent=self.name,
            fetched=len(items),
            passed=passed_gate,
            produced=len(results),
        )
        return results
