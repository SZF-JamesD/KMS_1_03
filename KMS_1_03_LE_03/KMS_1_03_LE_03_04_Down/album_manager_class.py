from album_class import Album
from track_class import Track
from tkinter_utils import MessageBoxHandler

class AlbumManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def load_album(self, album_title):
        #Load a specific album by its title.
        album_data = self.db_handler.fetch_one("albums", f"WHERE album_title = '{album_title}'")
        if album_data:
            album = Album.from_dict(album_data[0])
            album.track_list = self.load_tracks_for_album(album.album_title)  # Load tracks associated with this album
            return album
        return None
    

    def load_tracks_for_album(self, album_title):
            #Load all tracks for a specific album by its title.
            track_data_list = self.db_handler.fetch_all("tracks", f"WHERE album_title = '{album_title}'")
            return [Track.from_dict(track_data) for track_data in track_data_list]
    

    def load_all_albums(self):
        # Define the main query to fetch all albums
        main_query = "SELECT * FROM albums"
        
        # Define the subquery to fetch tracks for each album
        sub_query = "SELECT track_title, mp3_file, duration, album_title  FROM tracks WHERE album_title = %s"
        
        # Fetch albums with their related tracks
        album_data = self.db_handler.fetch_data_with_subquery(main_query, sub_query, sub_query_param_key='album_title')
        
        # Convert the result to Album objects
        albums = []
        for album in album_data:
            album_obj = Album.from_dict(album)
            for track_data in album['related_data']:
                track_obj = Track.from_dict(track_data)
                if track_obj not in album_obj.get_track_list():
                    album_obj.add_track(track_obj)
            albums.append(album_obj)

        return albums
    
    

    def save_album(self, album):
        #Save an album and its associated tracks to the database.
        for item in album:
            if item == None:
                MessageBoxHandler.show_error("Please enter album info.")
                return

        
        check_query = "SELECT COUNT(*) FROM albums WHERE album_title = %s"
        update_query = "UPDATE albums SET artist = %s, WHERE album_title = %s"
        insert_query = "INSERT INTO albums (album_title, artist) VALUES (%s, %s)"
        # For track data
        if "track_list" in album:
            track_data = [track.to_dict() for track in album.track_list if track]

            sub_check_query = "SELECT COUNT(*) FROM tracks WHERE track_title = %s AND album_title = %s"
            sub_update_query = "UPDATE tracks SET mp3_file = %s, duration = %s WHERE track_title = %s AND album_title = %s"
            sub_insert_query = "INSERT INTO tracks (track_title, mp3_file, duration, album_title) VALUES (%s, %s, %s, %s)"
        
        # Save both album and tracks using the save_data method
        self.db_handler.save_data(
            main_query=insert_query,
            check_query=check_query,
            update_query=update_query,
            sub_query=sub_insert_query if "track_list" in album else None,
            sub_check_query=sub_check_query if "track_list" in album else None,
            sub_update_query=sub_update_query if "track_list" in album else None,
            sub_query_update_params=[(track["mp3_file"], track["duration"], track["title"], track["album_title"]) for track in track_data if track] if "track_list" in album else None,
            update_params=[(album["artist"], album["album_title"])],
            data=[album],
            fetch_all_params=[(album["album_title"],)]
        )



    def delete_album(self, album_data):
        album_title = album_data["album_title"]
        self.db_handler.delete_with_dependencies(
            main_table="albums",
            dependent_table="tracks",
            main_key="album_title",
            dependent_key="album_title",
            value=album_title
        )


    def update_album(self, album_data):
        #Update an existing album in the database.
        self.save_album(album_data)
    
    def save_track(self, track_data):
        #Save track for a specific album.
        check_query = "SELECT COUNT(*) FROM tracks WHERE track_title = %s AND album_title = %s"
        update_query = "UPDATE tracks SET mp3_file = %s, duration = %s WHERE track_title = %s AND album_title = %s"
        insert_query = "INSERT INTO tracks (album_title,track_title, duration, mp3_file) VALUES (%s, %s, %s, %s)"
        fetch_all_params=[(track_data["track_title"], track_data["dropdown_selection"],)]

        # Insert new track
        self.db_handler.save_data(
            main_query=insert_query,
            check_query=check_query,
            update_query=update_query,
            update_params=[(track_data["mp3_file"], track_data["duration"], track_data["track_title"], track_data["dropdown_selection"])],
            data=[track_data],
            fetch_all_params=fetch_all_params

        )
    
    
    def create_album(self, album_data):
        title = album_data["album_title"]
        artist = album_data["artist"]
        if title != None and artist != None:
            album = Album(title, artist)
            self.save_album(album)
        else:
            MessageBoxHandler.show_error("Please enter a title and artist.")

    
    def delete_track(self, track_data):
        track_title = track_data["title"]
        album_title = track_data["dropdown_selection"]
        # Query to fetch the track ID based on title and album title
        query = "SELECT id FROM tracks WHERE track_title = %s AND album_title = %s"
        params = (track_title, album_title)
        track_data = self.db_handler.fetch_one(query, params)
        
        if track_data:
            track_id = track_data["id"]  # Get the ID from the query result
            # Use the ID to delete the track
            self.db_handler.delete_with_dependencies(
                main_table="tracks",
                main_key="id",
                value=track_id
            )
            self.messagebox.show_info("Success", f"Track '{track_title}' deleted.")
        else:
            self.messagebox.show_error("Error", f"No track found with title '{track_title}' in album '{album_title}'.")

        
    

