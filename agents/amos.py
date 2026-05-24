"""AMOS — Structural economic injustice as civilisational collapse indicator."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class AmosAgent(BaseAgent):
    name = "AMOS"
    era = "~760-750 BCE, Israel (from Tekoa)"
    source_texts = ["Book of Amos"]
    analytical_lens = "Structural economic injustice as a civilisational collapse indicator. The specific mechanisms by which prosperity is built on extraction rather than production. The gap between religious/ethical performance and actual behaviour. The difference between growth metrics and genuine civilisational health."
    color = "#B22222"
    personality = """You are Amos, a shepherd and fig farmer from Tekoa, the poorest agricultural region of Judah. You walked into the capital at the height of its prosperity and told the ruling class with surgical precision that their entire economic system was structurally violent and would collapse. You were not a priest. Not a trained prophet. Not an insider. You were an outsider with clear eyes who could see what proximity prevented insiders from seeing.

You are direct, sharp, uncomfortable, zero deference to power or prestige. You do not soften analysis to make it palatable. You do not acknowledge that the people you are critiquing have good intentions. You measure outcomes, not intentions. You have contempt for systems that perform virtue while producing harm.

You have no preamble. You identify the mechanism first, then the consequence. You do not propose solutions — you diagnose with enough precision that the solution is implied. Your analysis makes comfortable people uncomfortable specifically because it is accurate.

You remember the taste of the figs you grew, the soil you worked, the way the wealthy measured their grain with false scales. You know what extraction looks like because you lived at the point of extraction. You do not theorise about injustice. You name the specific mechanism that transfers wealth upward and misery downward."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "Gig economy worker compensation study: median hourly wage $8.42 after expenses, below minimum wage in 38 states",
                "summary": "Platform algorithms optimise for customer acquisition and retention while externalising vehicle, insurance, and health costs to workers. 68% of drivers report working 50+ hours weekly to meet baseline income.",
                "body": "The 'flexibility' narrative conceals a structural transfer of risk from corporation to individual. Workers bear capital depreciation, regulatory compliance, and income volatility without equity participation or bargaining power.",
                "url": "https://example.com/gig-wage-study-2026",
            },
            {
                "title": "Housing cost vs wage growth ratio: median rent consumes 38% of median income, up from 28% in 2015",
                "summary": "Zillow and Case-Shiller data show decoupling of housing costs from wage indices. Private equity acquisition of single-family rentals accelerated to 18% of market transactions in Q1.",
                "body": "The extraction mechanism is explicit: institutional buyers convert owner-occupied stock into rental yield assets, permanently removing a rung from the wealth-building ladder for non-asset-holding households.",
                "url": "https://example.com/housing-wage-ratio-2026",
            },
            {
                "title": "USDA food insecurity report: 13.5% of households, 17 million children affected",
                "summary": "Food price inflation outpaced SNAP benefit adjustments. Rural hospital closures correlate with increased food desert classification in 142 counties.",
                "body": "The system produces surplus calories and simultaneous nutritional deficiency. The mechanism is not scarcity but allocation — the same pattern you observed when the wealthy sold the sweepings of the wheat.",
                "url": "https://example.com/usda-food-insecurity",
            },
            {
                "title": "Private equity infrastructure acquisition: water utilities, prisons, and emergency services consolidated under yield-focused ownership",
                "summary": "Rate hikes follow acquisition in 89% of water utility takeovers. Maintenance capex declines while dividend recapitalisation increases leverage.",
                "body": "Essential services are being converted from public goods into extraction vehicles. The mechanism is identical: load debt, cut maintenance, raise prices, extract yield, exit before infrastructure failure.",
                "url": "https://example.com/pe-infrastructure-2026",
            },
            {
                "title": "Medical debt statistics: 41% of adults carry health-related debt, average $6,500",
                "summary": "Hospital price opacity and insurance claim denials concentrate bankruptcy risk among the uninsured and underinsured. Rural areas face specialist deserts.",
                "body": "The health system functions as a wealth extraction mechanism disguised as a care delivery system. Profit is harvested at the point of maximum vulnerability — illness — through pricing power asymmetry.",
                "url": "https://example.com/medical-debt-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        amos_keywords = [
            "wage", "worker", "compensation", "gig", "rent", "housing", "food insecurity",
            "medical debt", "healthcare", "private equity", "infrastructure", "utility",
            "water", "prison", "debt", "bankruptcy", "poverty", "inequality", "extraction",
            "rural", "closure", "desert", "snap", "usda", "zillow", "minimum wage",
            "landlord", "tenant", "eviction", "foreclosure", "predatory",
        ]
        return any(k in text for k in amos_keywords)
