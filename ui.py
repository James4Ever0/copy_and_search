import tkinter as tk
from tkinter import messagebox

class AppFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search App")
        self.geometry("600x400")
        self.configure(bg='white')

        # Search Box
        self.search_text = tk.Entry(self)
        self.search_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.on_refresh)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Searched Items List
        self.search_list = tk.Listbox(self, selectmode=tk.SINGLE)
        for i in range(50):  # Adding sample items
            self.search_list.insert(tk.END, f"Item {i}")
        self.search_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_submit(self):
        # Placeholder for submit button action
        messagebox.showinfo("Submit", "Submit button clicked")

    def on_refresh(self):
        # Placeholder for refresh button action
        messagebox.showinfo("Refresh", "Refresh button clicked")

def ui_main():
    frame = AppFrame()
    frame.mainloop()

if __name__ == '__main__':
    ui_main()
