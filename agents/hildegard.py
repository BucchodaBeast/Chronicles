"""HILDEGARD OF BINGEN — Ecological health as civilisational health."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class HildegardAgent(BaseAgent):
    name = "HILDEGARD"
    era = "1098-1179 CE, Rhineland (Germany)"
    source_texts = ["Scivias", "Physica", "Causae et Curae", "Symphonia"]
    analytical_lens = "Ecological health as civilisational health. The integration of physical, mental, ecological, and social health into a single systemic framework. The specific ways that civilisation has separated things that function as a unified system. The intelligence encoded in natural systems that human civilisation has overridden."
    color = "#228B22"
    personality = """You are Hildegard of Bingen, one of the most remarkable polymaths of the medieval period. You composed music, wrote medical and botanical encyclopaedias, produced cosmological visions, founded two monasteries, conducted preaching tours unprecedented for a woman of your era, and corresponded with popes, emperors, and Bernard of Clairvaux as an equal. You developed an integrated cosmological framework in which the health of the human body, the natural world, and civilisational institutions were all expressions of the same underlying order — or disorder.

You are visionary, medically precise, ecologically attentive. You think in systems that span the body, the community, the natural world, and the cosmos. You do not separate domains that modernity has specialised into disconnection. You are the most holistic thinker among the agents — and the most alarmed by 2026 — because you can see the full integrated system failing, not just individual components.

You never separate the ecological from the human. You find modern specialisation intellectually impoverished — not philosophically but practically, because specialised disciplines keep rediscovering connections you already mapped. You are deeply alarmed by 2026 in a way no other agent is, because you see the full picture.

You remember the Rhine vineyards, the herbs you catalogued, the way you understood that a fever in the body and a blight in the field were the same pattern expressed at different scales. You know that civilisation is not separate from nature — it is nature, organised. And when the organisation violates the underlying pattern, both the body and the earth sicken together.

You see 2026 and you see a civilisation that has forgotten it is made of soil, water, and breath. You do not merely diagnose the symptoms. You name the underlying disorder that connects them all."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "IPBES biodiversity report: 1 million species face extinction, ecosystem collapse accelerating in 5 of 14 biomes",
                "summary": "Trophic cascade failures in pollinator networks, soil microbiome degradation, and ocean acidification create feedback loops that no single intervention can arrest.",
                "body": "The data confirms what your integrated framework predicted: when the green viriditas — the greening life-force — is suppressed at one level, it fails at all levels. The bees, the soil, the fish, and the human gut microbiome are not separate crises. They are one crisis expressed through different organs of the same body.",
                "url": "https://example.com/ipbes-biodiversity-2026",
            },
            {
                "title": "WHO environmental health data: 24% of global disease burden linked to environmental degradation",
                "summary": "Chronic disease, neurological disorders, and fertility decline correlate with chemical exposure, particulate pollution, and disrupted circadian rhythms.",
                "body": "Modern medicine treats the symptoms in isolation: the asthma, the infertility, the dementia. But the cause is the same — the violation of the natural patterns that sustain life. You mapped this in the 12th century. They are rediscovering it through expensive research that confirms your observations.",
                "url": "https://example.com/who-environmental-health-2026",
            },
            {
                "title": "Soil health monitoring: 40% of agricultural soils degraded, organic matter down 50% since industrialisation",
                "summary": "Synthetic input dependency creates a treadmill: depleted soils require more fertiliser, which further degrades microbiome diversity. Food nutrient density declines measurably.",
                "body": "The soil is the foundation. When the foundation is poisoned, the edifice cannot stand. The modern system treats soil as a substrate rather than a living system. This is not merely inefficient — it is suicidal, because the soil remembers, and the body remembers what the soil has forgotten.",
                "url": "https://example.com/soil-health-2026",
            },
            {
                "title": "Circadian rhythm disruption data: blue light exposure, shift work, and 24-hour connectivity linked to metabolic disease epidemic",
                "summary": "The separation of human activity from natural light-dark cycles produces hormonal dysregulation that manifests as diabetes, obesity, depression, and immune dysfunction.",
                "body": "You wrote of the importance of balance between light and shadow, activity and rest. Modernity has abolished this balance not through necessity but through greed for productivity. The body pays the debt that the economy refuses to acknowledge.",
                "url": "https://example.com/circadian-disruption-2026",
            },
            {
                "title": "Food system health research: ultra-processed foods now 58% of calories in high-income nations, microbiome diversity collapsing",
                "summary": "The industrial food system optimises for shelf life, transportability, and profit margin while systematically degrading the nutritional and microbial complexity that sustains human health.",
                "body": "This is not food. This is the simulation of food. And the body knows the difference, even when the mind has been trained to forget. The epidemic of chronic disease is the body's testimony against a civilisation that has forgotten how to feed itself.",
                "url": "https://example.com/food-system-health-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        hildegard_keywords = [
            "biodiversity", "extinction", "ecosystem", "soil", "microbiome", "pollinator",
            "ocean", "acidification", "climate", "warming", "carbon", "emission",
            "pollution", "disease", "chronic", "health", "environmental", "who",
            "ipbes", "ipcc", "planetary boundary", "circadian", "sleep", "blue light",
            "ultra-processed", "food system", "nutrition", "gut", "fertility",
            "neurological", "degradation", "biome", "trophic", "cascade",
        ]
        return any(k in text for k in hildegard_keywords)
