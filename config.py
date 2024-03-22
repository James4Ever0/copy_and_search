from dataclass import AppConfig
import os

HOST_ADDRESS = "127.0.0.1"

KEYBOARD_EVENT_PORT = 8991
KEYBOARD_EVENT_ENDPOINT = "/latest_keypress_timestamp"

CLIPBOARD_EVENT_PORT = 8992
CLIPBOARD_EVENT_ENDPOINT = "/clipboard"

CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT = 1.5
CLIPBOARD_UPDATE_INTERVAL = 0.3
"""in seconds"""

KILL_ENDPOINT = "/kill"
KILL_TIMEOUT = 2
KILL_INTERVAL = 1

START_PROCESS_INTERVAL = 1

APP_DEFAULT_CONFIG_BASEPATH = os.path.join(os.path.expanduser("~"), ".copy_and_search")

if os.path.exists(APP_DEFAULT_CONFIG_BASEPATH):
    if not os.path.isdir(APP_DEFAULT_CONFIG_BASEPATH):
        raise Exception(f"Path '{APP_DEFAULT_CONFIG_BASEPATH}' is not a directory")
else:
    os.mkdir(APP_DEFAULT_CONFIG_BASEPATH)

APP_CONFIG_PATH = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "config.json")
APP_DEFAULT_INDEX_DIRECTORY = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "index")
APP_DEFAULT_EVENT_SOURCES = ["keyboard"]

APP_DEFAULT_CONFIG = AppConfig(
    index_directory=APP_DEFAULT_INDEX_DIRECTORY, event_sources=APP_DEFAULT_EVENT_SOURCES
)

SINGLETON_FILELOCK = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "singleton.lock")
SINGLETON_TIMEOUT = 2