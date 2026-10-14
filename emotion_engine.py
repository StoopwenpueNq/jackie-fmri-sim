from typing import Dict
import math

class EmotionVector:
    __slots__ = ("joy", "curiosity", "calm", "excitement", "anxiety", "affection")

    def __init__(self):
        self.joy = 0.5
        self.curiosity = 0.4
        self.calm = 0.55
        self.excitement = 0.3
        self.anxiety = 0.15
        self.affection = 0.6

    def apply(self, deltas: Dict[str, float], scale: float = 1.0):
        for k, v in deltas.items():
            if hasattr(self, k):
                setattr(self, k, getattr(self, k) + v * scale)
        self._clamp()

    def _clamp(self):
        for k in self.__slots__:
            setattr(self, k, max(0.0, min(1.0, getattr(self, k))))

    def normalize(self):
        self._clamp()
        s = sum(getattr(self, k) for k in self.__slots__)
        if s > 1e-9:
            for k in self.__slots__:
                setattr(self, k, getattr(self, k) / s)

    def dominant(self) -> str:
        return max(self.__slots__, key=lambda k: getattr(self, k))

    def as_dict(self) -> Dict[str, float]:
        return {k: round(getattr(self, k), 4) for k in self.__slots__}

    def dist(self, other: "EmotionVector") -> float:
        return math.sqrt(sum((getattr(self, k) - getattr(other, k)) ** 2 for k in self.__slots__))
