import pyperclip
pyperclip.set_clipboard('pbcopy') # override

import fastapi
import time
import beartype
from config import (
    CLIPBOARD_EVENT_ENDPOINT,
    CLIPBOARD_EVENT_PORT,
    CLIPBOARD_UPDATE_INTERVAL,
    HOST_ADDRESS,
    KEYBOARD_EVENT_ENDPOINT,
    KEYBOARD_EVENT_PORT,
    CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT,
)

from dataclass import ClipboardEvent, KeyboardEventTimestamp
import requests
import threading
from kill import kill_and_run
import json

session = requests.Session()
clipboard = ClipboardEvent(content="", timestamp=time.time(), source="mouse")


@beartype.beartype
def copy_to_clipboard(content: str):
    pyperclip.copy(content)


def update_clipboard_event():
    clipboard_content = pyperclip.paste()
    # print("new clipboard content:", clipboard_content)
    # print("old clipboard content:", clipboard["content"])
    clipboard_timestamp = time.time()

    if clipboard_content != clipboard["content"]:
        # print("updated")
        clipboard_source = "mouse"
        keyboard_event_timestamp: KeyboardEventTimestamp = session.get(
            f"http://{HOST_ADDRESS}:{KEYBOARD_EVENT_PORT}{KEYBOARD_EVENT_ENDPOINT}"
        ).json()
        # print("----")
        # print(clipboard_timestamp)
        # print(keyboard_event_timestamp["timestamp"])
        # print(abs(clipboard_timestamp - keyboard_event_timestamp["timestamp"]))
        # print(CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT)
        # print("----")
        if (
            abs(clipboard_timestamp - keyboard_event_timestamp["timestamp"])
            < CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT
        ):
            clipboard_source = "keyboard"

        clipboard["content"] = clipboard_content
        clipboard["timestamp"] = clipboard_timestamp
        clipboard["source"] = clipboard_source
        print("[clipboard listener]", "updated clipboard:", clipboard)


def clipboard_listener():
    while True:
        time.sleep(CLIPBOARD_UPDATE_INTERVAL)
        try:
            update_clipboard_event()
        except ConnectionError:
            print("Keyboard listener is not running.")
        except SystemExit:
            print("Exit because of SystemExit")
            break
        except KeyboardInterrupt:
            print("Exit because of KeyboardInterrupt")
            break
        except json.decoder.JSONDecodeError:
            print("Keyboard event listener is not started.")
            pass
        # except: # let's not
        #     pass


app = fastapi.FastAPI()


@app.get(CLIPBOARD_EVENT_ENDPOINT)
async def get_clipboard():
    global clipboard
    return clipboard


def main():
    # Create a clipboard listener in a separate daemon thread

    clipboard_thread = threading.Thread(target=clipboard_listener, daemon=True)
    clipboard_thread.start()

    kill_and_run(app, port=CLIPBOARD_EVENT_PORT, application_name='clipboard listener')


if __name__ == "__main__":
    main()
