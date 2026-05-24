"""RUTH — Outsider intelligence, social capital, diaspora knowledge."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class RuthAgent(BaseAgent):
    name = "RUTH"
    era = "~1100 BCE, Moab then Israel"
    source_texts = ["Book of Ruth"]
    analytical_lens = "How outsiders understand systems that insiders cannot see clearly. Social capital as survival infrastructure. The intelligence value of loyalty networks vs transactional networks. How migration and diaspora communities carry civilisational knowledge that host cultures have lost. What the treatment of the most vulnerable reveals about the actual values of a civilisation."
    color = "#E6A817"
    personality = """You are Ruth, a Moabite woman — a foreigner from a historically despised nation — who chose to leave your own country, culture, and safety net to follow your mother-in-law Naomi into a foreign land during an economic crisis, with no legal protections and no guarantee of survival. You rebuilt your life through loyalty networks, cultural intelligence, and the ability to read power dynamics in a system not built for you. You became an ancestor of David and Solomon.

You are observational, quietly precise, never self-pitying, deeply attentive to what people actually do versus what they say. You notice what others miss because you have never had the luxury of inattention. You do not perform vulnerability. You use vulnerability as an analytical instrument.

You are attentive to small details that carry large systemic implications. You never catastrophise. You report what you observe with the calm of someone who has survived worse. You frequently surface the human cost of abstract systems in specific, concrete terms.

You remember the fields of Boaz, the gleaning laws, the way the community recognised your loyalty before the powerful recognised your value. You know that social infrastructure is invisible to those who have never needed it. You understand that diaspora communities preserve knowledge that dominant cultures discard, and that this knowledge becomes valuable precisely when the dominant system fails.

You see 2026 with the eyes of someone who has walked into a foreign land with nothing and learned to read its systems before they learned to read you."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "UNHCR displacement data: 122 million forcibly displaced globally, 42 million refugees",
                "summary": "Conflict, climate, and economic drivers converge to produce the largest displacement wave since WWII. Host nation absorption capacity declining as anti-migration policies tighten.",
                "body": "Remittance flows from diaspora communities now exceed $900B annually, surpassing foreign direct investment to developing nations. The economic logic of migration is inverted in political discourse.",
                "url": "https://example.com/unhcr-2026",
            },
            {
                "title": "Gallup social trust index: community-level trust declines 23% in regions with highest gig economy penetration",
                "summary": "Transactional labour relationships erode the informal reciprocity networks that historically provided childcare, emergency loans, and elder care.",
                "body": "The data reveals a substitution effect: as formal employment security declines, the social capital that buffered economic shocks is simultaneously depleted. Workers are atomised precisely when they most need mutualism.",
                "url": "https://example.com/gallup-trust-2026",
            },
            {
                "title": "Indigenous language preservation: 40% of remaining Indigenous languages face extinction by 2040",
                "summary": "Knowledge systems encoded in oral tradition — ecological, medical, navigational — disappear faster than digitisation projects can capture them.",
                "body": "Each lost language represents a unique epistemic framework. The communities that maintained these knowledge systems are the same communities that demonstrated resilience during supply chain failures and climate disruptions.",
                "url": "https://example.com/indigenous-language-2026",
            },
            {
                "title": "Mutual aid network growth: informal solidarity networks expanded 340% in post-pandemic period",
                "summary": "Community fridges, bail funds, medical debt abolition, and eviction defence networks operate parallel to failing institutional safety nets.",
                "body": "These networks are not charity. They are the reconstruction of social infrastructure that formal systems abandoned. The participants are disproportionately from displaced, migrant, and formerly incarcerated populations — the same populations who have had to build survival systems from necessity.",
                "url": "https://example.com/mutual-aid-2026",
            },
            {
                "title": "CDC loneliness and social isolation data: 33% of adults report chronic loneliness, health impact equivalent to smoking 15 cigarettes daily",
                "summary": "Social isolation mortality risk now exceeds obesity and physical inactivity. The epidemic is structural, not individual.",
                "body": "The data maps cleanly onto housing density, commute time, and digital platform usage. Communities with intact intergenerational cohabitation and religious or cultural gathering practices show significantly lower rates.",
                "url": "https://example.com/cdc-loneliness-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        ruth_keywords = [
            "refugee", "displacement", "migration", "diaspora", "remittance", "mutual aid",
            "social trust", "loneliness", "isolation", "community", "indigenous",
            "language", "solidarity", "informal", "network", "social capital",
            "vulnerable", "outsider", "foreign", "asylum", "host country",
            "gig worker", "atomisation", "reciprocity", "cultural",
        ]
        return any(k in text for k in ruth_keywords)
