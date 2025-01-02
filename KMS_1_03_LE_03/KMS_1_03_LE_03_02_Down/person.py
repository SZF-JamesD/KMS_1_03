from abc import ABC, abstractmethod
from datetime import date

class Person(ABC):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    
    @abstractmethod
    def get_role(self):
        pass


class Member(Person):
    def __init__(self, id, name, email, join_date: date, status):
        super().__init__(id, name, email)
        self.join_date = join_date
        self.status = status

    def pay_fees(self):
        print(f"{self.name} paid fees.")

    def get_role(self):
        return "Member"


class ComiteeMember(Person):
    def __init__(self, id, name, email, comitee_role):
        super().__init__(id, name, email)
        self.comitee_role = comitee_role

    def get_role(self):
        return f"Board Member - {self.comitee_role}."



class Volunteer(Person):
    def __init__(self, id: int, name: str, email: str, hours: int = 0):
        super().__init__(id, name, email)
        self.hours = hours

    def logHours(self, hours: int):
        self.hours += hours
        print(f"{self.name} logged {hours} hours. Total: {self.hours}")

    def getRole(self) -> str:
        return "Volunteer"