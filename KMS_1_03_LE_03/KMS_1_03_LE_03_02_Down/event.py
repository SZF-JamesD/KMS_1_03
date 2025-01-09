from datetime import datetime

class Event:
    def __init__(self, event_name, location, date_time: datetime, description):
        self.event_name = event_name
        self.date_time = date_time
        self.location = location
        self.description = description
        self.attendees = []
        self.events = []

    def add_event(self, event_name):
        self.events.append(event_name)

    def add_participant(self, person_name):
        self.attendees.append(person_name)
        print(f"{person_name} registered for {self.event_name}.")

    def remove_participant(self, person_name):
        if person_name in self.attendees:
            self.attendees.remove(person_name)
            print(f"{person_name} removed from list for {self.event_name}.")
        else:
            print(f"{person_name} not registered for {self.event_name}")

    def list_participants(self):
        return self.attendees
    
    def get_event_details(self):
        return self.description
    