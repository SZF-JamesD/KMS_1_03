import json
from factory import *

class FileOperations:
    main_file = "KMS_1_03_LE_02_Down/people.json"
    filtered_file = "KMS_1_03_LE_02_Down/filtered.json"
    course_file = "KMS_1_03_LE_02_Down/courses.json"

    @classmethod
    def initialize_file(cls):
        try:
            with open(cls.main_file, "x") as file:
                json.dump([], file)
        except FileExistsError:
            pass 

        try:
            with open(cls.filtered_file, "x") as file:
                json.dump([], file)
        except FileExistsError:
            pass

        try:
            with open(cls.course_file, "x") as file:
                json.dump([], file)
        except FileExistsError:
            pass


    @classmethod
    def get_next_id(cls, prefix):
        highest_id = 0
        with open(cls.main_file, "r",) as file:
            content = json.load(file)
            if content:
                for person_data in content:
                    person_id = person_data.get("id")

                    if person_id and person_id.startswith(prefix):    
                        try:
                            current_id = int(person_id[1:])
                            if current_id > highest_id:
                                highest_id = current_id
                        except ValueError:
                            continue
        return f"{prefix}{highest_id + 1:03d}"
    
    @classmethod
    def write_person(cls, person_obj):
        person_data = person_obj.to_dict()
        try:
            with open(cls.main_file, "r") as file:
                content = json.load(file)
            

            for existing_person in content:
                if existing_person.get("id") == person_data["id"]:
                    print(f"Person already exists in records.")
                    return

            content.append(person_data)
            
            with open(cls.main_file, "w") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            print(f"Error writing person to file: {e}")

        
    @classmethod
    def read_all_people(cls):
        people = []
        try:
            with open(cls.main_file, "r") as file:
                content = json.load(file)          
            
            if content:
                for person_data in content:
                    person = Factory.create_person(person_data)
                    if person:
                        people.append(person)
            else:
                print(f"No data found in {cls.main_file}.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {cls.main_file}")
        return people

    
    @classmethod
    def filter_by_type(cls, person_type):
        filtered_people = []
        try:
            with open(cls.main_file, "r") as file:
                content = json.load(file)

            filtered_people = [person for person in content if person["id"][0] == person_type]

            with open(cls.filtered_file, "w") as file:
                json.dump(filtered_people, file, indent=4)

        except FileNotFoundError:
            print(f"File {cls.main_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {cls.main_file}")

    @classmethod
    def read_filtered_file(cls):
        try:
            with open(cls.filtered_file, "r") as file:
                content = json.load(file)
                print("Filtered Data from file:")
                for person in content:
                    print(person)
        except FileNotFoundError:
            print(f"File {cls.filtered_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {cls.filtered_file}")

    @classmethod
    def write_course(cls, course_obj):
        course_data = course_obj.to_dict()
        try: 
            with open(cls.course_file, "r") as file:
                content = json.load(file)
            

            updated = False
            for i, c in enumerate(content):
                if c['course name'] == course_obj.course_name:
                    content[i] = course_data
                    updated = True
                    break

            if not updated:
                content.append(course_data)

            with open(cls.course_file, "w") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            print(f"Error writing person to file: {e}")

    @classmethod
    def read_all_courses(cls):
        courses = []
        try:
            with open(cls.course_file, "r") as file:
                content = json.load(file)
                if content:
                    for course_data in content:
                        course = Factory.create_course(course_data)
                        if course:
                            courses.append(course)
                else:
                    print(f"No data found in {cls.course_file}.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {cls.course_file}")
        return courses

        
