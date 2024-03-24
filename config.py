from dataclass import AppConfig
import os
import json

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


def make_sure_directory_exists(directory: str):
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            raise Exception(f"Path '{directory}' is not a directory")
    else:
        os.mkdir(directory)


APP_CONFIG_PATH = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "config.json")
APP_DEFAULT_INDEX_DIRECTORY = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "index")
APP_DEFAULT_DOCUMENT_DIRECTORY = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "document")
APP_DEFAULT_EVENT_SOURCES = ["keyboard"]
APP_DEFAULT_SEARCH_LIMIT = 10

make_sure_directory_exists(APP_DEFAULT_CONFIG_BASEPATH)
make_sure_directory_exists(APP_DEFAULT_DOCUMENT_DIRECTORY)

APP_DEFAULT_CONFIG = AppConfig(
    index_directory=APP_DEFAULT_INDEX_DIRECTORY,
    document_directory=APP_DEFAULT_DOCUMENT_DIRECTORY,
    event_sources=APP_DEFAULT_EVENT_SOURCES,
    search_limit=APP_DEFAULT_SEARCH_LIMIT,
)

if os.path.exists(APP_CONFIG_PATH):
    with open(APP_CONFIG_PATH, "r") as f:
        APP_CONFIG = AppConfig(**json.load(f))
else:
    with open(APP_CONFIG_PATH, "w+") as f:
        json.dump(APP_DEFAULT_CONFIG, f)
    APP_CONFIG = APP_DEFAULT_CONFIG

SINGLETON_FILELOCK = os.path.join(APP_DEFAULT_CONFIG_BASEPATH, "singleton.lock")
SINGLETON_TIMEOUT = 2

SEARCH_LIMIT = APP_CONFIG['search_limit']

MONITOR_CLIPBOARD_PERIOD = 1
MONITOR_CLIPBOARD_TIMEOUT = 2
