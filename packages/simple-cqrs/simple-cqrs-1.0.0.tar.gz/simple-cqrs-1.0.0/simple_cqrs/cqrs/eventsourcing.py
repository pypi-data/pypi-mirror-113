from typing import List, Optional

from simple_cqrs.domain_event import DomainEvent


class EventStream:
    def __init__(self, events: List[DomainEvent], version: Optional[int]):
        self.events = events
        self.version = version

    @staticmethod
    def new(events: List[DomainEvent] = None):
        return EventStream(events or [], None)
