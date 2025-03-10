import tkinter as tk
from tkinter import messagebox
from clipboard import copy_to_clipboard
from search import refresh_index, search_by_query
from typing import List, Callable
from types import SimpleNamespace
import requests
import threading
from requests.exceptions import ConnectionError

from config import (
    MONITOR_CLIPBOARD_PERIOD,
    MONITOR_CLIPBOARD_TIMEOUT,
    HOST_ADDRESS,
    CLIPBOARD_EVENT_ENDPOINT,
    CLIPBOARD_EVENT_PORT,
    APP_CONFIG,
    # APP_CONFIG_PATH,
)
from edit import open_directory_in_explorer  # open_file_in_editor
from dataclass import ClipboardEvent
import http, time

session = requests.Session()

APP_NAME = "复制搜索"

BUTTON_SEARCH = "搜索"
BUTTON_REFRESH = "刷新"
BUTTON_CONFIG = "配置"
REFRESH_DONE_INFO = "索引刷新完成"

"""
Layout:
 __________________________________________
|                                          |
|          ITEM LIST                       |
|                                          |
|__________________________________________|
|        SEARCH BOX     | REFRESH | SUBMIT |
|_______________________|_________|________|

"""


def on_search_list_select(event: "tk.Event[tk.Listbox]"):
    selected_index = event.widget.curselection()
    if selected_index:
        selected_item = event.widget.get(selected_index[0])
        print("[ui]", "selected item:", selected_item)  # , type(selected_item)) # str
        # copy item content.
        copy_to_clipboard(selected_item)


class AppFrame(tk.Tk):
    def clear_search_list(self):
        self.search_list.delete(0, tk.END)

    def update_search_list_by_items(self, items: List[str]):
        print("[ui]", "clearing item list")
        self.clear_search_list()
        for item in items:
            print("[ui]", "inserting item:", item)
            self.search_list.insert(tk.END, item)

    def __init__(self):
        super().__init__()
        self.last_query = ""
        self.title(APP_NAME)
        self.geometry("600x400")
        self.configure(bg="white")
        self.resizable(False, False)

        # Set the window to be always on top
        self.attributes("-topmost", True)

        # Searched Items List
        self.search_list = tk.Listbox(self, selectmode=tk.SINGLE, height=18, width=64)
        self.search_list.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Bind the select event to the Listbox
        self.search_list.bind("<<ListboxSelect>>", on_search_list_select)

        self.search_frame = tk.Frame(self)
        # self.search_frame = tk.Frame(self, height=100, width=580)
        self.search_frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

        # Search Box
        self.search_text = tk.Entry(self.search_frame)
        self.search_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.search_frame)
        self.button_frame.pack(
            side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=False
        )

        self.refresh_button = tk.Button(
            self.button_frame, text=BUTTON_REFRESH, command=self.on_refresh
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(
            self.button_frame, text=BUTTON_SEARCH, command=self.on_submit
        )
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.config_button = tk.Button(
            self.button_frame, text=BUTTON_CONFIG, command=self.on_config
        )
        self.config_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.is_running = True

    def on_config(self):
        open_directory_in_explorer(APP_CONFIG["document_directory"])
        # open_file_in_editor(APP_CONFIG_PATH)

    def perform_search(self, query: str):
        if query:  # non-empty query
            if query != self.last_query:  # not the same as before
                self.last_query = query
                print("[ui]", "searching:", query)
                items = search_by_query(query)
                self.update_search_list_by_items(items)
                return True

    # listen to clipboard.

    def on_submit(self):
        # Placeholder for submit button action
        # get textbox content.
        query = self.search_text.get()
        # let's just override the clipboard.
        copy_to_clipboard(query)
        self.perform_search(query)

    def on_refresh(self):
        # Placeholder for refresh button action
        refresh_index()
        messagebox.showinfo(BUTTON_REFRESH, REFRESH_DONE_INFO, parent=self)


def monitor_clipboard_and_perform_search(frame: AppFrame):
    def main_loop():
        url = f"http://{HOST_ADDRESS}:{CLIPBOARD_EVENT_PORT}{CLIPBOARD_EVENT_ENDPOINT}"
        while True:
            time.sleep(MONITOR_CLIPBOARD_PERIOD)
            if getattr(frame, "is_running", False) is not True:
                print("[ui] main frame is not running.")
                continue
            inner_loop(url)

    def inner_loop(url: str):
        try:
            resp = session.get(url, timeout=MONITOR_CLIPBOARD_TIMEOUT)
        except ConnectionError:
            resp = SimpleNamespace()
            resp.status_code = http.HTTPStatus.BAD_GATEWAY
        if resp.status_code == http.HTTPStatus.OK:
            data = resp.json()
            data = ClipboardEvent(**data)
            if data["source"] in APP_CONFIG["event_sources"]:
                clipboard_content = data["content"]
                is_searched = frame.perform_search(clipboard_content)
                if is_searched:
                    print("[ui]", "performing clipboard search:", clipboard_content)
        else:
            if resp.status_code == http.HTTPStatus.BAD_GATEWAY:
                print("[ui]", "clipboard server is not running")
            else:
                print(
                    "[ui]", "abnormal clipboard server status code:", resp.status_code
                )
            print("[ui]", "abnormal request at:", url)

    main_loop()


def start_daemon_thread(target: Callable, args=(), kwargs={}):
    t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    t.start()


def ui_main():
    frame = AppFrame()
    # start_daemon_thread(frame.mainloop)
    # monitor_clipboard_and_perform_search(frame)
    start_daemon_thread(monitor_clipboard_and_perform_search, args=(frame,))
    frame.mainloop()


# if __name__ == "__main__":
#     ui_main()
