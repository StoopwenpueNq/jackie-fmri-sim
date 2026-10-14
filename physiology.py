from dataclasses import dataclass
from typing import Optional

@dataclass
class PhysioState:
    hr: float = 110.0
    rr: float = 22.0
    spo2: float = 97.0
    temp: float = 38.5
    accel: float = 0.25

    def update_from_session(self, hr: float, rr: float = None, temp: float = None, accel: float = None):
        self.hr = hr
        if rr is not None:
            self.rr = rr
        if temp is not None:
            self.temp = temp
        if accel is not None:
            self.accel = accel

    def arousal_index(self) -> float:
        return (self.hr - 90) / 50.0 + self.accel * 1.4
