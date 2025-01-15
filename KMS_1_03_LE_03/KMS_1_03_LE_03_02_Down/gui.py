from tkinter_utils import *
import tkinter as tk
from tkinter import ttk
from member_management_class import MemberManagement
from event_management_class import EventManagement

#date and role being mixed up in writing dunno why fix later.
class ClubManagementApp(NotebookBasedGui):
    def __init__(self, root, title="Club Management", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        self.member_manager = MemberManagement("KMS_1_03_LE_03/KMS_1_03_LE_03_02_Down/members.csv")
        self.event_manager = EventManagement("KMS_1_03_LE_03/KMS_1_03_LE_03_02_Down/events.csv", self.member_manager)

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
        self.controller = controller
        self.max_name_length = max((len(member.get_first_name() + " " + member.get_last_name()) for member in self.controller.member_manager.get_members()),default=0)
        print(f"Max name length: {self.max_name_length}")
 
        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)
        
        self.tab1 = InnerNotebookTab(self.inner_notebook, "Add Member",
            widgets=[
            (DropdownMenu, {"options": ["Member", "Comitee Member"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
            (InputFields, {"field_list": [("First Name", "first_name"), ("Last Name", "last_name"), ("Email", "email")]}),
            ]
        )
        
        self.tab2 = InnerNotebookTab(self.inner_notebook, "Remove Member",
            widgets=[
                (InputFields, {"field_list": [("ID", "id")]})
            ]
        )

        self.tab3 = InnerNotebookTab(self.inner_notebook, "Change Status",
            widgets=[
                (DropdownMenu, {"options": ["Member", "Comitee Member"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
                (InputFields, {"field_list": [("ID", "id")]})              
            ]
        )

        self.tab4 = InnerNotebookTab(self.inner_notebook, "Payments",
            widgets=[
                (InputFields, {"field_list": [("ID", "id")]})
            ]
        )
        
        self.tab5 = InnerNotebookTab(self.inner_notebook, "View All",
            widgets=[   
                (ScrollableListbox, {"items": [f"{member.get_id().ljust(4)}: {(member.get_first_name() + ' ' + member.get_last_name()).ljust(self.max_name_length+4)}{'Role: ' + member.get_role().ljust(14)}"for member in self.controller.member_manager.get_members()],})
            ])
        
        Buttons(4, (self.tab1.get_tab_frame(), self.tab2.get_tab_frame(), self.tab3.get_tab_frame(), self.tab4.get_tab_frame()), 
                ("Add new Member", "Remove Member", "Change Member Status", "Pay Membership Fees"),
                (lambda: self.controller.member_manager.add_member(self.tab1.get_field_values()),
                lambda: self.controller.member_manager.remove_member(self.tab2.get_field_values()), 
                lambda: self.controller.member_manager.change_role(self.tab3.get_field_values()),
                lambda: self.controller.member_manager.pay_fees(self.tab4.get_field_values())),
                (tk.TOP,)*no_of_buttons,("w",)*no_of_buttons,(5,)*no_of_buttons,(5,)*no_of_buttons)
        
        self.inner_notebook.bind("<<NotebookTabChanged>>", 
        lambda event: self.tab5.update_inner_tab(
        event,
        "View All",
        [f"{member.get_id().ljust(4)}: {(member.get_first_name() + ' ' + member.get_last_name()).ljust(self.max_name_length+4)}{'Role: ' + member.get_role().ljust(14)}"for member in self.controller.member_manager.get_members()],
        0))
        

        
    
        

class EventManager(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        no_of_buttons = 5
        self.max_event_length = max((len(event.get_event_name()) for event in self.controller.event_manager.get_events()), default=0)
        self.max_location_length = max((len(event.get_event_location()) for event in self.controller.event_manager.get_events()), default=0)


        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)

        self.tab1 = InnerNotebookTab(self.inner_notebook, "Add New Event",
            widgets=[
                (DropdownMenu, {"options": ["Event", "Meeting"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Role"}),
                (InputFields, {"field_list": [("Event Name", "event_name"), 
                                            ("Location", "location"),
                                            ("Date and Time", "date_time"), 
                                            ]})
            ]
        )

        self.tab2 = InnerNotebookTab(self.inner_notebook, "Edit Event",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"),
                                            ("Location", "location"),
                                            ("Date and Time", "date_time"), 
                                            ("Description", "description")]})
            ]
        )

        self.tab3 = InnerNotebookTab(self.inner_notebook, "Remove Event",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name")]})
            ]
        )

        self.tab4 = InnerNotebookTab(self.inner_notebook, "Participant Management",
            widgets=[
                (InputFields, {"field_list": [("Event Name", "event_name"),
                                              ("Participant ID", "id")]})
            ]
        )

        self.tab5 = InnerNotebookTab(self.inner_notebook, "View all Events",
            widgets=[
                (ScrollableListbox, {"items": [event.get_event_name().ljust(self.max_event_length+4) + "Location: " + event.get_event_location().ljust(self.max_location_length+4) + "Date and Time: " + event.get_event_date_time().ljust(15) + "Attendees: "+ ", ".join([attendee for attendee in event.get_attendees()]) for event in self.controller.event_manager.get_events()],
                "scrollbar2": "horizontal",
                "scroll_side2": "bottom",
                })
            ])
   
        Buttons(no_of_buttons, (self.tab1.get_tab_frame(), self.tab2.get_tab_frame(), self.tab3.get_tab_frame(),self.tab4.get_tab_frame(), self.tab4.get_tab_frame()), 
                ("Add a New Event", 
                "Edit an Event",
                "Remove an Event", 
                "Add a Member to an Event",
                "Remove a Member from an Event"),
                (lambda: self.controller.event_manager.add_event(self.tab1.get_field_values()), 
                 lambda: self.controller.event_manager.edit_event(self.tab2.get_field_values()), 
                 lambda: self.controller.event_manager.remove_event(self.tab3.get_field_values()),
                 lambda: self.controller.event_manager.add_member_to_event(self.tab4.get_field_values()),
                 lambda: self.controller.event_manager.remove_member_from_event(self.tab4.get_field_values())), 
                 (tk.TOP,)*no_of_buttons, ("w",)*no_of_buttons, (5,)*no_of_buttons, (5,)*no_of_buttons)

        self.inner_notebook.bind("<<NotebookTabChanged>>", 
        lambda event: self.tab5.update_inner_tab(event,
        "View all Events",
        [event.get_event_name().ljust(self.max_event_length+4) + "  " + "Location: " + event.get_event_location().ljust(self.max_location_length+4) + "Date and Time: " + event.get_event_date_time().ljust(20) + "Attendees: " + ", ".join([attendee for attendee in event.get_attendees()]) for event in self.controller.event_manager.get_events()],
        0))


class ComiteeManagement(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)

        self.tab1 = InnerNotebookTab(self.inner_notebook, "View Comitee",
            widgets=[
                (ScrollableListbox, {"items": [f"{member.get_id():<4}: {(member.get_first_name() + " " + member.get_last_name()).ljust(20)}"
                for member in self.controller.member_manager.get_members() if member.get_role() == "Comitee Member"]})
            ])

        self.tab2 = InnerNotebookTab(self.inner_notebook, "Meetings",
                                widgets=[
                (ScrollableListbox, {"items": [event.get_event_name()+"   "+event.get_event_location()+"   "+event.get_event_date_time() for event in self.controller.event_manager.get_events() if event.get_event_description() == "Meeting"]})])
        
        self.inner_notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        selected_tab = event.widget.index("current")
        if selected_tab == 0:
            self.tab1.update_inner_tab(event,
            "View Comitee",
            [f"{member.get_id():<4}: {(member.get_first_name() + " " + member.get_last_name()).ljust(20)}"
            for member in self.controller.member_manager.get_members() if member.get_role() == "Comitee Member"],
            0)
        elif selected_tab == 1:
            self.tab2.update_inner_tab(
                event,
                "Meetings",
                [event.get_event_name() + "   " + event.get_event_location() + "   " + event.get_event_date_time()
                for event in self.controller.event_manager.get_events() if event.get_event_description() == "Meeting"],
                0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClubManagementApp(root, title="Club Management" )

    def on_close():
        app.member_manager.save_to_csv()
        app.event_manager.save_to_csv()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()