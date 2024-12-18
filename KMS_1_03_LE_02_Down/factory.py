class Factory:
    
    @staticmethod
    def create_person(person_data):
        from person_class import Customer, Employee
        if person_data['id'].startswith('C'):
            return Customer(person_data['first name'], person_data['last name'], id=person_data["id"])
        elif person_data['id'].startswith('E'):
            return Employee(person_data['first name'], person_data['last name'], person_data['position'], id=person_data["id"])
        return None
    
    @staticmethod
    def create_course(course_data):
        from person_class import Customer, Employee
        from course import Course
        if course_data:
            course = Course(course_name=course_data["course name"],
                            description=course_data["description"],
                            employee_id=course_data["employee ID"])
            
            participants = course_data.get("participants", [])
            for p in participants:
                participant = Factory.create_person(p)
                if participant:
                    course.add_participant(participant)
            return course
        return None