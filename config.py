from typing_extensions import TypedDict, Literal
from typing import List

class AppConfig(TypedDict):
    index_directory:str
    event_sources:List[Literal['keyboard', 'mouse']]