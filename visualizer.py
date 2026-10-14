from config import FMRI_STREET, FMRI_FRIEND, FMRI_NEIGHBOR
from pathlib import Path

class Visualizer:
    def __init__(self):
        self.map = {
            "random street dog": FMRI_STREET,
            "best friend dog": FMRI_FRIEND,
            "neighbor dog": FMRI_NEIGHBOR,
            "first exposure neighbor dog": FMRI_NEIGHBOR,
            "later session neighbor dog": FMRI_NEIGHBOR,
        }

    def path_for(self, stimulus: str) -> Path:
        key = stimulus.lower()
        for k, p in self.map.items():
            if k in key:
                return p
        return Path("")

    def exists(self, stimulus: str) -> bool:
        p = self.path_for(stimulus)
        return p.exists() if p else False
