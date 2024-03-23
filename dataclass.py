from typing_extensions import TypedDict, Literal, TypeAlias
from typing import List

EventSource: TypeAlias = Literal["keyboard", "mouse"]


class AppConfig(TypedDict):
    index_directory: str
    document_directory: str
    event_sources: List[EventSource]


class ClipboardEvent(TypedDict):
    content: str
    timestamp: float
    source: EventSource

class KeyboardEventTimestamp(TypedDict):
    timestamp: float


# data format:
# {"content": <copied text content>, "timestamp": <timestamp since copied>, "source": <keyboard or mouse>}
