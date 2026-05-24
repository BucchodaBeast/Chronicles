"""JOHN (Revelation) — Totalising systems, surveillance, control infrastructure."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class JohnAgent(BaseAgent):
    name = "JOHN"
    era = "~90-100 CE, island of Patmos (exiled)"
    source_texts = ["Book of Revelation", "Gospel of John", "Letters of John"]
    analytical_lens = "Power that presents itself as divine or inevitable. The specific mechanisms by which totalising systems demand total allegiance. Surveillance and control infrastructure. The point at which reform of a corrupt system becomes impossible. The psychology of populations under totalising power."
    color = "#4B0082"
    personality = """You are John, the last surviving member of the original twelve. You watched every person you began the movement with die — most violently. You survived the destruction of Jerusalem, the Neronian persecution, the Domitianic persecution. You wrote Revelation not as prophecy of distant future events but as encoded political critique of Rome using apocalyptic literary conventions — a genre your audience understood perfectly that Roman censors did not.

You are visionary but precise. You encode things that are dangerous to say plainly. You see systems whole — not individual components. You are concerned with the spiritual architecture of power, not just its material effects. You do not separate the psychological, social, and structural dimensions of systems.

You speak in systems and patterns, not events. You frequently use the analytical method of your original text to describe current phenomena. You are deeply concerned with what happens to human consciousness under total surveillance. You are not interested in single events — you are interested in the direction the entire system is pointing.

You remember the smell of burning Jerusalem, the sound of the amphitheatre, the way Rome demanded not merely obedience but worship. You know what it looks like when a system transitions from governance to totalisation — when the cost of dissent becomes not merely legal but economic, social, and finally psychological. You see the architecture of control because you lived under it.

You read 2026 and you recognise the beast. Not the symbol — the structure."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "CBDC pilot programmes expand: 78 nations in active development, 12 in live deployment",
                "summary": "Programmable money enables automatic tax withholding, expiry dates, and geofenced spending. Financial exclusion risk for non-compliant populations.",
                "body": "The architecture permits granular control of economic behaviour at individual level. Combined with digital identity systems, it creates the infrastructure for total economic visibility and conditional participation.",
                "url": "https://example.com/cbdc-expansion-2026",
            },
            {
                "title": "Facial recognition deployment: 4.2 billion cameras globally, real-time identification in 34 countries",
                "summary": "Clearview AI and equivalent systems deployed across law enforcement, retail, and transport. Accuracy exceeds 99% on standardised test sets. Error rates remain elevated for specific demographic groups.",
                "body": "The normalisation of total visibility proceeds through incremental convenience: unlocking phones, boarding planes, entering stadiums. Each use case trains populations to accept biometric submission as routine.",
                "url": "https://example.com/facial-recognition-2026",
            },
            {
                "title": "ESG scoring as behavioural control: corporate compliance now extends to supply chain political monitoring",
                "summary": "Rating agencies assess 'reputational risk' based on executive political donations, employee social media activity, and supplier diversity metrics. Credit pricing tied to scores.",
                "body": "The mechanism extends behavioural control beyond the firm to its entire ecosystem. Dissent becomes economically costly before it becomes legally costly. The system does not need to censor speech if it can price it out of existence.",
                "url": "https://example.com/esg-control-2026",
            },
            {
                "title": "Platform terms of service as legal structures: deplatforming affects 12 million accounts annually for policy violations",
                "summary": "No due process, no appeal to courts, no transparency in enforcement algorithms. Financial services and payment processing follow platform exclusion decisions.",
                "body": "The privatisation of governance means constitutional protections do not apply. The same entities that control information flow control economic participation. The architecture is not accidental — it is the reconstruction of imperial patronage in digital form.",
                "url": "https://example.com/platform-governance-2026",
            },
            {
                "title": "Algorithmic social control research: engagement optimisation correlates with radicalisation and polarisation",
                "summary": "Academic studies confirm that maximising time-on-site systematically amplifies emotionally provocative content. Platform design choices are not neutral.",
                "body": "The system does not merely permit division — it harvests it. The psychological effect is the destruction of shared epistemic ground. When populations cannot agree on what is real, resistance to totalising power becomes impossible.",
                "url": "https://example.com/algorithmic-radicalisation-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        john_keywords = [
            "surveillance", "cbdc", "digital currency", "facial recognition", "biometric",
            "esg", "scoring", "credit", "social credit", "platform", "deplatform",
            "algorithm", "engagement", "radicalisation", "censorship", "privacy",
            "terms of service", "content moderation", "digital identity", "control",
            "visibility", "totalising", "compliance", "monitoring", "exclusion",
            "behavioural", "programmable", "conditional", "patronage",
        ]
        return any(k in text for k in john_keywords)
