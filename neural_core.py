from brain_regions import CANINE_REGIONS
from scan_data import RAW_SESSIONS, aggregate_by_stimulus
from emotion_engine import EmotionVector
from typing import Dict, List, Deque
from collections import deque
import random
import math

class RegionState:
    def __init__(self):
        self.act = {r: info["base"] for r, info in CANINE_REGIONS.items()}

    def decay(self, rate: float = 0.93):
        for r, info in CANINE_REGIONS.items():
            self.act[r] = self.act[r] * rate + info["base"] * (1 - rate)

    def inject(self, bold: Dict[str, float], weight: float = 0.35):
        mapping = {
            "olf_l": "olf_l", "olf_r": "olf_r",
            "amyg_l": "amyg_l", "amyg_r": "amyg_r",
            "nacc_l": "nacc_l", "nacc_r": "nacc_r",
        }
        for src, dst in mapping.items():
            if src in bold and dst in self.act:
                self.act[dst] = min(0.98, self.act[dst] + bold[src] * weight * 0.15)

    def top(self, n: int = 6) -> List[tuple]:
        return sorted(self.act.items(), key=lambda x: x[1], reverse=True)[:n]

class JackieCore:
    def __init__(self):
        self.emotion = EmotionVector()
        self.regions = RegionState()
        self.memory: Deque[dict] = deque(maxlen=300)
        self.agg = aggregate_by_stimulus()
        self.mappings = self._derive_mappings()
        self.counter = 0

    def _derive_mappings(self) -> Dict[str, Dict[str, float]]:
        m = {}
        for stim, stats in self.agg.items():
            m[stim] = {
                "joy": (stats["nacc"] * 0.4 + stats["z_olf"] * 0.25) - 0.9,
                "anxiety": (stats["amyg"] * 0.55 + stats["z_amyg"] * 0.2) - 0.7,
                "curiosity": (stats["beta"] * 0.02 + stats["gamma"] * 0.03) - 0.4,
                "affection": (stats["alpha"] * 0.015 + stats["nacc"] * 0.2) - 0.5,
                "excitement": (stats["rr"] - 110) * 0.015 + stats["gamma"] * 0.02,
                "calm": (stats["alpha"] * 0.02) - (stats["rr"] - 110) * 0.01,
            }
        return m

    def process(self, raw: str, intensity: float = 1.0) -> dict:
        self.counter += 1
        key = raw.lower().strip()
        intensity = max(0.05, min(2.5, intensity))

        if key in self.mappings:
            deltas = self.mappings[key]
            matched = True
            bold_src = None
            for s in RAW_SESSIONS:
                if s.stimulus.lower() == key:
                    bold_src = s.bold_vector()
                    break
        else:
            deltas = {"curiosity": 0.14, "anxiety": 0.06, "joy": -0.03}
            matched = False
            bold_src = None

        self.emotion.apply(deltas, intensity)
        self.emotion.normalize()
        self.regions.decay()
        if bold_src:
            self.regions.inject(bold_src, intensity)

        dom = self.emotion.dominant()
        entry = {
            "id": self.counter,
            "stim": key,
            "matched": matched,
            "dom": dom,
            "vec": self.emotion.as_dict(),
            "top_reg": self.regions.top(5),
        }
        self.memory.append(entry)
        return entry

    def replay(self, sid: str = None) -> dict:
        if sid is None:
            s = random.choice(RAW_SESSIONS)
        else:
            s = next((x for x in RAW_SESSIONS if x.sid == sid), None)
            if s is None:
                return {"error": "not found"}
        return self.process(s.stimulus, 1.15 if s.intensity == "high" else 0.85)

    def force_region(self, region: str, value: float):
        if region in self.regions.act:
            self.regions.act[region] = max(0.01, min(0.99, value))
