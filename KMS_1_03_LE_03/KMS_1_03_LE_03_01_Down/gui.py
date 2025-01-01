import tkinter as tk
from tkinter_utils import NotebookBasedGui
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import graph_utils, datetime, inspect
from vehicle_class import Vehicle, Car, Truck, Bicycle, Motorcycle
from file_utils import read_json, write_json, write_csv_data

class GeneralInfo(ttk.Frame):#total vehicles, time, date 
    def __init__(self, parent, controller):
        super().__init__(parent)
        data = read_json("company_vehicles.json")
        ttk.Label(self, text="General Information")

        self.info_container = ttk.Frame(self)
        self.info_container.pack(fill='x', padx=10, pady=10)

        self.date_time_label = ttk.Label(self.info_container, font=("Helvetica", 10))
        self.date_time_label.pack(side=tk.LEFT, padx=10)

        self.info_label = ttk.Label(self.info_container, text=f"Total Vehicles: {len(data)}")
        self.info_label.pack(side=tk.RIGHT, padx=10)

        self.update_time()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y\n%H:%M:%S")
        self.date_time_label.config(text=current_time)
        self.after(1000, self.update_time)


class AddNewVehicle(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Add New Veihicle").grid(row=0, column=0, columnspan=2, pady=10)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="New Vehicle Info").grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        ttk.Label(self, text="Type of Vehicle").grid(row=1, column=0, sticky="w", padx=5, pady=5)
                
        self.entries = {}
        self.vehicle_classes = {"Car": Car, 
                                "Truck": Truck, 
                                "Motorcycle": Motorcycle, 
                                "Bicycle": Bicycle}
        
        self.vehicle_var = tk.StringVar()
        self.vehicle_dropdown = ttk.Combobox(self, textvariable=self.vehicle_var, values=[key.capitalize() for key in self.vehicle_classes.keys()], state="readonly")
        self.vehicle_dropdown.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.vehicle_dropdown.set("Select Vehicle Type")
        self.vehicle_dropdown.bind("<<ComboboxSelected>>", self.update_fields)

        self.create_fields(self.get_fields(Vehicle))


    def get_fields(self, cls):
        # Get parameters of Vehicle's __init__ method
        base_params = inspect.signature(Vehicle.__init__).parameters
        base_fields = list(base_params.keys())[1:]  # Skip 'self'

        # Get parameters of the subclass's __init__ method
        subclass_params = inspect.signature(cls.__init__).parameters
        subclass_fields = [
            name for name in subclass_params.keys()
            if name not in base_params and name != 'self'
        ]

        return base_fields + subclass_fields

    def create_fields(self, field_names):
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 3: #avoids clearing the dropdown or label
                widget.destroy()

        #print(f"Creating fields: {field_names}")

        self.entries.clear()
        for i, field_name in enumerate(field_names, start=4):
            ttk.Label(self, text=f"{field_name.replace('_', ' ').capitalize()}").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, sticky="e", padx=5, pady=5)
            self.entries[field_name] = entry
        ttk.Button(self, text="Confirm", command=self.add_new).grid(row=i+2, column=0, sticky="w", padx=5, pady=5)

    def update_fields(self, event):
        vehicle_type = self.vehicle_var.get()
        #print(f"selected vehicle type: {vehicle_type}")
        vehicle_class = self.vehicle_classes.get(vehicle_type, Vehicle)
        #print(f"mapped class: {vehicle_class.__name__}")
        #print(f"Valid keys in vehicle_classes: {list(self.vehicle_classes.keys())}")

        fields = self.get_fields(vehicle_class)
        #print(f"Fields for {vehicle_type}: {fields}")
        self.create_fields(fields)
        

    def add_new(self):
        vehicle_type = self.vehicle_var.get()
        if vehicle_type == "Select Vehicle Type":
            print("Error, please select a vehicle type.")
            return
        
        vehicle_data = {}
        for field_name, entry in self.entries.items():
            value = entry.get()
            vehicle_data[field_name] = value

        vehicle_data["type"] = vehicle_type

        write_json("company_vehicles.json", [vehicle_data])
        print("New vehicle added successfully!")   


class RecordsAndFueling(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="See Fleet Records").pack(pady=10)
        self.data = read_json("company_vehicles.json")
        self.columns = self.extract_columns(self.data)

        self.tree_vert_scroll = ttk.Scrollbar(self, orient="vertical")
        self.tree_vert_scroll.pack(side="right", fill="y")

        self.tree_hor_scroll = ttk.Scrollbar(self, orient="horizontal")
        self.tree_hor_scroll.pack(side="bottom", fill="x")

        self.filter_entry = ttk.Combobox(self, values=["All", "Car", "Truck", "Motorcycle", "Bicycle"], state="readonly")
        self.filter_entry.set("All")
        self.filter_entry.pack(side="left", padx=5)
        self.filter_button = ttk.Button(self, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(side="left")

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        for col in self.columns:
           self.tree.heading(col, text=col)
           self.tree.column(col, width=100)

        self.tree_hor_scroll.config(command=self.tree.xview)
        self.tree_vert_scroll.config(command=self.tree.yview)

        self.load_data(self.data)

        ttk.Label(self, text="Refuel Selected Vehicle").pack(pady=10)

        fuel_input_frame = ttk.Frame(self)
        fuel_input_frame.pack(pady=5)

        ttk.Label(fuel_input_frame, text="Fuel Amount (L):").pack(side="left", padx=5)
        self.fuel_entry = ttk.Entry(fuel_input_frame)
        self.fuel_entry.pack(side="left", padx=5)

        self.fuel_type = ttk.Combobox(self, text="Select Fuel Type", values=["Gasoline", "Diesel"], state="readonly")
        self.fuel_type.set("Gasoline")
        self.fuel_type.pack(side="left", padx=5)
        

        self.refuel_button = ttk.Button(self, text="Refuel", command=self.refuel_selected)
        self.refuel_button.pack(side="left", padx=10)

    def extract_columns(self, data):
        if not data:
            return []
        col_names = []
        for items in data:
            for keys in items.keys():
                if keys not in col_names:
                    col_names.append(keys)
        return col_names

    def load_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in data:
            self.tree.insert("", "end", values=[row.get(col, "") for col in self.columns])
        
    def apply_filter(self):
        selected_filter = self.filter_entry.get()
        if selected_filter == "All":
            filtered_data = self.data
        else:
            filtered_data = [row for row in self.data if row.get("type") == selected_filter]
        self.load_data(filtered_data)

    def refuel_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a vehicle to refuel.")
            return
        
        reg_no = self.tree.item(selected_item[0], "values")[1]
        fuel_amount = self.fuel_entry.get()
        fuel_type = self.fuel_type.get()

        if not fuel_amount.isdigit() or float(fuel_amount) <= 0:
            messagebox.showerror("Error", "Please enter a valid fuel amount.")
            return
        
        if fuel_type not in ["Gasoline", "Diesel"]:
            messagebox.showerror("Error", "Something went wrong with fuel type selection.")
            return

        fuel_amount = float(fuel_amount)

        for vehicle in self.data:
            if vehicle["registration_no"] == reg_no:
                current_fuel = float(vehicle.get("current_fuel_level", 0))
                fuel_capacity = float(vehicle.get("fuel_capacity", 0))

                if current_fuel + fuel_amount > fuel_capacity:
                    messagebox.showerror("Error", "Fuel amount exceeds the vehicle's capacity.")
                    return
                
                vehicle["current_fuel_level"] = current_fuel + fuel_amount
                write_json("company_vehicles.json", self.data)
                write_csv_data("monthly_fuel_consumption.csv", fuel_type, fuel_amount)
                self.load_data(self.data)
                messagebox.showinfo("Success", f"Added {fuel_amount}L of {fuel_type} to {reg_no}.")
                FuelConsumption.update_graph()
                return
            
        messagebox.showerror("Error", "Vehicle not found.")


class FuelConsumption(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Fuel Consumption Info")

        self.graph_container = ttk.Frame(self)
        self.graph_container.pack(fill=tk.BOTH, expand=True)

        self.update_graph()

    def update_graph(self):
        for widget in self.graph_container.winfo_children():
            widget.destroy()

        fig = graph_utils.show_graph()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = NotebookBasedGui(root, title="Fleet Management")
    app.add_frames([GeneralInfo, AddNewVehicle, RecordsAndFueling, FuelConsumption])

    root.protocol("WM_DELETE_WINDOW", root.quit)

    app.run()