import tkinter as tk
from tkinter import ttk, messagebox

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
                self.container.add(frame, text=frame_class.__name__)

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