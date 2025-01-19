from tkinter_utils import *
import tkinter as tk
from tkinter import ttk
from album_manager_class import AlbumManager
from data_utils import DatabaseHandler

class MusicManagementApp(NotebookBasedGui):
    def __init__(self, root, title="Music Management", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        
        self.db_handler = DatabaseHandler(host="localhost", user="root", password="", database="music_management")
        self.album_manager = AlbumManager(self.db_handler)

        self.add_frames([
            AlbumManagment
        ])

class AlbumManagment(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.all_albums = self.controller.album_manager.load_all_albums()
        self.max_artist_name_length, self.max_track_title_length = (
            max(
                (len(album.get_artist()) for album in self.all_albums),
                default=0),
            max(
                (len(track.get_title()) for album in self.all_albums for track in album.get_track_list()),
                default=0))

        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)

        self.tab1 = InnerNotebookTab(self.inner_notebook, "Music Collection",
            widgets=[
            (ScrollableText, {"items": [],
                                
                                }),
            ]
        )

        self.tab2 = InnerNotebookTab(self.inner_notebook, "Manage Album Collection",
            widgets=[
                (InputFields, {"field_list": [("Album Title", "album_title"), ("Artist", "artist")]})
            ]
        )

        self.tab3 = InnerNotebookTab(self.inner_notebook, "Manage Tracks",
            widgets=[   
                 (DropdownMenu, {"options": [(album.get_album_title()) for album in self.controller.album_manager.load_all_albums()],"side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Album"}),
                (InputFields, {"field_list": [("Track Title", "track_title"), ("Duration", "duration"), ("MP3 File", "mp3_file") ]})
            ])
        
        Buttons(4, (self.tab2.get_tab_frame(), self.tab2.get_tab_frame(), self.tab3.get_tab_frame(), self.tab3.get_tab_frame()),
                ("Add new Album", "Remove Album", "Add new Track", "Remove Track"),
                (lambda: self.controller.album_manager.save_album(self.tab2.get_field_values()),
                lambda:self.controller.album_manager.delete_album(self.tab2.get_field_values()),
                lambda:self.controller.album_manager.save_track(self.tab3.get_field_values()),
                lambda:self.controller.album_manager.delete_track(self.tab3.get_field_values())),
                (tk.TOP,)*4, ("w",)*4, (5,)*4, (5,)*4
                )

        self.inner_notebook.bind(
            "<<NotebookTabChanged>>",
            lambda event: self.update_music_collection_text(event)
        )

    def update_music_collection_text(self, event):
        # Ensure we update only when the tab index changes to the "Music Collection" tab
        if self.inner_notebook.index(self.inner_notebook.select()) == 0:  # 0 is the index for "Music Collection"
            # Prepare the new content for the text box dynamically
            self.tab1.update_inner_tab(
            event,
            "Music Collection",  
            [
            f"{album.get_artist().ljust(self.max_artist_name_length + 4)} {album.total_duration()}    {album.get_album_title()} \nTrack List:\n" +
            "".join(
                track.get_title().ljust(self.max_track_title_length + 4) +
                track.get_duration().ljust(6) + " " +
                track.get_mp3_file() + "\n"
                for track in album.get_track_list()
            )
            for album in self.controller.album_manager.load_all_albums()
            ],
        0  
    )



if __name__ == "__main__":
    root = tk.Tk()
    app = MusicManagementApp(root, title="Music Management" )
    
    def on_close():
        try:
            app.db_handler.close()
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()