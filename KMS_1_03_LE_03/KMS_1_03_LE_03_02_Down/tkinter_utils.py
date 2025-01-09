import tkinter as tk
from tkinter import ttk, messagebox
import re

class BaseGui:
    def __init__(self, root, title="Application", geometry="800x600", resizable=(False, False), container_type="frame"):
        #initialize app with root window, title, geometry, resizability, and container type
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(*resizable)

        #choose container type
        self.container_type = container_type
        self.container = self._create_container()

        self.frames = {}

    def _create_container(self):
        #creates main container based on the container type variable.
        if self.container_type == "frame":
            container = ttk.Frame(self.root)
            container.pack(fill="both", expand=True)
            return container
        elif self.container_type == "notebook":
            container = ttk.Notebook(self.root)
            container.pack(fill="both", expand=True)
            return container
        else:
            raise ValueError(f"Unsupported container type: {self.container_type}.")
        
    def add_frames(self, frame_classes):
        #add frames from a list of frame classes.
        for frame_class in frame_classes:
            frame = frame_class(self.container, self)
            self.frames[frame_class] = frame

            if self.container_type == "frame":
                frame.grid(row=0, column=0, sticky="nsew")
            elif self.container_type == "notebook":
                self.container.add(frame, text=re.sub( r"([A-Z])", r" \1", frame_class.__name__).split())

    def show_frame(self, frame_class):
        #raise the specified frame (only applies to "frame" container type).
        if self.container_type == "frame":
            frame = self.frames[frame_class]
            frame.tkraise()
        else:
            raise RuntimeError("show_frame is not supported for container type 'notebook'.")
        
    def run(self):
        #starts tkinter main loop
        self.root.mainloop()

    def handle_error(self, title, message):
        #show an error message dialog.
        messagebox.showerror(title, message)

class FrameBasedGui(BaseGui):
    def __init__(self, root, title="Frame-Based", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable, container_type="frame")

class NotebookBasedGui(BaseGui):
    def __init__(self, root, title="Notebook-Based", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable, container_type="notebook")

class InnerNotebookTab:
    def __init__(self, notebook, tab_name, widgets=None):
        """
        Initialize a tab within a notebook.

        :param notebook: The parent notebook (ttk.Notebook instance).
        :param tab_name: Name of the tab.
        :param widgets: A list of (widget_class, kwargs) tuples defining the widgets to add.
        """
        self.notebook = notebook
        self.tab_name = tab_name
        self.widgets = widgets or []
        self.tab_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_frame, text=self.tab_name)

        self.widget_instances = []

        self.add_widgets()

    def add_widgets(self):
        for widget_class, widget_kwargs in self.widgets:
            #if widget_class == InputFields:
            widget_instance = widget_class(self.tab_frame, **widget_kwargs)
            self.widget_instances.append(widget_instance)
            #else:
            #    widget = widget_class(self.tab_frame, **widget_kwargs)
            #    widget.pack(pady=5, padx=5)


    def get_field_values(self):
        field_values = {}

        for widget_instance in self.widget_instances:
            # Check if the widget instance has a get_field_values method
            if hasattr(widget_instance, "get_input_field_values"):
                field_values.update(widget_instance.get_input_field_values())
            elif hasattr(widget_instance, "get_dropdown_value"):
                # For widgets like DropdownMenu
                field_values[widget_instance.get_name()] = widget_instance.get_dropdown_value()
        #print(field_values)
        return field_values
        

    def get_tab_frame(self):
        return self.tab_frame


class InputFields:
    def __init__(self, container, field_list):
        self.container = container
        self.field_list = field_list
        self.entries = {}

        self.create_input_fields()

    def create_input_fields(self):
        for field_label, field_name in self.field_list:
            frame = ttk.Frame(self.container)
            frame.pack(fill="x", pady=5)
            ttk.Label(frame, text=f"{field_label}:").pack(side="left", padx=5, anchor="w")
            entry = ttk.Entry(frame)
            entry.pack(side="right", fill="x", expand=True, padx=5)
            self.entries[field_name] = entry

    def get_input_field_values(self):
        field_values = {}
        for field_name, entry in self.entries.items():
            field_values[field_name] = entry.get()

        return field_values


class CheckButtons:
    def __init__(self, root, checkbox_names, start_row=0, start_column=0):
        self.root = root
        self.checkbox_names = checkbox_names
        self.checkboxes = []
        self.start_row = start_row
        self.start_column = start_column
        self.checkbox_vars = {}

        self.create_checkboxes()

        def create_checkboxes(self):
            for i, name in enumerate(self.checkbox_names):
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self.root, text=name, variable=var)
                checkbox.grid(row=self.start_row + i, column=self.start_column, sticky="w")
                self.checkboxes.append((checkbox, var))
                self.checkbox_vars[name] = var
            
        def get_checkbox_states(self): #good for selecting a bunch and then confirming with another button. no real time updating.
            return {name: var.get() for (checkbox, var), name in zip(self.checkboxes, self.checkbox_names)}
        
        def bind_checkbox_changes(self, callback): #for real time updating of whatever the checkboxes are working with.
            for name, var in self.checkbox_vars.items():
                var.trace_add("write", lambda *args, name=name, var=var: callback(name, var.get()))
        #callback is what function, for example update_graph

        def show_states(self): # purely for debugging, displays state of boxes in the console 
            states = self.get_checkbox_states()
            print("Checkbox states:", states)

class Buttons:
    def __init__(self, amount: int, location: tuple, text: tuple, command: tuple, side: tuple, anchor: tuple, padx: tuple, pady: tuple):
        self.amount = amount
        self.location = location
        self.text = text
        self.command = command
        self.side = side
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.buttons = []
        #edit this to take a number (how many buttons, and then tuples or lists for each other thing, then a loop that goes through in range(amount)
        #and goes through the index in each item, ie location[0], text[0] etc to create each button)
        self.create_buttons()

    def create_buttons(self):
        for i in range(self.amount):
            self.buttons.append(ttk.Button(self.location[i], text=self.text[i], command=self.command[i]).pack(side=self.side[i], anchor=self.anchor[i], padx=self.padx[i], pady=self.pady[i]))
        return self.buttons


class DropdownMenu:
    def __init__(self, container, options: list, side, anchor, padx, pady,label_text=None, default=None):
        self.container = container
        self.label_text = label_text
        self.options = options
        self.default = default  
        self.side = side
        self.anchor = anchor
        self.padx = padx
        self.pady = pady

        self.string_var = tk.StringVar(value=self.default) 
        self.create_dropdown()

    def create_dropdown(self):
        if self.label_text:
            ttk.Label(self.container, text=self.label_text).pack(side=self.side, anchor=self.anchor, padx=self.padx, pady=self.pady)
        ttk.OptionMenu(self.container, self.string_var, self.default, *self.options).pack(side=self.side, anchor=self.anchor, padx=self.padx, pady=self.pady)

    def get_dropdown_value(self):
        return self.string_var.get()
    
    def get_name(self):
        return "dropdown_selection"

'''
class DropdownMenu(ttk.Frame):
    def __init__(self, parent, label_text, options, default=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.label_text = label_text
        self.options = options
        self.default = default or options[0]

        self.variable = tk.StringVar(value=self.default)

        self._create_components()

    def _create_components(self):
        ttk.Label(self, text=self.label_text).pack(side=tk.LEFT, anchor = "w", padx=5, pady=5)
        self.dropdown = ttk.OptionMenu(self, self.variable, self.default, *self.options)
        self.dropdown.pack(side=tk.LEFT, anchor = "w", padx=5, pady=5)

    def get_value(self):
        return self.variable.get()'''