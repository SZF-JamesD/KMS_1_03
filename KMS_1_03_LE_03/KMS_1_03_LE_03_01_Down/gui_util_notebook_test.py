import tkinter as tk
from tkinter import ttk
from tkinter_utils import NotebookBasedGui

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Main Menu").pack()


class AddNew(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Add New Entry").pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookBasedGui(root, title="Test Frame App", geometry="800x800")
    app.add_frames([MainMenu, AddNew])
    app.run()