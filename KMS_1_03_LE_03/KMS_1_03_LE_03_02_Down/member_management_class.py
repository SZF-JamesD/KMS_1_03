import person
from datetime import date
'''
1. Add member - for date, save it as default date object format, to display use strftime for %d.%m.%Y
2. Remove Member
3. Change member status
'''
class MemberManagement:
    def __init__(self):
        self.members = []
        
    def add_member(self, name, id, email, status):
        self.name = name
        self.id = id
        self.email = email
        self.join_date = date.today()
        self.status = status
        
        self.members.append(person.Member(self.id, self.name, self.email, self.join_date, self.status))
        return self.members

    def remove_member(self, name, id):
        self.name = name
        self.id = id

        self.members.remove(member for member in self.members if member.get_name() == self.name and member.get_id() == self.id)

    def change_status(self, name, id, new_status):
        self.name = name
        self.id = id
        self.new_status = new_status
        
        if self.new_status in ["Member", "Comitee Member", "Volunteer"]:
            for member in self.members:
                if member.get_name() == self.name and member.get_id == self.id:
                    member.status = new_status
                    return self.members
        return f"Something went wrong with the status selection, please try again."
        
