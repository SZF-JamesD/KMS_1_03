from tkinter_utils import *
import tkinter as tk
from tkinter import ttk
from data_utils import DatabaseHandler
from validation_utils import is_valid_name, is_valid_address, is_valid_email_address, is_valid_phone_number, is_valid_date
from customer_manager_class import CustomerManager
from vehicle_manager_class import VehicleManager
from rental_history_mananger_class import RentalHistoryManager

class RentalCompanyApp(NotebookBasedGui):
    def __init__(self, root, title="System Analysis", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        
        self.db_handler = DatabaseHandler(host="localhost", user="root", password="", database="vehicle_rental_management")
        self.vehicle_manager = VehicleManager(self.db_handler)
        self.customer_manager = CustomerManager(self.db_handler)
        self.rental_manager = RentalHistoryManager(self.db_handler)

        self.add_frames([
            VehicleManagement,
            CustomerManagement,
            RentalManagement,
            SavedData
        ])

class VehicleManagement(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #add, edit, remove on one tab +validation

        self.veh_fields = InputFields(self, [("Brand", "brand"), ("Model", "model"), ("Registration No.", "reg_no")])
        self.status_dropdown = DropdownMenu(self,[("available"), ("rented"),( "maintenance")], side="top", anchor="w", padx=5, pady=5, default="available")

        Buttons(3, (self,)*3, ("Save Vehicle", "Edit Vehicle", "Delete Vehicle"),
                (lambda: self.on_button_click("add_vehicle"),
                 lambda: self.on_button_click("add_vehicle"),
                 lambda: self.on_button_click("delete_vehicle")),
                 ("left",)*3, ("n", )*3, (5, )*3, (5, )*3)
        
    def on_button_click(self, function):
        field_values = self.veh_fields.get_input_field_values()
        field_values["vehicle_status"] = self.status_dropdown.get_dropdown_value()
        method = getattr(self.controller.vehicle_manager, function, None)
        
        if method:
            method(field_values)

class CustomerManagement(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #add, edit, remove +vaöidation

        self.customer_field = InputFields(self, [("First Name", "first_name"), ("Last Name", "last_name"), ("Phone Number", "telephone_number"), ("Email", "email")])
        self.payment_dropdown = DropdownMenu(self, [("card"), ("cash")], side="top", anchor="w", padx="5", pady="5", default="card")

        Buttons(3, (self,)*3, ("Save Customer", "Edit Customer", "Delete Customer"),
                (lambda: self.on_button_click("add_customer"),
                 lambda: self.on_button_click("add_customer"),
                 lambda: self.on_button_click("delete_customer")),
                 ("left",)*3, ("n", )*3, (5, )*3, (5, )*3)


    def on_button_click(self, function):
        field_values = self.customer_field.get_input_field_values()
        field_values["payment_choice"] = self.payment_dropdown.get_dropdown_value()
        method = getattr(self.controller.customer_manager, function, None)
        if method:
            method(field_values)


class RentalManagement(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #add remove + date validation

        self.rental_field = InputFields(self, [("First Name", "first_name"), ("Last Name", "last_name"), ("Registration No.", "reg_no"), ("Rental Start (YYYY-MM-DD)", "rental_start"), ("Rental End (YYYY-MM-DD)","rental_end")])


        Buttons(2, (self, )*2, ("Add Rental", "Remove Rental"),
                (lambda: self.on_button_click("add_rental"),
                 lambda: self.on_button_click("delete_rental")),
                 ("left", )*2, ("n", )*2, (5,)*2, (5,)*2)
        
    def on_button_click(self, function):
        field_values = self.rental_field.get_input_field_values()
        method = getattr(self.controller.rental_manager, function, None)
        if method:
            method(field_values)

class SavedData(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        

        self.filter_option = DropdownMenu(self, [("Vehicles"), ("Customers"), ("Rentals")],side="top", anchor="w", padx="5", pady="5", default="Select A Filter", trace_add_value="write", callback=self.handle_dropdown_selection)

        self.view = ScrollableListbox(self, scrollbar2="horizontal", scroll_side2="bottom")

    def handle_dropdown_selection(self, selected_value):
        self.load(selected_value)

    def load(self, selected_value):
        table_name = ""
        if selected_value == "Vehicles":
            table_name = "vehicle_info"
        elif selected_value == "Customers":
            table_name = "customer_info"
        else:
            table_name = "rental_history"
        # Define the main query to fetch all albums
        main_query = f"SELECT * FROM {table_name}"
        data = self.controller.db_handler.fetch_all(main_query)
        
        self.view.update_items(data)
            

if __name__ == "__main__":
    root = tk.Tk()
    app = RentalCompanyApp(root, title="System Info" )
    
    def on_close():
        try:
            app.db_handler.close()
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()