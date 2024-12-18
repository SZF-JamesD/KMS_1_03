from file_operations import FileOperations

class Person:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self._id = None

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError("First name cannot be empty")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value:
            raise ValueError("Last name cannot be empty")
        self._last_name = value
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not value:
            raise ValueError("ID cannot be None")
        self._id = value

    def __str__(self):
        return f"{self.id}: {self.first_name} {self.last_name}"
    
    def to_dict(self):
        return{
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name
        }
    

class Customer(Person):
    def __init__(self, first_name, last_name, id=None):
        super().__init__(first_name, last_name)
        self.id = id or FileOperations.get_next_id("C")


class Employee(Person):
    def __init__(self, first_name, last_name, position, id=None):
        super().__init__(first_name, last_name)
        self.id = id or FileOperations.get_next_id("E")
        self._position = position

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        if not value:
            raise ValueError("Position cannot be empty.")
        self._position = value

    def __str__(self):
        return f"{super().__str__()}, Position: {self.position}"
    
    def to_dict(self):
        return{
            **super().to_dict(),
            "position": self.position
        }