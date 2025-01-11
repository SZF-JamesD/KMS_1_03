from datetime import datetime
import ast

class Event:
    def __init__(self, event_name, location, date_time: datetime, description):
        self.event_name = event_name
        self.date_time = date_time
        self.location = location
        self.description = description
        self.attendees = []

    def get_attendees(self):
        return self.attendees
    
    def get_event_name(self):
        return self.event_name
    
    def get_event_description(self):
        return self.description
    
    def get_event_location(self):
        return self.location
    
    def get_event_date_time(self):
        return self.date_time
    
    def to_dict(self):
        return {
            "Event Name": self.event_name,
            "Location": self.location,
            "Date and Time": self.date_time,
            "Description": self.description,  
            "Attendees": self.attendees  
        }

    @classmethod
    def from_dict(cls, data):
        event = cls(
            event_name=data["Event Name"],
            location=data["Location"],
            date_time=data["Date and Time"],
            description=data["Description"],)
        attendees = data.get("Attendees")
        attendees = attendees[1:-1]
        attendees = [item.strip().strip("'") for item in attendees.split(",")]
        
        #attendees = ast.literal_eval(data.get("Attendees"))
        
        if attendees[0] == '':
            attendees.pop(0)
        event.attendees = attendees    
        return event
        