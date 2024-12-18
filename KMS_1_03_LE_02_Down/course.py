class Course:
    def __init__(self, course_name, description, employee_id):
        self.course_name = course_name
        self.description = description
        self.participants = []
        self.employee_id = employee_id

    def add_participant(self, person):
        self.participants.append(person)
        print(f"Particiant {person.first_name} {person.last_name} added to course {self.course_name}.")

    def to_dict(self):
        return{
            "course name": self.course_name,
            "description": self.description,
            "employee ID": self.employee_id,
            "participants": [person.to_dict() for person in self.participants]
        }

    def __str__(self):
        participant_info = (f"\nParticipants:\n{'\n'.join([f'{p.first_name} {p.last_name}' for p in self.participants])}" if self.participants else f"\nNo participants\n")

        return f"Course: {self.course_name}\nDescription: {self.description}\nEmployee ID: {self.employee_id}{participant_info}"
