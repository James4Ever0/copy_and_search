import tkinter as tk
from tkinter import messagebox
from clipboard import copy_to_clipboard


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
    def __init__(self):
        super().__init__()
        self.title("Search App")
        self.geometry("600x400")
        self.configure(bg="white")
        self.resizable(False, False)

        # Searched Items List
        self.search_list = tk.Listbox(self, selectmode=tk.SINGLE, height=18, width=64)
        # for i in range(20):
        for i in range(50):  # Adding sample items
            self.search_list.insert(tk.END, f"Item {i}")
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
            self.button_frame, text="Submit", command=self.on_submit
        )
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def on_submit(self):
        # Placeholder for submit button action
        # get textbox content.
        entry_text = self.search_text.get()
        print("[ui]", "searching:", entry_text)
        # search for content.
        messagebox.showinfo("Submit", "Submit button clicked")

    def on_refresh(self):
        # Placeholder for refresh button action
        messagebox.showinfo("Refresh", "Refresh button clicked")


def ui_main():
    frame = AppFrame()
    frame.mainloop()


if __name__ == "__main__":
    ui_main()
