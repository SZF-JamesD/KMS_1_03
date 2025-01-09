from tkinter_utils import *
import tkinter as tk
from tkinter import ttk, messagebox
from member_management_class import MemberManagement
from datetime import date
from event_management_class import EventManagement

#date and role being mixed up in writing dunno why fix later.
class ClubManagementApp(NotebookBasedGui):
    def __init__(self, root, title="Club Management", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        self.member_manager = MemberManagement("KMS_1_03_LE_03/KMS_1_03_LE_03_02_Down/members.csv")
        self.event_manager = EventManagement("KMS_1_03_LE_03/KMS_1_03_LE_03_02_Down/events.csv")

        self.add_frames([
            GeneralInfo,
            ManageMember,
            EventManager,
            ComiteeManagement
        ])

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        self.frames["GeneralInfo"].refresh_display()


class GeneralInfo(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        info_container = ttk.Frame(self)
        info_container.pack(fill='x', padx=10, pady=10)

        self.total_members_label = ttk.Label(info_container, text="")
        self.total_members_label.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        self.upcoming_event_label = ttk.Label(info_container, text="")
        self.upcoming_event_label.pack()

        self.refresh_display()

    def refresh_display(self):
        self.events = self.controller.event_manager.get_events()
        self.members = self.controller.member_manager.get_members()
        
        self.total_members_label.config(text=f"Total Members: {len(self.members)}")
        self.upcoming_event_label.config(text=f"Upcoming Events:\n{''.join(event.get_event_name() + '\n' for event in self.events)}" 
         if len(self.events) != 0 else "Upcoming Events:\nNo events scheduled.")


class ManageMember(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        no_of_buttons = 4
        max_name_length = max(len(member.get_first_name() + " " + member.get_last_name()) for member in controller.member_manager.get_members())
   
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
        
        tab5 = InnerNotebookTab(inner_notebook, "View All",
            widgets=[   
                (ScrollableListbox, {"items": [f"{member.get_id():<4}: {(member.get_first_name() + " " + member.get_last_name()).ljust(max_name_length+4)} {'Role: ' + (member.get_role())}"
                for member in controller.member_manager.get_members()]})
            ])
            
        Buttons(4, (tab1.get_tab_frame(), tab2.get_tab_frame(), tab3.get_tab_frame(), tab4.get_tab_frame()), 
                ("Add new Member", "Remove Member", "Change Member Status", "Pay Membership Fees"),
                (lambda: controller.member_manager.add_member(tab1.get_field_values()),
                lambda: controller.member_manager.remove_member(tab2.get_field_values()), 
                lambda: controller.member_manager.change_role(tab3.get_field_values()),
                lambda: controller.member_manager.pay_fees(tab4.get_field_values())),
                (tk.TOP,)*no_of_buttons,("w",)*no_of_buttons,(5,)*no_of_buttons,(5,)*no_of_buttons)


class EventManager(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        no_of_buttons = 5

        inner_notebook = ttk.Notebook(self)
        inner_notebook.pack(expand=True, fill=tk.BOTH)

        tab1 = InnerNotebookTab(inner_notebook, "Add New Event",
            widgets=[
                (DropdownMenu, {"options": ["Event", "Meeting"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
                (InputFields, {"field_list": [("Event Name", "event_name"), 
                                            ("Location", "location"),
                                            ("Date and Time", "date_time"), 
                                            ]})
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

        tab4 = InnerNotebookTab(inner_notebook, "Participant Management",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"),
                                              ("Participant ID", "id")]})
            ]
        )

        tab5 = InnerNotebookTab(inner_notebook, "View all Events",
            widgets=[
                (ScrollableListbox, {"items": [event.get_event_name() for event in controller.event_manager.get_events()]})
            ])
   
        Buttons(no_of_buttons, (tab1.get_tab_frame(), tab2.get_tab_frame(), tab3.get_tab_frame(),tab4.get_tab_frame(), tab4.get_tab_frame()), 
                ("Add a New Event", 
                "Edit an Event",
                "Remove an Event", 
                "Add a Member to an Event",
                "Remove a Member from an Event"),
                (lambda: controller.event_manager.add_event(tab1.get_field_values()), 
                 lambda: controller.event_manager.edit_event(tab2.get_field_values()), 
                 lambda: controller.event_manager.remove_event(tab3.get_field_values()),
                 lambda: controller.event_manager.add_member_to_event(tab4.get_field_values()),
                 lambda: controller.event_manager.remove_member_from_event(tab4.get_field_values())), 
                 (tk.TOP,)*no_of_buttons, ("w",)*no_of_buttons, (5,)*no_of_buttons, (5,)*no_of_buttons)


class ComiteeManagement(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        
        inner_notebook = ttk.Notebook(self)
        inner_notebook.pack(expand=True, fill=tk.BOTH)

        tab1 = InnerNotebookTab(inner_notebook, "View Comitee",
            widgets=[
                (ScrollableListbox, {"items": [f"{member.get_id():<4}: {(member.get_first_name() + " " + member.get_last_name()).ljust(20)}"
                for member in controller.member_manager.get_members() if member.get_role() == "Comitee Member"]})
            ])
        
        tab2 = InnerNotebookTab(inner_notebook, "Meetings",
                                widgets=[
                (ScrollableListbox, {"items": [event.get_event_name() for event in controller.event_manager.get_events() if event.get_event_description() == "Meeting"]})])


if __name__ == "__main__":
    root = tk.Tk()
    app = ClubManagementApp(root, title="Club Management" )

    def on_close():
        app.member_manager.save_to_csv()
        app.event_manager.save_to_csv()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()