from event import Event
from datetime import date, datetime
from file_utils import write_csv, read_csv
from member_management_class import MemberManagement

class EventManagement:
    def __init__(self, file_path):
        self.file_path = file_path
        self.events = []
        self.load_events()

    def get_events(self):
        return self.events

    def load_events(self):
        data = read_csv(self.file_path)
        for item in data:
            self.events.append(Event.from_dict(item))
        print("Events loaded successfully.")    


    def save_to_csv(self):
        try:
            write_csv(self.file_path, [event.to_dict() for event in self.events])
            print("Events saved successfully.")
        except Exception as e:
            print(f"Error saving events: {e}")


    def add_event(self, event_data):
        event_name = event_data.get("event_name", "")
        location = event_data.get("location", "")
        date_time = event_data.get("date_time", "")
        description = event_data.get("dropdown_selection", "")
        try:
            new_event = Event(event_name, location, date_time, description)
            self.events.append(new_event)
            print(f"'{event_name}' added successfully.")
        except Exception as e:
            print(f"Error adding member: {e}")


    def remove_event(self, event_data):
        event_name = event_data.get("event_name")
        try:
            if event_name in (event.get_event_name() for event in self.events):
                self.events = [event for event in self.events if event.get_event_name() != event_name]
                print(f"Event '{event_name}' removed successfully.")
                print([event.get_event_name() for event in self.events])
                return
            print(f"Event '{event_name}' not registered.")
        except Exception as e:
            print(f"Error removing event: {e}")


    def edit_event(self, event_data):
        event_name = event_data.get("event_name", "")
        location = event_data.get("location", "")
        date_time = event_data.get("date_time", "")
        description = event_data.get("description", "")
        try:
            for i, event in enumerate(self.events):
                if event.get_event_name() == event_name:
                    event_participatns = event.get_attendees()
                    new_event = Event(event_name, location, date_time, description)
                    new_event.attendees = event_participatns                   
                    self.events[i] = new_event
                    print(f"{event_name} edited successfully")
                    return
            print(f"Event '{event_name}' not registered.")
        except Exception as e:
            print(f"Error editing event: {e}")


    def add_member_to_event(self, event_data, member_data):
        event_name = event_data.get("event_name", "")
        member_id = member_data.get("id", "")
        try:
            for event in self.events:
                if event.get_event_name() == event_name:
                    for member in MemberManagement.members:
                        if member.get_id() == member_id:
                            event.attendees.append(member)
                            print(f"{member.get_name()} added to {event_name}.")
                        else:
                            print(f"Member ID number {member_id} not registered.")
                else:
                    print(f"Event '{event_name} not registered.")            
        except Exception as e:
            print(f"Error adding member to event: {e}")

    def remove_member_from_event(self, event_data, member_data):
        event_name = event_data.get("event_name", "")
        member_id = member_data.get("id", "")
        try:
            for event in self.events:
                if event.get_event_name() == event_name:
                    for member in MemberManagement.members:
                        if member.get_id() == member_id:
                            event.attendees.remove(member)
                            print(f"{member.get_name()} removed from {event_name}.")
                        else:
                            print(f"Member ID number {member_id} not registered.")
                else:
                    print(f"Event '{event_name} not registered.")            
        except Exception as e:
            print(f"Error removing member from event: {e}")
