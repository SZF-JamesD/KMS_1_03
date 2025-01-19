from validation_utils import is_valid_duration

class Track:
    def __init__(self, title, mp3_file, duration, album_title):
        self.title = title
        self.mp3_file = mp3_file
        self.duration = is_valid_duration(duration)
        self.album_title = album_title
        
    def get_title(self):
        return self.title
    
    def get_mp3_file(self):
        return self.mp3_file
    
    def get_duration(self):
        return self.duration
    
    def get_album_title(self):
        return self.album_title

    def to_dict(self):
        return {
            "track_title": self.title,
            "mp3_file": self.mp3_file,
            "duration": self.duration,
            "album_title": self.album_title
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["track_title"], data["mp3_file"], data["duration"], data["album_title"])

    def __str__(self):
        return f"{self.title} [{self.get_duration()}]"
    