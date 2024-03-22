from dataclass import AppConfig

HOST_ADDRESS="127.0.0.1"

KEYBOARD_EVENT_PORT=8991
KEYBOARD_EVENT_ENDPOINT="/latest_keypress_timestamp"

CLIPBOARD_PORT=8992
CLIPBOARD_ENDPOINT="/clipboard"

CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT = 1.5
CLIPBOARD_UPDATE_INTERVAL = 0.3
"""in seconds"""