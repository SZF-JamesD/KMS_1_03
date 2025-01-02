
class Comitee:
    def __init__(self, members):
        self.members = members

    def add_member(self, name):
        self.members.append(name)

    def list_members(self):
        return [member.get_info() for member in self.members]