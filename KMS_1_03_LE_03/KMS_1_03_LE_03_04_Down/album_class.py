from track_class import Track

class Album:
    def __init__(self, album_title, artist): 
        self.album_title = album_title
        self.artist = artist
        self.track_list = []
        self.duration = self.total_duration() if len(self.track_list) >1 else "0"


    def add_track(self, track):
        self.track_list.append(track)

    def remove_track(self, track_title):
        self.track_list = [track for track in self.track_list if track.title != track_title]
        
    def total_duration(self):
        #Calculate the total duration of all tracks in the album.
        total_seconds = 0
        
        # Sum the durations of all tracks in seconds
        for track in self.track_list:
            
            total_seconds += self.convert_to_seconds(track.get_duration())

        # Convert total seconds back to hh:mm:ss or mm:ss format

        return self.convert_to_time_format(total_seconds)

    def convert_to_seconds(self, duration):
        #Convert a time string (hh:mm:ss or mm:ss) to total seconds.

        time_parts = duration.split(":")
        
        if len(time_parts) == 2:  # mm:ss format
            minutes, seconds = map(int, time_parts)
            return minutes * 60 + seconds
        elif len(time_parts) == 3:  # hh:mm:ss format
            hours, minutes, seconds = map(int, time_parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError("Invalid time format. Use mm:ss or hh:mm:ss.")

    def convert_to_time_format(self, total_seconds):
        #Convert total seconds back to hh:mm:ss or mm:ss format.
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"


    def get_album_title(self):
        return self.album_title
    
    def get_artist(self):
        return self.artist
    
    def get_track_list(self):
        return self.track_list

    def to_dict(self):
        return {
            "album_title": self.album_title,
            "artist": self.artist,
            "track_list": [track.to_dict() for track in self.track_list],
        }
    

    @classmethod
    def from_dict(cls, data):
        album = cls(data["album_title"], data["artist"])
        album.track_list = [Track.from_dict(track_dict) for track_dict in data["related_data"]]
        return album


    def __str__(self):
        return f"Album: {self.album_title}, Artist: {self.artist}, Total Duration: {self.duration}"
