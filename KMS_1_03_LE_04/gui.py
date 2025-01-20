from tkinter_utils import *
import tkinter as tk
from tkinter import ttk
from data_utils import DatabaseHandler
from system_info_utils import collect_system_info

class SystemInfoApp(NotebookBasedGui):
    def __init__(self, root, title="System Analysis", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        
        self.db_handler = DatabaseHandler(host="localhost", user="root", password="", database="system_analysis")
        

        self.add_frames([
            SystemInfo,
            SavedData

        ])

class SystemInfo(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.system_info = collect_system_info()
        self.system_info_display = f"{list(self.system_info.keys())}: {list(self.system_info.values())}"
        tk.Label(self, text="Select which info to save:", font=("Arial", 14)).pack(pady=10)
        self.checkboxes = CheckButtons(self, checkbox_data=self.system_info, offvalue="", pady=5)

        Buttons(1, (self,), ("Save Selected Info",), command=(self.save_info,), side=("top",), anchor=("w",), padx=(10,), pady=(10,))

    def save_info(self):
        selected_items = self.checkboxes.get_checkbox_states()
        if not selected_items:
            MessageBoxHandler.show_error("No selection", "Please select at least one piece of information to save.")
            return

        update_value = ", ".join(f"{data}" for data in selected_items.keys())
        check_query = "SELECT COUNT(*) FROM system_info WHERE machine = %s"
        update_query = "UPDATE system_info SET "+ update_value
        insert_query = "INSERT INTO system_info (" +update_value +  ") VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)"
        self.controller.db_handler.save_data(
            main_query=insert_query,
            check_query=check_query,
            update_query=update_query,
            update_params=[selected_items],
            data=[selected_items],
            fetch_all_params=[(item,) for item in selected_items.keys()]
        )



class SavedData(ttk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Previously Saved System Info:", font=("Arial", 14)).pack(pady=10)

        self.data_listbox = ScrollableListbox(self, [], scroll_side2="bottom", scrollbar2="horizontal")

        tk.Button(self, text="Refresh", command=self.refresh_data()).pack(pady=10)

    def refresh_data(self):
        query = "SELECT * FROM system_info"
        saved_data = self.controller.db_handler.fetch_all(query)
        #for dicts in saved_data:
        #    for key, value in dicts.items():

        #formatted_data = [f"{item['field']}: {item['value']}" for item in saved_data]
        #print(formatted_data)

        self.data_listbox.update_items(saved_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoApp(root, title="System Info" )
    
    def on_close():
        try:
            app.db_handler.close()
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()