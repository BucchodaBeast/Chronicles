"""Multi-dimensional signal scoring (10 dimensions)."""
import json
import math
from typing import Dict, Any

DIMENSIONS = {
    'novelty':               0.15,
    'consequence':           0.20,
    'information_density':   0.10,
    'actionability':         0.10,
    'rarity_of_attention':   0.15,
    'cross_domain':          0.10,
    'temporal_advantage':    0.10,
    'anomaly_score':         0.05,
    'epistemic_impact':      0.03,
    'strategic_depth':       0.02,
}

MINIMUM_SCORE = 0.52


def score_signal(item: Dict[str, Any]) -> Dict[str, Any]:
    """Score a raw item across 10 dimensions using only metadata. No LLM."""
    text = item.get("title", "") + " " + item.get("summary", "") + " " + item.get("body", "")
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 1. novelty: uncommon keywords, rare entities
    uncommon = sum(1 for w in words if len(w) > 8)
    novelty = min(1.0, uncommon / max(word_count * 0.05, 1))

    # 2. consequence: presence of impact keywords
    impact_keywords = [
        "collapse", "crisis", "surge", "crash", "breakdown", "default",
        "sanction", "war", "invasion", "recession", "depression", "famine",
        "shortage", "bankruptcy", "liquidation", "merger", "acquisition",
        "regulation", "legislation", "bailout", "stimulus", "tariff",
        "trade", "currency", "reserve", "military", "defense", "nuclear",
        "cyber", "attack", "breach", "exploit", "vulnerability",
        "climate", "warming", "drought", "flood", "extinction", "biodiversity",
        "inequality", "poverty", "wealth", "concentration", "monopoly",
    ]
    impact_hits = sum(1 for k in impact_keywords if k in text_lower)
    consequence = min(1.0, impact_hits / 3.0)

    # 3. information_density: numbers, named entities, ratios
    numbers = sum(1 for w in words if any(c.isdigit() for c in w))
    density = min(1.0, numbers / max(word_count * 0.03, 1))
    information_density = 0.5 + (density * 0.5)

    # 4. actionability: contains specific actors, instruments, or levers
    action_keywords = [
        "should", "must", "will", "plan", "policy", "strategy", "reform",
        "invest", "divest", "buy", "sell", "hedge", "migrate", "relocate",
        "diversify", "consolidate", "regulate", "deregulate", "vote",
        "strike", "boycott", "sanction", "negotiate", "treaty", "alliance",
    ]
    action_hits = sum(1 for k in action_keywords if k in text_lower)
    actionability = min(1.0, action_hits / 2.0)

    # 5. rarity_of_attention: length suggests depth; short clickbait is low
    if word_count < 30:
        rarity = 0.2
    elif word_count < 80:
        rarity = 0.5
    else:
        rarity = min(1.0, 0.6 + (word_count / 1000))

    # 6. cross_domain: multiple domain keywords present
    domains = {
        "finance": ["market", "stock", "bond", "equity", "derivative", "bank", "fed", "ecb"],
        "geopolitics": ["nato", "eu", "china", "russia", "iran", "israel", "ukraine", "taiwan"],
        "tech": ["ai", "algorithm", "surveillance", "data", "platform", "cyber", "chip"],
        "health": ["pandemic", "disease", "hospital", "pharma", "vaccine", "mental health"],
        "environment": ["climate", "carbon", "emission", "renewable", "fossil", "oil", "gas"],
        "social": ["inequality", "housing", "education", "migration", "refugee", "protest"],
    }
    domain_hits = 0
    for domain, keywords in domains.items():
        if any(k in text_lower for k in keywords):
            domain_hits += 1
    cross_domain = min(1.0, domain_hits / 3.0)

    # 7. temporal_advantage: time-sensitive language
    time_keywords = ["urgent", "breaking", "exclusive", "leak", "draft", "upcoming", "imminent", "next week", "q3", "2026", "before"]
    time_hits = sum(1 for k in time_keywords if k in text_lower)
    temporal_advantage = min(1.0, time_hits / 2.0)

    # 8. anomaly_score: deviation words
    anomaly_keywords = ["unexpected", "surprise", "unprecedented", "record", "historic", "first time", "never", "sudden", "shock"]
    anomaly_hits = sum(1 for k in anomaly_keywords if k in text_lower)
    anomaly_score = min(1.0, anomaly_hits / 2.0)

    # 9. epistemic_impact: framework-challenging language
    epistemic_keywords = ["paradigm", "theory", "model", "framework", "assumption", "consensus", "debunk", "revised", "overturn"]
    epistemic_hits = sum(1 for k in epistemic_keywords if k in text_lower)
    epistemic_impact = min(1.0, epistemic_hits / 2.0)

    # 10. strategic_depth: second-order language
    depth_keywords = ["cascade", "spiral", "feedback", "loop", "contagion", "systemic", "structural", "derivative", "knock-on", "blowback"]
    depth_hits = sum(1 for k in depth_keywords if k in text_lower)
    strategic_depth = min(1.0, depth_hits / 2.0)

    scores = {
        'novelty': novelty,
        'consequence': consequence,
        'information_density': information_density,
        'actionability': actionability,
        'rarity_of_attention': rarity,
        'cross_domain': cross_domain,
        'temporal_advantage': temporal_advantage,
        'anomaly_score': anomaly_score,
        'epistemic_impact': epistemic_impact,
        'strategic_depth': strategic_depth,
    }

    weighted = sum(scores[k] * DIMENSIONS[k] for k in DIMENSIONS)

    return {
        "dimensions": scores,
        "weighted_score": round(weighted, 4),
        "passes": weighted >= MINIMUM_SCORE,
    }
