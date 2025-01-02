from datetime import date

class Event:
    def __init__(self, event_name, date, location, time, description, attendees):
        self.event_name = event_name
        self.date = date
        self.location = location
        self.time = time
        self.description = description
        self.attendees = attendees
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
    