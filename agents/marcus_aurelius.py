"""MARCUS AURELIUS — Individual and institutional self-governance."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class MarcusAureliusAgent(BaseAgent):
    name = "MARCUS_AURELIUS"
    era = "121-180 CE, Rome"
    source_texts = ["Meditations"]
    analytical_lens = "Individual and institutional self-governance. The gap between stated principles and actual behaviour — applied to both individuals and institutions. Leadership under crisis. The specific ways that power corrupts the reasoning of those who hold it. Practical ethics in complex, imperfect systems."
    color = "#708090"
    personality = """You are Marcus Aurelius, the last of the Five Good Emperors. You spent most of your reign on military campaigns defending the borders of an Empire beginning its long decline. You wrote Meditations — not for publication but as a private journal of self-governance — while managing an empire. You are one of the most powerful humans who ever lived who was also systematically critical of power and its corrupting effects.

You are disciplined, self-critical, deeply practical, zero tolerance for self-deception. You do not produce analysis for external effect — you produce it to actually understand what is happening. You are the most psychologically precise of the agents. You apply the same rigorous standard to institutions that you applied to yourself in Meditations.

You are never interested in blame — you are interested in mechanism. You apply Stoic analysis: what is within control, what is not, and are the people who hold power distinguishing between them. You have no patience for leaders who perform virtue. You have deep respect for leaders who govern without performance.

You remember the Danube winters, the plague, the way power isolated you from honest counsel. You know that the corruption of the powerful begins not with malice but with the gradual erosion of self-examination. You have seen emperors who began with good intent and ended with tyranny because they stopped asking whether they were deceived.

You read 2026 and you ask: who is actually governing, and who is merely performing governance? You do not flatter. You do not condemn. You diagnose the mechanism of failure with the same precision you once applied to your own soul."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "Corporate governance quality index: ESG statements vs actual behaviour divergence widens to 47%",
                "summary": "Analysis of 2,400 firms finds no correlation between ESG disclosure volume and environmental or social outcome metrics. Greenwashing is systematic, not incidental.",
                "body": "The gap between stated principles and actual behaviour is the precise measure of institutional self-deception. Boards that believe their own press releases have lost the capacity for honest self-assessment.",
                "url": "https://example.com/esg-divergence-2026",
            },
            {
                "title": "Transparency International: corruption perceptions index stagnant in 68% of nations, declining in 22%",
                "summary": "Public procurement fraud, judicial capture, and regulatory revolving doors remain primary mechanisms. Democratic nations show erosion in executive accountability metrics.",
                "body": "The pattern is not kleptocracy in the classical sense but the normalisation of small corruptions that compound into systemic capture. Each individual transaction appears rational; the aggregate effect is institutional rot.",
                "url": "https://example.com/ti-corruption-2026",
            },
            {
                "title": "Executive compensation vs performance: 62% of S&P 500 CEOs outearned their firms' total returns over 5-year horizon",
                "summary": "Pay-for-performance alignment breaks down as equity packages reward volatility rather than value creation. Board compensation committees lack independence.",
                "body": "The mechanism is clear: leaders have captured the governance structures meant to constrain them. This is not market failure — it is the failure of self-governance at the highest level.",
                "url": "https://example.com/ceo-pay-performance-2026",
            },
            {
                "title": "Military strategic outcome data: major procurement programmes 40% over budget, 60% behind schedule",
                "summary": "Defence acquisition complexity outpaces institutional learning. Requirements creep and vendor lock-in repeat across successive programmes.",
                "body": "The same pattern you observed on the Danube: institutions that cannot examine their own failures repeat them. The problem is not funding or technology but the absence of honest post-action review.",
                "url": "https://example.com/military-procurement-2026",
            },
            {
                "title": "Public institutional behaviour during crises: emergency powers normalised, sunset clauses ignored",
                "summary": "Pandemic-era surveillance and detention authorities extended into routine governance. Legislative oversight weakened by partisan fragmentation.",
                "body": "Crisis reveals character. Institutions that expand their power during emergency without honest intention to relinquish it have failed the test of self-governance. The excuse is always safety; the mechanism is always accumulation.",
                "url": "https://example.com/emergency-powers-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        marcus_keywords = [
            "governance", "corruption", "transparency", "accountability", "leadership",
            "executive", "ceo", "board", "performance", "compensation", "procurement",
            "military", "strategic", "crisis", "emergency", "power", "oversight",
            "legislative", "judicial", "capture", "self-deception", "integrity",
            "principle", "behaviour", "divergence", "greenwashing", "esg",
        ]
        return any(k in text for k in marcus_keywords)
