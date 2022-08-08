from rasa.core.tracker_store import InMemoryTrackerStore
from rasa.shared.core.domain import Domain
from rasa.core.brokers.broker import EventBroker
from typing import Optional

class InMemoryTrackerStoreLimited(InMemoryTrackerStore):

    def __init__(
        self, domain: Domain, event_broker: Optional[EventBroker] = None, max_event_history: Optional[int] = 5
    , **kwargs) -> None:
        super().__init__(domain, event_broker, **kwargs)
        self.max_event_history = max_event_history
