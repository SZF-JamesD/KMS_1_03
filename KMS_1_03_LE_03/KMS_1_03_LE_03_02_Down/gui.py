from tkinter_utils import NotebookBasedGui, Buttons, FrameBasedGui
import tkinter as tk
from tkinter import ttk
from member_management_class import *

class GeneralInfo(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        #display total members, and upcoming event info
        info_container = ttk.Frame(self)
        info_container.pack(fill='x', padx=10, pady=10)

        member_info_label = ttk.Label(info_container, text=f"Total Members: fill this later")
        member_info_label.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

        event_info_label = ttk.Label(info_container, text="Upcoming Events: fill later")
        event_info_label.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=10)


class ManageMember(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        members = {}
        no_of_buttons = 4
        Buttons(4, (self,)*no_of_buttons, ("Add new Member", "Remove Member", "Change Member Status", "Pay Membership Fees"),
                (0,)*no_of_buttons,(tk.TOP,)*no_of_buttons,("w",)*no_of_buttons,(5,)*no_of_buttons,(5,)*no_of_buttons)
        
        #buttons should be new frames instead of opening pop ups, so notebook within notebook, 4 tabs within the main Manage Member tab


class EventManagement(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        events = []
        no_of_buttons = 5
        Buttons(no_of_buttons, (self, )*no_of_buttons, ("Add a New Event", "Edit an Event", "Remove an Event", "Add a Member to an Event","Remove a Member from an Event"),
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
    app = FrameBasedGui(root, title="Club Management")
    app.add_frames([GeneralInfo, ManageMember, EventManagement, ComiteeManagement])

    root.protocol("WM_DELETE_WINDOW", root.quit)

    app.run()