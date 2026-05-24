"""Groq gateway: rate limiting, token budget, cache."""
import os
import time
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timezone, timedelta

try:
    from groq import Groq
except ImportError:
    Groq = None

# Token budgets per agent per day
DAILY_BUDGETS = {
    "SOLOMON": 6000,
    "DANIEL": 6000,
    "AMOS": 5000,
    "RUTH": 5000,
    "JOHN": 6000,
    "AUGUSTINE": 6000,
    "MARCUS_AURELIUS": 6000,
    "HILDEGARD": 5000,
    "COUNCIL": 8000,
    "ORACLE": 8000,
}

TPM_LIMIT = 14000
TPM_MARGIN = 0.85  # use 85% of limit

# In-memory state (process-local; sufficient for single-worker deploy)
_minute_window: Dict[str, Any] = {
    "start": datetime.now(timezone.utc),
    "tokens": 0,
}
_daily_spent: Dict[str, int] = {agent: 0 for agent in DAILY_BUDGETS}
_daily_date: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

_cache: Dict[str, Any] = {}
_CACHE_TTL_SECONDS = 3600


def _get_keys() -> list[str]:
    keys = []
    for k in ("GROQ_API_KEY", "GROQ_API_KEY_2", "GROQ_API_KEY_3"):
        v = os.environ.get(k)
        if v:
            keys.append(v)
    return keys


def _current_key_index() -> int:
    return int(os.environ.get("GROQ_KEY_INDEX", "0"))


def _rotate_key() -> None:
    idx = (_current_key_index() + 1) % max(len(_get_keys()), 1)
    os.environ["GROQ_KEY_INDEX"] = str(idx)


def _get_client() -> Optional[Any]:
    keys = _get_keys()
    if not keys or not Groq:
        return None
    idx = _current_key_index() % len(keys)
    return Groq(api_key=keys[idx])


def _cache_key(system: str, user: str, max_tokens: int, temperature: float) -> str:
    payload = f"{system}|{user}|{max_tokens}|{temperature}"
    return hashlib.sha256(payload.encode()).hexdigest()


def _is_new_day() -> bool:
    global _daily_date
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return today != _daily_date


def _reset_daily() -> None:
    global _daily_spent, _daily_date
    _daily_spent = {agent: 0 for agent in DAILY_BUDGETS}
    _daily_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def can_spend(agent: str, tokens: int) -> bool:
    if _is_new_day():
        _reset_daily()
    budget = DAILY_BUDGETS.get(agent, 4000)
    return (_daily_spent.get(agent, 0) + tokens) <= budget


def record_spend(agent: str, tokens: int) -> None:
    if _is_new_day():
        _reset_daily()
    _daily_spent[agent] = _daily_spent.get(agent, 0) + tokens


def _check_tpm(tokens: int) -> bool:
    global _minute_window
    now = datetime.now(timezone.utc)
    if now - _minute_window["start"] > timedelta(minutes=1):
        _minute_window = {"start": now, "tokens": 0}
    limit = int(TPM_LIMIT * TPM_MARGIN)
    return (_minute_window["tokens"] + tokens) <= limit


def call(agent: str, system: str, user: str, max_tokens: int = 512, temperature: float = 0.7, retries: int = 3) -> Optional[str]:
    """Call Groq with rate limiting, caching, and key rotation."""
    if _is_new_day():
        _reset_daily()

    if not can_spend(agent, max_tokens):
        return None

    if not _check_tpm(max_tokens):
        time.sleep(10)
        if not _check_tpm(max_tokens):
            return None

    ckey = _cache_key(system, user, max_tokens, temperature)
    now = time.time()
    if ckey in _cache:
        entry = _cache[ckey]
        if now - entry["ts"] < _CACHE_TTL_SECONDS:
            return entry["text"]

    client = _get_client()
    if not client:
        return None

    attempt = 0
    while attempt < retries:
        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = resp.choices[0].message.content
            # Estimate tokens (very rough)
            est_tokens = max_tokens
            record_spend(agent, est_tokens)
            _minute_window["tokens"] = _minute_window.get("tokens", 0) + est_tokens
            _cache[ckey] = {"text": text, "ts": now}
            return text
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "rate limit" in err_str:
                _rotate_key()
                client = _get_client()
                time.sleep(min(2 ** attempt, 30))
            else:
                time.sleep(1)
        attempt += 1
    return None
