from scan_data import RAW_SESSIONS, Session
from typing import List, Optional

class SessionLoader:
    def __init__(self):
        self.sessions = RAW_SESSIONS

    def by_id(self, sid: str) -> Optional[Session]:
        for s in self.sessions:
            if s.sid == sid:
                return s
        return None

    def by_stimulus(self, name: str) -> List[Session]:
        name = name.lower()
        return [s for s in self.sessions if name in s.stimulus.lower()]

    def social_only(self) -> List[Session]:
        keys = ["street", "friend", "neighbor"]
        return [s for s in self.sessions if any(k in s.stimulus.lower() for k in keys)]

    def highest_confidence(self) -> Session:
        return max(self.sessions, key=lambda s: s.confidence)
