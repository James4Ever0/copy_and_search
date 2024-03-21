import pyperclip
import fastapi
import time
from config import (
    CLIPBOARD_ENDPOINT,
    CLIPBOARD_PORT,
    HOST_ADDRESS,
    KEYBOARD_EVENT_ENDPOINT,
    KEYBOARD_EVENT_PORT,
    CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT,
)
from dataclass import ClipboardEvent, KeyboardEventTimestamp
import requests

session = requests.Session()
clipboard = ClipboardEvent(
            content="", timestamp=time.time(), source="mouse"
        )

def update_clipboard_event(init=False):
    global clipboard, session
    clipboard_content = pyperclip.paste()
    clipboard_timestamp = time.time()
    
    if clipboard_content != clipboard.content:
        clipboard_source = "mouse"
        keyboard_event_timestamp: KeyboardEventTimestamp = session.get(
            f"http://{HOST_ADDRESS}:{KEYBOARD_EVENT_PORT}/{KEYBOARD_EVENT_ENDPOINT}"
        ).json()
        if (
            abs(clipboard_timestamp - keyboard_event_timestamp["timestamp"])
            < CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT
        ):
            clipboard_source = "keyboard"
        ret = ClipboardEvent(
            content=clipboard_content,
            timestamp=clipboard_timestamp,
            source=clipboard_source,
        )
    return ret


def get_clipboard_change(): ...


def get_clipboard_source(): ...
