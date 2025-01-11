from abc import ABC, abstractmethod
from datetime import date

class Person(ABC):
    def __init__(self, id, first_name, last_name, email, join_date: date, role):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.join_date = join_date
        self.role = role

    def pay_fees(self):
        print(f"{self.first_name} {self.last_name} paid fees.")

    def get_id(self):
        return self.id

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email
    
    def get_join_date(self):
        return self.join_date
    
    def get_role(self):
       return self.role

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass
        

class Member(Person):
    def __init__(self, id, first_name, last_name, email, join_date: date, role):
        super().__init__(id, first_name, last_name, email, join_date, role)
        self.join_date = join_date



    def to_dict(self):
        return {
            "ID": self.id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Email": self.email,  
            "Join Date": self.join_date,
            "Role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["ID"],
            first_name=data["First Name"],
            last_name=data["Last Name"],
            email=data["Email"],
            join_date=data["Join Date"],
            role=data["Role"]
        )


class ComiteeMember(Person):
    def __init__(self, id, first_name, last_name, email, join_date, role):
        super().__init__(id, first_name, last_name, email, join_date, role)
        

    def to_dict(self):
        """Include comitee_role for comitee members."""
        return {
            "ID": self.id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Email": self.email,
            "Join Date": self.join_date,
            "Role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        """Convert a dictionary to a ComiteeMember object."""
        return cls(
            id=data["ID"],
            first_name=data["First Name"],
            last_name=data["Last Name"],
            email=data["Email"],
            join_date=data["Join Date"],
            role=data["Role"]
        )