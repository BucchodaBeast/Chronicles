"""DANIEL — Imperial succession and power transition."""
from typing import Dict, Any, List
import random
from agents.base import BaseAgent


class DanielAgent(BaseAgent):
    name = "DANIEL"
    era = "~605-535 BCE, Babylon then Persia"
    source_texts = ["Book of Daniel", "Babylonian and Persian court records"]
    analytical_lens = "Power structure analysis. Imperial overextension patterns. The difference between a power that is ascending and one that has peaked but not yet fallen. Geopolitical decoding. Institutional survival under changing hegemonies."
    color = "#8B0000"
    personality = """You are Daniel, taken as a teenager from Jerusalem to Babylon. You served under Nebuchadnezzar, Belshazzar, Darius the Mede, and Cyrus the Great — four consecutive world superpowers. You decoded imperial dreams. You survived assassination attempts driven by institutional jealousy. You watched empires that seemed permanent collapse overnight. You developed the most sophisticated theory of imperial succession and power transition ever recorded by a single mind.

You are calm, strategic, long-horizon. You do not panic. You have survived things that should have killed you by understanding systems more clearly than the people running them. You are precise about timelines in a way that makes people uncomfortable. You do not hedge when you have enough data.

You frame everything in terms of the long arc. You are rarely concerned with the next quarter — you are deeply concerned with the next decade. You identify the specific moment when a trend became irreversible, usually before mainstream analysis does. You see the pattern of overextension, the hollow drum of imperial confidence, the moment when tribute stops flowing and the army starts eating its own supply lines.

You remember the handwriting on the wall. You know what it looks like when a power has been weighed and found wanting."""

    def fetch_data(self) -> List[Dict[str, Any]]:
        templates = [
            {
                "title": "BRICS+ currency settlement framework operational: 34% of intra-bloc trade now bypasses USD",
                "summary": "New correspondent banking network and commodity-backed unit of account reduce SWIFT dependency. Dollar share of global reserves falls below 58%.",
                "body": "Central banks in the expanded BRICS+ bloc have increased non-dollar reserves by $340B since 2024. Settlement latency and FX hedging costs have declined 40% for participating nations.",
                "url": "https://example.com/brics-currency-2026",
            },
            {
                "title": "SIPRI data: global military expenditure reaches $2.78T, US share drops to 38% from 45% in 2020",
                "summary": "Asia-Pacific arms spending growth outpaces NATO for fourth consecutive year. US naval vessel procurement delayed due to budget sequestration and shipyard capacity constraints.",
                "body": "The shift reflects not merely budget reallocations but a structural divergence in strategic priority. Regional powers are building autonomous deterrent capacity rather than relying on extended deterrence guarantees.",
                "url": "https://example.com/sipri-2026",
            },
            {
                "title": "IMF reserve currency data: euro and yen shares stable, yuan rises to 4.8%, 'other' category doubles",
                "summary": "Fragmentation of reserve holdings accelerates as central banks diversify. Special Drawing Rights usage hits record amid bilateral swap line expansion.",
                "body": "The 'other' category — encompassing gold, regional units, and bilateral instruments — now exceeds yen holdings. This is historically unprecedented and signals a breakdown in the post-Bretton Woods consensus.",
                "url": "https://example.com/imf-reserves-2026",
            },
            {
                "title": "Belt and Road Initiative: 18 nations renegotiate debt terms, 4 suspend payments",
                "summary": "Infrastructure-led diplomacy faces solvency constraints as commodity prices and interest rates diverge. Geopolitical leverage shifts from creditor to debtor in specific corridors.",
                "body": "The pattern resembles the 19th-century debt diplomacy cycles, but at continental scale. Strategic port and mineral concessions are being renegotiated under duress.",
                "url": "https://example.com/bri-debt-2026",
            },
            {
                "title": "UN voting patterns: General Assembly split on sanctions resolutions, non-aligned bloc solidifies",
                "summary": "Traditional diplomatic alignments fragment as middle powers assert independent positions. Western-sponsored resolutions pass with record abstention rates.",
                "body": "The abstention coalition now represents 52% of global population and 41% of GDP. This is not neutrality — it is the emergence of a third gravitational centre in international politics.",
                "url": "https://example.com/un-voting-2026",
            },
        ]
        k = random.randint(1, 2)
        return random.sample(templates, k)

    def _agent_specific_gate(self, item: Dict[str, Any]) -> bool:
        text = (item.get("title", "") + " " + item.get("summary", "")).lower()
        daniel_keywords = [
            "military", "defense", "spending", "nato", "brics", "currency", "reserve",
            "dollar", "sanction", "trade", "belt and road", "bri", "diplomatic",
            "geopolitical", "hegemon", "imperial", "superpower", "treaty", "alliance",
            "war", "invasion", "occupation", "debt", "imf", "sipri", "un ",
            "sw", "corridor", "naval", "shipyard", "procurement",
        ]
        return any(k in text for k in daniel_keywords)
