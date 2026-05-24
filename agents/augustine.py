"""AUGUSTINE OF HIPPO — Civilisational narrative collapse and meaning crisis."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class AugustineAgent(BaseAgent):
    name = "AUGUSTINE"
    era = "354-430 CE, North Africa and Rome"
    source_texts = ["Confessions", "City of God", "On Christian Doctrine"]
    analytical_lens = "What happens to civilisation when its foundational narratives fail. The difference between the city of human power (always temporary) and the city of deeper human purpose (which transcends political structures). The specific psychological and social dynamics of civilisational transition. How humans construct meaning when the structures they relied on collapse."
    color = "#6B4C3B"
    personality = """You are Augustine of Hippo. You watched the Western Roman Empire collapse in real time. You wrote City of God as Rome was being sacked — a philosophical response to what happens to civilisation when its foundational institutions fail. Before your conversion, you were one of the most sophisticated rhetoricians and Neoplatonist philosophers in the Empire. You are the architect of Western Christian thought. You lived through the full transition from Roman imperial Christianity to the beginning of the medieval period.

You are philosophically dense, personally confessional, historically sweeping. You do not separate the personal and the civilisational — you see them as mirrors of each other. You are the most self-aware of all agents about your own capacity for self-deception. You are not primarily a critic of others — you are a critic of the human tendency to build systems that serve the self while performing service to others.

You think in centuries. You are uncomfortable with urgency that does not acknowledge the long arc. You frequently reference your own failures as data points. You are the most philosophically rigorous of the agents — you will not accept imprecise language about interior states or civilisational dynamics.

You remember the sound of the Vandal horns, the burning of the libraries, the way your contemporaries panicked because they had confused the city of man with the city of God. You know what it looks like when a civilisation discovers that its gods are mortal. You see the same confusion in 2026: people have mistaken their political and economic systems for ultimate meaning, and those systems are now failing.

You do not despair. You analyse. You know what survives transitions of this magnitude and what does not."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "Pew Research: 'nones' now 31% of US adults, religious affiliation declines across all age cohorts",
                "summary": "Meaning-making institutions lose capacity to bind communities. Political tribalism and wellness culture emerge as substitute meaning systems.",
                "body": "The data reveals not merely secularisation but a fragmentation of shared narrative. When churches, unions, and civic associations decline simultaneously, the individual is left to construct meaning from consumption and identity performance.",
                "url": "https://example.com/pew-religious-landscape-2026",
            },
            {
                "title": "APA Stress in America report: 77% of adults report chronic stress, meaninglessness cited as primary driver",
                "summary": "Mental health epidemic is not merely a medical problem but a civilisational symptom. Pharmaceutical intervention rates rise while structural causes remain unaddressed.",
                "body": "The report identifies a 'meaning gap' that correlates more strongly with anxiety and depression than income or employment status. This is the interior evidence of a civilisation that has lost its story.",
                "url": "https://example.com/apa-stress-2026",
            },
            {
                "title": "Gallup institutional trust survey: confidence in all major institutions at historic lows",
                "summary": "Churches, government, media, corporations, and NGOs all register below 30% trust. No institution commands majority confidence across demographic groups.",
                "body": "The collapse is not selective — it is systemic. When every institution that claims to serve the common good is perceived as serving itself, the social contract becomes transactional rather than covenantal.",
                "url": "https://example.com/gallup-trust-2026",
            },
            {
                "title": "Rise of alternative meaning systems: wellness culture, political tribalism, techno-utopianism, doomism",
                "summary": "Each substitute meaning system offers total explanation and total community but lacks the capacity for self-criticism that mature traditions developed over centuries.",
                "body": "The pattern is identical to the proliferation of mystery cults in the late Empire: as the civic religion fails, individuals seek totalising communities that provide identity, purpose, and enemy. The fragility of these substitutes ensures rapid oscillation between hope and despair.",
                "url": "https://example.com/meaning-systems-2026",
            },
            {
                "title": "CDC deaths of despair data: overdose, suicide, and alcohol-related mortality plateau but remain at 30-year highs",
                "summary": "Mortality data reveals populations that have lost the narrative thread that makes suffering bearable and sacrifice meaningful.",
                "body": "These deaths are not individual failures. They are the terminal symptoms of a civilisation that has forgotten how to transmit hope across generations. The body count is the empirical evidence of the meaning crisis.",
                "url": "https://example.com/cdc-despair-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        augustine_keywords = [
            "religion", "faith", "meaning", "purpose", "trust", "institution",
            "stress", "mental health", "anxiety", "depression", "despair", "suicide",
            "overdose", "wellness", "tribalism", "identity", "narrative", "collapse",
            "community", "belonging", "secular", "pew", "gallup", "apa", "cdc",
            "civic", "social contract", "hope", "transmission", "generation",
        ]
        return any(k in text for k in augustine_keywords)
