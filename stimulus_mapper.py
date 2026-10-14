from typing import Dict, Tuple
from scan_data import aggregate_by_stimulus, RAW_SESSIONS

class StimulusMapper:
    def __init__(self):
        self.agg = aggregate_by_stimulus()
        self.lookup = self._build()

    def _build(self) -> Dict[str, Dict]:
        table = {}
        for s in RAW_SESSIONS:
            key = s.stimulus.lower()
            table[key] = {
                "bold": s.bold_vector(),
                "eeg": s.eeg_vector(),
                "hr": s.rr,
                "intensity": s.intensity,
                "familiarity": s.familiarity,
                "confidence": s.confidence,
                "z_olf": s.z_olf,
                "z_amyg": s.z_amyg,
            }
        # explicit social overrides
        table["random street dog"] = table.get("random street dog", table.get("random street dog", {}))
        table["best friend dog"] = table.get("best friend dog", {})
        table["neighbor dog"] = table.get("later session neighbor dog", table.get("first exposure neighbor dog", {}))
        return table

    def resolve(self, text: str) -> Tuple[str, Dict]:
        t = text.lower().strip()
        if t in self.lookup:
            return t, self.lookup[t]
        # fuzzy social
        if "street" in t or "random" in t:
            return "random street dog", self.lookup.get("random street dog", {})
        if "best friend" in t or "friend" in t:
            return "best friend dog", self.lookup.get("best friend dog", {})
        if "neighbor" in t:
            return "neighbor dog", self.lookup.get("neighbor dog", {})
        return t, {}
