from .event_type import EventType

class Event:
    def __init__(self, type: EventType, timestamp: float, source: int, dest: int) -> None:
        self.type = type
        self.timestamp = timestamp
        self.source = source
        self.dest = dest
    
    def __lt__(self, other: 'Event'):
        return self.timestamp < other.timestamp
    
    def __repr__(self) -> str:
        return f'Event(time:{self.timestamp}, type:{self.type}, s:{self.source}, d:{self.dest})'