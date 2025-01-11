from event import Event
from validation_utils import is_valid_address, is_valid_date
from tkinter_utils import MessageBoxHandler
from file_utils import write_csv, read_csv

class EventManagement:
    def __init__(self, file_path, member_manager):
        self.file_path = file_path
        self.member_manager = member_manager
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
        if not is_valid_address(location):
            return
        date, time = date_time.split(" ")
        if not is_valid_date(date):
            return
        try:
            new_event = Event(event_name, location, date_time, description)
            self.events.append(new_event)
            MessageBoxHandler.show_info("Success", f"{event_name} added successfully.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error adding member: {e}")


    def remove_event(self, event_data):
        event_name = event_data.get("event_name")
        try:
            if event_name in (event.get_event_name() for event in self.events):
                self.events = [event for event in self.events if event.get_event_name() != event_name]
                print(f"Event '{event_name}' removed successfully.")
                return
            raise Exception(f"Event '{event_name}' not registered.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error removing event: {e}")


    def edit_event(self, event_data):
        event_name = event_data.get("event_name", "")
        location = event_data.get("location", "")
        date_time = event_data.get("date_time", "")
        description = event_data.get("description", "")
        if not is_valid_address(location):
            return
        date, time = date_time.split(" ")
        if not is_valid_date(date):
            return
        try:
            for i, event in enumerate(self.events):
                if event.get_event_name() == event_name:
                    event_participatns = event.get_attendees()
                    new_event = Event(event_name, location, date_time, description)
                    new_event.attendees = event_participatns                  
                    self.events[i] = new_event
                    MessageBoxHandler.show_info("Success", f"{event_name} edited successfully")
                    return
            raise Exception(f"Event '{event_name}' not registered.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error editing event: {e}")


    def add_member_to_event(self, event_data):
        event_name = event_data.get("event_name", "")
        member_id = event_data.get("id", "")
        try:
            for event in self.events:
                if event.get_event_name() == event_name:
                    for member in self.member_manager.members:
                        print(member.get_id())
                        if member.get_id() == member_id:
                            member_name = member.get_first_name()
                            event.attendees.append(member_name)
                            MessageBoxHandler.show_info("Success", f"{member_name} added to {event_name}.")
                            return
                        elif member == self.member_manager.members[-1]:
                            raise Exception(f"Member ID number {member_id} not registered.")
                elif event == self.events[-1]:
                    raise Exception(f"Event '{event_name} not registered.")            
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error adding member to event: {e}")

    def remove_member_from_event(self, event_data, member_data):
        event_name = event_data.get("event_name", "")
        member_id = member_data.get("id", "")
        try:
            for event in self.events:
                if event.get_event_name() == event_name:
                    for member in self.member_manager.members:
                        if member.get_id() == member_id:
                            event.attendees.remove(member)
                            MessageBoxHandler.show_info("Success", f"{member.get_name()} removed from {event_name}.")
                        else:
                            raise Exception(f"Member ID number {member_id} not registered.")
                else:
                    raise Exception(f"Event '{event_name} not registered.")            
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error removing member from event: {e}")
