from person import Member
from datetime import date

class Club:
    def __init__(self, name, founded_year: date):
        self.name = name
        self.founded_year = founded_year
        self.members = []
        self. events = []

    def add_member(self, member: Member):
        self.members.append(member)
        print(f"{member.name} added to {self.name}.")

    def remove_member(self, member: Member):
        self.members.remove(member)
        print(f"{member.name} removed from {self.name}")

    def list_members(self):
        for mem in self.members:
            print(mem)

    def __str__(self):
        return f"{self.name}\nFounded in {self.founded_year}\nCurrent members are {[member for member in self.members]}"

    