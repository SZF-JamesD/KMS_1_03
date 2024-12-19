import tkinter as tk
from tkinter import ttk
from tkinter_utils import FrameBasedGui

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Main Menu").pack()
        ttk.Button(self, text="Go to Add New", command=lambda: self.controller.show_frame(AddNew)).pack(pady=10)

class AddNew(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Add New Entry").pack()
        ttk.Button(self, text="Go to Main Manu", command=lambda: self.controller.show_frame(MainMenu)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FrameBasedGui(root, title="Test Frame App", geometry="800x800")
    app.add_frames([MainMenu, AddNew])
    app.show_frame(MainMenu)
    app.run()