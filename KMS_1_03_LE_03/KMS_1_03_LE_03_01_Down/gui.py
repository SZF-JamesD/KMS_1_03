import tkinter as tk
from tkinter_utils import NotebookBasedGui
from tkinter import ttk

class GeneralInfo(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="General Information")

class AddNewVehicle(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Add New Veihicle")

class SeeRecods(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="See Fleet Records")

class Fueling(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Refuel")

class FuelConsumption(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Fuel Consumption Info")


if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookBasedGui(root, title="Fleet Management")
    app.add_frames([GeneralInfo, AddNewVehicle, SeeRecods, Fueling, FuelConsumption])
    app.run()