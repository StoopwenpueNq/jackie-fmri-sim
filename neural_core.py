from brain_regions import CANINE_REGIONS
from scan_data import RAW_SESSIONS, aggregate_by_stimulus
from emotion_engine import EmotionVector
from physiology import PhysioState
from stimulus_mapper import StimulusMapper
from session_loader import SessionLoader
from visualizer import Visualizer
from config import DECAY_RATE, INJECT_WEIGHT, REGION_BOOST, MEMORY_SIZE
from typing import Dict, List, Deque
from collections import deque
import random
import math

class RegionState:
    def __init__(self):
        self.act = {r: info["base"] for r, info in CANINE_REGIONS.items()}

    def decay(self, rate: float = DECAY_RATE):
        for r, info in CANINE_REGIONS.items():
            self.act[r] = self.act[r] * rate + info["base"] * (1.0 - rate)

    def inject(self, bold: Dict[str, float], weight: float = INJECT_WEIGHT):
        mapping = {
            "olf_l": "olf_l", "olf_r": "olf_r",
            "amyg_l": "amyg_l", "amyg_r": "amyg_r",
            "nacc_l": "nacc_l", "nacc_r": "nacc_r",
        }
        for src, dst in mapping.items():
            if src in bold and dst in self.act:
                self.act[dst] = min(0.99, self.act[dst] + bold[src] * weight * 0.14)

    def apply_social_boost(self, label: str):
        boosts = REGION_BOOST.get(label, {})
        for r, v in boosts.items():
            if r in self.act:
                self.act[r] = min(0.99, self.act[r] + v)

    def top(self, n: int = 6) -> List[tuple]:
        return sorted(self.act.items(), key=lambda x: x[1], reverse=True)[:n]

class JackieCore:
    def __init__(self):
        self.emotion = EmotionVector()
        self.regions = RegionState()
        self.physio = PhysioState()
        self.mapper = StimulusMapper()
        self.loader = SessionLoader()
        self.viz = Visualizer()
        self.memory: Deque[dict] = deque(maxlen=MEMORY_SIZE)
        self.agg = aggregate_by_stimulus()
        self.mappings = self._derive_mappings()
        self.counter = 0

    def _derive_mappings(self) -> Dict[str, Dict[str, float]]:
        m = {}
        for stim, stats in self.agg.items():
            m[stim] = {
                "joy": (stats["nacc"] * 0.42 + stats["z_olf"] * 0.22) - 0.85,
                "anxiety": (stats["amyg"] * 0.58 + stats["z_amyg"] * 0.18) - 0.65,
                "curiosity": (stats["beta"] * 0.018 + stats["gamma"] * 0.025) - 0.38,
                "affection": (stats["alpha"] * 0.014 + stats["nacc"] * 0.19) - 0.48,
                "excitement": (stats["rr"] - 108) * 0.014 + stats["gamma"] * 0.018,
                "calm": (stats["alpha"] * 0.019) - (stats["rr"] - 108) * 0.009,
            }
        return m

    def process(self, raw: str, intensity: float = 1.0) -> dict:
        self.counter += 1
        key, meta = self.mapper.resolve(raw)
        intensity = max(0.05, min(2.5, intensity))

        if key in self.mappings:
            deltas = self.mappings[key]
            matched = True
        else:
            deltas = {"curiosity": 0.13, "anxiety": 0.07, "joy": -0.04}
            matched = False

        self.emotion.apply(deltas, intensity)
        self.emotion.normalize()
        self.regions.decay()

        if meta.get("bold"):
            self.regions.inject(meta["bold"], intensity)
            self.physio.update_from_session(meta.get("hr", 110))

        # social specific
        if "street" in key:
            self.regions.apply_social_boost("street")
            self.physio.hr = 124
        elif "friend" in key:
            self.regions.apply_social_boost("friend")
            self.physio.hr = 112
        elif "neighbor" in key:
            self.regions.apply_social_boost("neighbor")
            self.physio.hr = 98

        dom = self.emotion.dominant()
        entry = {
            "id": self.counter,
            "stim": key,
            "matched": matched,
            "dom": dom,
            "vec": self.emotion.as_dict(),
            "top_reg": self.regions.top(5),
            "hr": self.physio.hr,
            "arousal": round(self.physio.arousal_index(), 3),
            "fMRI": str(self.viz.path_for(key)),
        }
        self.memory.append(entry)
        return entry

    def replay(self, sid: str = None) -> dict:
        if sid is None:
            s = random.choice(RAW_SESSIONS)
        else:
            s = self.loader.by_id(sid)
            if s is None:
                return {"error": "not found"}
        inten = 1.2 if s.intensity == "high" else 0.85
        return self.process(s.stimulus, inten)

    def force_region(self, region: str, value: float):
        if region in self.regions.act:
            self.regions.act[region] = max(0.01, min(0.99, value))
