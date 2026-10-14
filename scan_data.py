from dataclasses import dataclass
from typing import Dict, List
import statistics

@dataclass
class Session:
    sid: str
    stimulus: str
    duration: int
    intensity: str
    time: str
    fasting: int
    handler: str
    familiarity: str
    rr: int
    temp: float
    accel: float
    licking: int
    olf_l: float
    olf_r: float
    amyg_l: float
    amyg_r: float
    nacc_l: float
    nacc_r: float
    z_olf: float
    z_amyg: float
    theta: int
    alpha: int
    beta: int
    gamma: int
    trials: int
    rejected: int
    confidence: float
    notes: str

    def bold_vector(self) -> Dict[str, float]:
        return {
            "olf_l": self.olf_l,
            "olf_r": self.olf_r,
            "amyg_l": self.amyg_l,
            "amyg_r": self.amyg_r,
            "nacc_l": self.nacc_l,
            "nacc_r": self.nacc_r,
        }

    def eeg_vector(self) -> Dict[str, float]:
        total = self.theta + self.alpha + self.beta + self.gamma
        return {
            "theta": self.theta / total if total else 0,
            "alpha": self.alpha / total if total else 0,
            "beta": self.beta / total if total else 0,
            "gamma": self.gamma / total if total else 0,
        }

RAW_SESSIONS: List[Session] = [
    Session("J001", "chicken meat", 300, "high", "10:15", 18, "Jackie", "novel food",
            118, 38.6, 0.32, 1, 1.82, 1.28, 2.40, 2.21, 2.21, 4.31, 2.65, 3.2,
            32, 24, 18, 15, 24, 0, 0.89, "high reward, high BOLD, clean data."),
    Session("J002", "best friend dog", 300, "high", "14:22", 12, "Jackie", "very familiar",
            112, 38.4, 0.21, 0, 1.36, 1.68, 0.92, 0.88, 1.55, 1.42, 3.25, 1.80,
            22, 20, 17, 13, 24, 0, 0.83, "expected response, strong BOLD, calm."),
    Session("J003", "random street dog", 300, "medium", "09:47", 16, "Jackie", "unfamiliar",
            126, 38.7, 0.48, 0, 0.65, 0.72, 0.35, 0.41, 0.52, 0.48, 1.45, 0.72,
            36, 25, 16, 10, 24, 3, 0.61, "more movement, 3 trials rejected."),
    Session("J004", "walk", 600, "low", "11:05", 8, "Jackie", "context",
            104, 38.3, 0.18, 0, 0.12, 0.18, -0.05, 0.02, 0.10, 0.08, 0.28, -0.03,
            24, 23, 18, 14, 32, 0, 0.72, "baseline session, low reactivity."),
    Session("J005", "first exposure neighbor dog", 300, "medium", "15:10", 14, "Jackie", "unfamiliar",
            121, 38.5, 0.37, 0, 0.78, 0.95, 0.48, 0.55, 0.68, 0.71, 1.78, 0.93,
            24, 17, 14, 12, 24, 2, 0.64, "first exposure, mild rejection."),
    Session("J006", "later session neighbor dog", 300, "high", "16:45", 10, "Jackie", "now familiar",
            115, 38.4, 0.25, 0, 1.25, 1.49, 0.85, 0.79, 1.12, 1.05, 2.89, 1.58,
            29, 29, 16, 13, 24, 0, 0.81, "model confidence rising, clean."),
]

def aggregate_by_stimulus() -> Dict[str, Dict[str, float]]:
    groups = {}
    for s in RAW_SESSIONS:
        key = s.stimulus.lower()
        if key not in groups:
            groups[key] = {"olf": [], "amyg": [], "nacc": [], "z_olf": [], "z_amyg": [],
                           "theta": [], "alpha": [], "beta": [], "gamma": [], "rr": [], "conf": []}
        b = s.bold_vector()
        groups[key]["olf"].append((b["olf_l"] + b["olf_r"]) / 2)
        groups[key]["amyg"].append((b["amyg_l"] + b["amyg_r"]) / 2)
        groups[key]["nacc"].append((b["nacc_l"] + b["nacc_r"]) / 2)
        groups[key]["z_olf"].append(s.z_olf)
        groups[key]["z_amyg"].append(s.z_amyg)
        groups[key]["theta"].append(s.theta)
        groups[key]["alpha"].append(s.alpha)
        groups[key]["beta"].append(s.beta)
        groups[key]["gamma"].append(s.gamma)
        groups[key]["rr"].append(s.rr)
        groups[key]["conf"].append(s.confidence)
    result = {}
    for k, v in groups.items():
        result[k] = {m: statistics.mean(vals) for m, vals in v.items()}
    return result
