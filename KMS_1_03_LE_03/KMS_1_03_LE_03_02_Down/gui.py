from tkinter_utils import *
import tkinter as tk
from tkinter import ttk, messagebox
from member_management_class import MemberManagement
from datetime import date

#date and role being mixed up in writing dunno why fix later.
class ClubManagementApp(NotebookBasedGui):
    def __init__(self, root, title="Club Management", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        self.member_manager = MemberManagement("KMS_1_03_LE_03/KMS_1_03_LE_03_02_Down/members.csv")

        self.add_frames([
            GeneralInfo,
            ManageMember,
            EventManagement,
            ComiteeManagement
        ])

class GeneralInfo(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)

        self.member_manager = controller.member_manager.members

        info_container = ttk.Frame(self)
        info_container.pack(fill='x', padx=10, pady=10)

        total_members_label = ttk.Label(info_container, text=f"Total Members: {len(self.member_manager)}")
        total_members_label.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        upcoming_event_label = ttk.Label(info_container, text="Upcoming Events: (to be implemented)")
        upcoming_event_label.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=10)


class ManageMember(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        no_of_buttons = 4
        
        inner_notebook = ttk.Notebook(self)
        inner_notebook.pack(expand=True, fill=tk.BOTH)
        tab1 = InnerNotebookTab(inner_notebook, "Add Member",
            widgets=[
            (DropdownMenu, {"options": ["Member", "Comitee Member"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
            (InputFields, {"field_list": [("First Name", "first_name"), ("Last Name", "last_name"), ("Email", "email")]}),
            ]
        )
        
        tab2 = InnerNotebookTab(inner_notebook, "Remove Member",
            widgets=[
                (InputFields, {"field_list": [("ID", "id")]})
            ]
        )

        tab3 = InnerNotebookTab(inner_notebook, "Change Status",
            widgets=[
                (DropdownMenu, {"options": ["Member", "Comitee Member"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
                (InputFields, {"field_list": [("ID", "id")]})              
            ]
        )

        tab4 = InnerNotebookTab(inner_notebook, "Payments",
            widgets=[
                (InputFields, {"field_list": [("ID", "id")]})
            ]
        )
        

        Buttons(4, (tab1.get_tab_frame(), tab2.get_tab_frame(), tab3.get_tab_frame(), tab4.get_tab_frame()), 
                ("Add new Member", "Remove Member", "Change Member Status", "Pay Membership Fees"),
                (lambda: controller.member_manager.add_member(tab1.get_field_values()),
                lambda: controller.member_manager.remove_member(tab2.get_field_values()), 
                lambda: controller.member_manager.change_role(tab3.get_field_values()),
                lambda: controller.member_manager.pay_fees(tab4.get_field_values())),
                (tk.TOP,)*no_of_buttons,("w",)*no_of_buttons,(5,)*no_of_buttons,(5,)*no_of_buttons)


class EventManagement(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        no_of_buttons = 5

        inner_notebook = ttk.Notebook(self)
        inner_notebook.pack(expand=True, fill=tk.BOTH)

        tab1 = InnerNotebookTab(inner_notebook, "Add New Event",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"), 
                                            ("Location", "location"),
                                            ("Date and Time", "date_time"), 
                                            ("Description", "description")]})
            ]
        )

        tab2 = InnerNotebookTab(inner_notebook, "Edit Event",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"),
                                            ("Location", "location"),
                                            ("Date and Time", "date_time"), 
                                            ("Description", "description")]})
            ]
        )

        tab3 = InnerNotebookTab(inner_notebook, "Remove Event",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name")]})
            ]
        )

        tab4 = InnerNotebookTab(inner_notebook, "Participant Management,",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"),
                                              ("Participant ID", "id")]})
            ]
        )
   
        Buttons(no_of_buttons, (tab1.get_tab_frame(), tab2.get_tab_frame(), tab3.get_tab_frame(),tab4.get_tab_frame(), tab4.get_tab_frame()), 
                ("Add a New Event", 
                "Edit an Event",
                "Remove an Event", 
                "Add a Member to an Event",
                "Remove a Member from an Event"),
                (0,)*no_of_buttons, (tk.TOP,)*no_of_buttons, ("w",)*no_of_buttons, (5,)*no_of_buttons, (5,)*no_of_buttons)
        #add new events to list

class ComiteeManagement(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        no_of_buttons = 2
        Buttons(2, (self,)*no_of_buttons, ("View all Comitee Members","Plan Meeting"),(0,)*no_of_buttons,
                (tk.TOP,)*no_of_buttons, ("w",)*no_of_buttons, (5,)*no_of_buttons, (5,)*no_of_buttons)

        #view comitee members and what they do, also upcoming comitee specific things.



if __name__ == "__main__":
    root = tk.Tk()
    app = ClubManagementApp(root, title="Club Management" )

    def on_close():
        app.member_manager.save_to_csv()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()