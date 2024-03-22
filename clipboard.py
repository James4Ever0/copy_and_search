import pyperclip
import fastapi
import time
from config import (
    CLIPBOARD_ENDPOINT,
    CLIPBOARD_PORT,
    CLIPBOARD_UPDATE_INTERVAL,
    HOST_ADDRESS,
    KEYBOARD_EVENT_ENDPOINT,
    KEYBOARD_EVENT_PORT,
    CLIPBOARD_SOURCE_AS_KEYBOARD_TIMELIMIT,
)

from dataclass import ClipboardEvent, KeyboardEventTimestamp
import requests
import threading

session = requests.Session()
clipboard = ClipboardEvent(content="", timestamp=time.time(), source="mouse")


def update_clipboard_event():
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


def clipboard_listener():
    while True:
        time.sleep(CLIPBOARD_UPDATE_INTERVAL)
        try:
            update_clipboard_event()
        except SystemExit:
            print("Exit because of SystemExit")
            break
        except KeyboardInterrupt:
            print("Exit because of KeyboardInterrupt")
            break
        except:
            pass


app = fastapi.FastAPI()

@app.get(CLIPBOARD_ENDPOINT)
async def get_clipboard():
    global clipboard
    return clipboard

def main():
    # Create a clipboard listener in a separate daemon thread
    
    clipboard_thread = threading.Thread(target=clipboard_listener, daemon=True)
    clipboard_thread.start()

    import uvicorn
    uvicorn.run(app, host=HOST_ADDRESS, port=CLIPBOARD_PORT)

if __name__ == "__main__":
    main()