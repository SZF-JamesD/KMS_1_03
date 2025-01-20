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
            self.notebook = container
            return container
        else:
            raise ValueError(f"Unsupported container type: {self.container_type}.")
        
    def add_frames(self, frame_classes):
        #add frames from a list of frame classes.
        for frame_class in frame_classes:
            frame = frame_class(self.container, self)
            frame_name = frame_class.__name__
            self.frames[frame_name] = frame

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
    
    def update_inner_tab(self, event, tab_name, update_variable_info, updated_widget_index):
        '''
        To dynamically refresh inner tabs
        event: is normally going to be 'self.inner_notebook.bind("<<NotebookTabChanged>>", InnerNotebookTab.update_inner_tab())'
        tab_name:name of the tab to be updated
        update_variable_info: what is going to be inside the variable, such as a string or list etc
        update_widget: The index of the widget to be updated within the tab.
        '''
        selected_inner_tab = event.widget.tab(event.widget.select(), "text")
        if selected_inner_tab == tab_name:   
            widget_instance = self.widget_instances[updated_widget_index]
            widget_instance.update_items(update_variable_info)

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
    def __init__(self, root, checkbox_names, onvalue, side="top", anchor="w", padx=10, pady=10, offvalue = "" ):
        self.root = root
        self.checkbox_names = checkbox_names
        self.checkboxes = []
        self.checkbox_vars = {}
        self.side = side
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.offvalue = offvalue
        self.onvalue = onvalue

        self.create_checkboxes()

class CheckButtons:
    def __init__(self, root, checkbox_data, offvalue="", side="top", anchor="w", padx=10, pady=10):
        """
        Initialize the CheckButtons widget.

        Args:
            root: The Tkinter root or parent widget.
            checkbox_data: A dictionary with keys as checkbox names and values as checkbox `onvalue`.
            offvalue: The value when the checkbox is not selected.
            side: The side of the parent widget where the checkboxes will be packed.
            anchor: The anchor position of the checkbox text.
            padx: Horizontal padding for the checkboxes.
            pady: Vertical padding for the checkboxes.
        """
        self.root = root
        self.checkbox_data = checkbox_data
        self.checkboxes = []
        self.checkbox_vars = {}
        self.side = side
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.offvalue = offvalue

        self.create_checkboxes()

    def create_checkboxes(self):
        """
        Create checkboxes dynamically based on checkbox_data.
        """
        for name, value in self.checkbox_data.items():
            var = tk.StringVar(value=self.offvalue)  # Default to offvalue
            checkbox = tk.Checkbutton(
                self.root,
                text=f"{name}: {value}",
                variable=var,
                onvalue=value,  # Use value from checkbox_data as onvalue
                offvalue=self.offvalue
            )
            checkbox.pack(side=self.side, anchor=self.anchor, padx=self.padx, pady=self.pady)
            self.checkboxes.append((checkbox, var))
            self.checkbox_vars[name] = var

    def get_checkbox_states(self):
        """
        Get the current states of all checkboxes.

        Returns:
            A dictionary with checkbox names as keys and their current values as values.
        """
        return {name: var.get() for name, var in self.checkbox_vars.items()}
    
    def bind_checkbox_changes(self, callback): #for real time updating of whatever the checkboxes are working with.
        for name, var in self.checkbox_vars.items():
            var.trace_add("write", lambda *args, name=name, var=var: callback(name, var.get()))
    #callback is what function, for example update_graph

    def show_states(self): # purely for debugging, displays state of boxes in the console 
        states = self.get_checkbox_states()

            

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
    def __init__(self, container, options: list, side, anchor, padx, pady, trace_add_value=None, label_text=None, default=None, callback=None):
        self.container = container
        self.label_text = label_text
        self.options = options
        self.default = default  
        self.side = side
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.trace_add_value = trace_add_value #write, read, or unset
        self.callback = callback

        self.string_var = tk.StringVar(value=self.default) 
        self.create_dropdown()

    def create_dropdown(self):
        if self.label_text:
            ttk.Label(self.container, text=self.label_text).pack(side=self.side, anchor=self.anchor, padx=self.padx, pady=self.pady)
        ttk.OptionMenu(self.container, self.string_var, self.default, *self.options).pack(side=self.side, anchor=self.anchor, padx=self.padx, pady=self.pady)
        
        if self.trace_add_value:
            self.string_var.trace_add(self.trace_add_value, self._on_value_change)

    def get_dropdown_value(self):
        return self.string_var.get()
    
    def get_name(self):
        return "dropdown_selection"
    
    def _on_value_change(self, *args):
        if self.callback:
            self.callback(self.string_var.get())

class ScrollableListbox:
    def __init__(self, container, items=None, height=10, width=50, scrollbar1="vertical", scrollbar2=None, scroll_side1="right", scroll_side2=None, scroll_fill="y", listbox_view="yview"):
        """
        A Listbox widget with a vertical scrollbar.

        container: The parent widget/container to place the listbox in.
        items: List of items to populate the listbox with (optional).
        height: The number of visible rows in the listbox.
        width: The width of the listbox in characters.
        scrollbar1: Direction of the scrollbar, vertical or horizontal.
        scrollbar2: Direction of the second scrollbar, vertical or horizontal.
        scroll_side1: Side of the scrollbar.
        scroll_side2: If you want a second scrollbar.
        scroll_fill: Fill axis for scroll bar.
        listbox_view: Direction of the box view.
        """
        self.container = container
        self.items = items or []
        self.height = height
        self.width = width
        self.scrollbar1 = scrollbar1
        self.scrollbar2 = scrollbar2
        self.scroll_side1 = scroll_side1
        self.scroll_side2 = scroll_side2
        self.scroll_fill = scroll_fill
        self.listbox_view = listbox_view


        self.create_listbox()

    def create_listbox(self):
        """Create the Listbox and add a scrollbar."""
        listbox_frame = ttk.Frame(self.container)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the Listbox widget
        self.listbox = tk.Listbox(listbox_frame, font="TkFixedFont", height=self.height, width=self.width)
        

        if self.scrollbar2 == None:
            # Create a Scrollbar for the Listbox
            scrollbar = ttk.Scrollbar(listbox_frame, orient=self.scrollbar1, command=self.listbox_view)
            scrollbar.pack(side=self.scroll_side1, fill=self.scroll_fill)
            
            # Link the scrollbar with the listbox
            if self.scrollbar1 == "vertical":
                self.listbox.config(yscrollcommand=scrollbar.set)
            else:
                self.listbox.config(xscrollcommand=scrollbar.set)

        else:
            if self.scrollbar1 == "vertical":
                h_scrollbar = ttk.Scrollbar(listbox_frame, orient=self.scrollbar2, command=self.listbox.xview)
                h_scrollbar.pack(side=self.scroll_side2, fill="x")
                v_scrollbar = ttk.Scrollbar(listbox_frame, orient=self.scrollbar1, command=self.listbox_view)
                v_scrollbar.pack(side=self.scroll_side1, fill=self.scroll_fill)
                             
            else:
                h_scrollbar = ttk.Scrollbar(listbox_frame, orient=self.scrollbar1, command=self.listbox_view)
                h_scrollbar.pack(side=self.scroll_side1, fill=self.scroll_fill)
                v_scrollbar = ttk.Scrollbar(listbox_frame, orient=self.scrollbar2, command=self.listbox.yview)
                v_scrollbar.pack(side=self.scroll_side2, fill="y")          
            self.listbox.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        # Insert items into the Listbox
        self.update_items(self.items)

    def update_items(self, items):
        """Update the items in the listbox."""
        self.listbox.delete(0, tk.END)  # Clear the current list
        for item in items:
            self.listbox.insert(tk.END, item)  # Add new items

    def get_selected_item(self):
        """Get the currently selected item from the listbox."""
        try:
            selected_index = self.listbox.curselection()
            return self.listbox.get(selected_index)
        except IndexError:
            return None
        

class MessageBoxHandler:
    #utility class for displaying and handling error, warning, and info messages.

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title, message):
        messagebox.showwarning(title, message)

    @staticmethod
    def show_info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def handle_exception(exception):
        exception_message = f"An error occured: {str(exception)}"
        MessageBoxHandler.show_error("Error", exception_message)

class ScrollableText:
    def __init__(self, container, items=None, height=10, width=50, scrollbar="vertical", scroll_side="right", scroll_fill="y"):
        self.container = container
        self.items = items or []
        self.height = height
        self.width = width
        self.scrollbar = scrollbar
        self.scroll_side = scroll_side
        self.scroll_fill = scroll_fill

        self.create_text_widget()

    def create_text_widget(self):
        """Create a Text widget and add a scrollbar."""
        text_frame = ttk.Frame(self.container)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the Text widget
        self.text_widget = tk.Text(text_frame, font="TkFixedFont", height=self.height, width=self.width, wrap="word")

        # Create a Scrollbar for the Text widget
        scrollbar = ttk.Scrollbar(text_frame, orient=self.scrollbar, command=self.text_widget.yview)
        scrollbar.pack(side=self.scroll_side, fill=self.scroll_fill)

        self.text_widget.config(yscrollcommand=scrollbar.set)
        self.text_widget.pack(side="left", fill="both", expand=True)

        # Insert items into the Text widget
        self.update_items(self.items)

    def update_items(self, items):
        """Update the items in the Text widget."""
        self.text_widget.delete(1.0, tk.END)  # Clear the current text
        for item in items:
            self.text_widget.insert(tk.END, item + "\n")  # Add new items, with a newline for each one

    def get_selected_item(self):
        """Get the currently selected item from the Text widget."""
        try:
            selected_index = self.text_widget.index(tk.CURRENT)
            return selected_index
        except IndexError:
            return None