from person import Member, ComiteeMember
from datetime import date
from file_utils import write_csv, read_csv
from validation_utils import is_valid_name, is_valid_email_address
from tkinter_utils import MessageBoxHandler

class MemberManagement:
    def __init__(self, file_path):
        self.file_path = file_path
        self.members = []
        self.load_members()


    def get_members(self):
        return self.members
    
    def load_members(self):
        data = read_csv(self.file_path)
        for item in data:
            if item["Role"] == "Comitee Member":
                self.members.append(ComiteeMember.from_dict(item))
            else:
                self.members.append(Member.from_dict(item))
        print("Members loaded successfully.")    


    def save_to_csv(self):
        try:
            #print([member.to_dict() for member in self.members])
            #print([member for member in self.members])
            write_csv(self.file_path, [member.to_dict() for member in self.members])
            print("Members saved successfully.")
        except Exception as e:
            print(f"Error saving members: {e}")

    
    def add_member(self, member_data):
        first_name = member_data.get("first_name", "")
        last_name = member_data.get("last_name", "")
        member_id = int(self.members[-1].get_id()) +1 if len(self.members) != 0 else 1
        role = member_data.get("dropdown_selection", "")
        email = member_data.get("email", "")
        if not is_valid_name(first_name + " " + last_name):
            return 
        if not is_valid_email_address(email):
            return
        try:
            join_date = date.today()
            if role == "Comitee Member":
                new_member = ComiteeMember(member_id, first_name, last_name, email, join_date, role)
            else:
                new_member = Member(member_id, first_name, last_name, email, join_date, role)
            self.members.append(new_member)
            MessageBoxHandler.show_info("Success",f"{role} '{first_name} {last_name}' added successfully.")
        except Exception as e:
            MessageBoxHandler.show_error("Validation Error", str(e))


    def remove_member(self, id):
        id = id.get("id")
        try:
            if id in (member.get_id() for member in self.members):
                self.members = [member for member in self.members if member.get_id() != id]
                MessageBoxHandler.show_info("Success", f"Member with id {id} removed successfully.")
            else:
                raise Exception(f"Member with ID {id} not in register")
        except Exception as e:
            MessageBoxHandler.show_error("Error", e)


    def change_role(self, member_data):
        id = member_data.get("id")
        new_role = member_data.get("dropdown_selection")
        try:
            for i, member in enumerate(self.members):
                if member.get_id() == id:
                    first_name = member.get_first_name()
                    last_name = member.get_last_name()
                    email = member.get_email()
                    join_date = member.get_join_date()
                    
                    if new_role == "Comitee Member":
                        new_member = ComiteeMember(id, first_name, last_name, email, join_date, new_role)
                    elif new_role == "Member":
                        new_member = Member(id, first_name, last_name, email, join_date, new_role)
                    else:
                        print(f"Invalid role '{new_role}'.")
                        return
                    
                    self.members[i] = new_member
                    print(f"Role of {first_name} {last_name} changed to '{new_role}'.")
                    return
            raise Exception(f"Member with ID number {id} not in register.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", e)


    def pay_fees(self, member_data):
        id = member_data.get("id")
        try:
            for member in self.members:
                if member.get_id() == id:
                    member.pay_fees()
                    return
            raise ValueError(f"Member with ID number {id} not in register.")
        except Exception:
            MessageBoxHandler.show_error("Error", "Error processing payment.")
        except ValueError as e:
            MessageBoxHandler.show_error("Error", e)