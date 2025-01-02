#from utils.tkinter_utils import NotebookBasedGui
import tkinter as tk
from tkinter import ttk


class GeneralInfo(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)


class ManageMember(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)


class EventPlanning(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)


class Comitee(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)




if __name__ == "__main__":
    import os
    print("Current working directory:", os.getcwd())
    #print(sys.path)
    root = tk.Tk()
    #app = NotebookBasedGui(root, title="Club Management")
    #app.add_frames([GeneralInfo, ManageMember, EventPlanning, Comitee])

    root.protocol("WM_DELETE_WINDOW", root.quit)

    #app.run()