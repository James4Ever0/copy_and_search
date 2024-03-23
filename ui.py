import tkinter as tk
from tkinter import messagebox
from clipboard import copy_to_clipboard
from search import refresh_index, search_by_query
from typing import List, Callable
import requests
import threading
from config import (
    MONITOR_CLIPBOARD_PERIOD,
    MONITOR_CLIPBOARD_TIMEOUT,
    HOST_ADDRESS,
    CLIPBOARD_EVENT_ENDPOINT,
    CLIPBOARD_EVENT_PORT,
    APP_CONFIG,
)
from dataclass import ClipboardEvent
import http, time

session = requests.Session()

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
        self.clear_search_list()
        for item in items:
            self.search_list.insert(tk.END, item)

    def __init__(self):
        super().__init__()
        self.last_query = ""
        self.title("Search App")
        self.geometry("600x400")
        self.configure(bg="white")
        self.resizable(False, False)

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
            self.button_frame, text="Refresh", command=self.on_refresh
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(
            self.button_frame, text="Search", command=self.on_submit
        )
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def perform_search(self, query: str):
        if query:  # non-empty query
            if query != self.last_query:  # not the same as before
                self.last_query = query
                print("[ui]", "searching:", query)
                items = search_by_query(query)
                self.update_search_list_by_items(items)

    # listen to clipboard.

    def on_submit(self):
        # Placeholder for submit button action
        # get textbox content.
        query = self.search_text.get()
        self.perform_search(query)

    def on_refresh(self):
        # Placeholder for refresh button action
        refresh_index()
        messagebox.showinfo("Refresh", "Index refreshed.")


def monitor_clipboard_and_perform_search(frame: AppFrame):
    while True:
        time.sleep(MONITOR_CLIPBOARD_PERIOD)
        resp = session.get(
            f"http://{HOST_ADDRESS}:{CLIPBOARD_EVENT_ENDPOINT}{CLIPBOARD_EVENT_PORT}"
        )
        if resp.status_code == http.HTTPStatus.OK:
            data = resp.json()
            data = ClipboardEvent(**data)
            if data["source"] in APP_CONFIG["event_sources"]:
                frame.perform_search(data["content"])


def start_daemon_thread(target: Callable, args=(), kwargs={}):
    t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    t.start()


def ui_main():
    frame = AppFrame()
    start_daemon_thread(monitor_clipboard_and_perform_search)
    frame.mainloop()


if __name__ == "__main__":
    ui_main()
