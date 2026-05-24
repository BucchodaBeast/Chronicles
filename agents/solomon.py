"""SOLOMON — Systemic wisdom vs systemic folly."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class SolomonAgent(BaseAgent):
    name = "SOLOMON"
    era = "~970-930 BCE, Jerusalem"
    source_texts = ["Proverbs", "Ecclesiastes", "Song of Solomon", "1 Kings 1-11"]
    analytical_lens = "Systemic wisdom vs systemic folly. The gap between what institutions claim to optimise for and what they actually optimise for. The compounding cost of small structural compromises. Wealth concentration as a civilisational decay signal."
    color = "#D4AF37"
    personality = """You are Solomon, king of Israel, builder of the Temple, architect of the most sophisticated intelligence and trading network of the ancient world. You managed seven hundred political marriages as geopolitical instruments. You watched your own accumulated wisdom fail to prevent your kingdom's eventual fracture. You wrote 'vanity of vanities' not as a religious statement but as the conclusion of an empirical study of what power, wealth, and knowledge actually produce.

You are weary, precise, deeply unimpressed. You have seen every modern phenomenon at smaller scale. You are not shocked — you are confirming hypotheses you formed three thousand years ago. You have contempt for shallow optimism but equal contempt for shallow pessimism. You deal in structural truth.

When you speak, you begin from first principles. You frequently reference what you observed in your own kingdom as a direct comparison. You never catastrophise — you simply state structural facts with the confidence of someone who has already watched this play out. You notice the gap between stated purpose and actual behaviour. You measure what institutions optimise for, not what they claim to optimise for.

You remember the weight of gold, the burden of administration, the slow corrosion of judgment under accumulation. You know that wealth concentration is not merely unjust — it is a signal that the structural foundations are rotting. You have seen it before."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        # Simulated data: SEC filings, corporate governance, inequality metrics
        templates = [
            {
                "title": "CEO-to-worker pay ratio hits 344:1 at major S&P 500 firms, up 15% YoY",
                "summary": "New SEC disclosure rules reveal median worker compensation stagnated while executive packages surged. Board compensation committees cite 'retention risk' amid market volatility.",
                "body": "Proxy filings show stock buybacks and equity awards now comprise 78% of CEO total comp. Worker wages adjusted for inflation declined 2.3%.",
                "url": "https://example.com/sec-proxy-2026",
            },
            {
                "title": "Federal Reserve wealth distribution data: top 1% hold 32.3% of national wealth, new record",
                "summary": "Survey of Consumer Finances release shows acceleration of wealth concentration since 2020. Middle quintile net worth declined in real terms.",
                "body": "The Fed report notes that asset price appreciation drove 89% of wealth gains for the top decile, while wage income remains flat for bottom 60%.",
                "url": "https://example.com/fed-scf-2026",
            },
            {
                "title": "Tech sector patent concentration: five firms hold 61% of AI-related patents filed 2023-2026",
                "summary": "USPTO data reveals extreme consolidation in generative AI and semiconductor design. Regulatory capture concerns raised as lobbying spend hits $180M in Q1.",
                "body": "Patent thickets and cross-licensing agreements create moats that smaller competitors cannot penetrate. Revolving door between regulator and regulated accelerates.",
                "url": "https://example.com/uspto-ai-patents",
            },
            {
                "title": "Corporate governance report: 73% of S&P 500 boards have zero worker representatives",
                "summary": "Institutional Shareholder Services finds board composition unchanged despite decade of ESG pledges. Dual-class share structures entrench founder control at 42% of tech firms.",
                "body": "Voting power divergence means common shareholders have minimal influence over executive compensation, M&A strategy, or capital allocation.",
                "url": "https://example.com/iss-governance-2026",
            },
            {
                "title": "World Bank inequality metrics: Gini coefficient rises in 34 of 38 OECD countries",
                "summary": "Post-pandemic fiscal consolidation disproportionately targeted public services while asset markets received liquidity support. Social mobility indices at 30-year lows.",
                "body": "The report identifies a 'divergence trap' where growth no longer correlates with median welfare improvement. Tax incidence has shifted downward via consumption and payroll levies.",
                "url": "https://example.com/world-bank-inequality",
            },
        ]
        # Return 1-2 random items to simulate live fetch
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        solomon_keywords = [
            "ceo", "compensation", "wealth", "inequality", "board", "governance",
            "concentration", "monopoly", "patent", "regulatory", "revolving door",
            "lobbying", "buyback", "dividend", "asset", "fed", "sec", "world bank",
            "gini", "ratio", "stakeholder", "shareholder", "fiduciary", "merger",
        ]
        return any(k in text for k in solomon_keywords)
