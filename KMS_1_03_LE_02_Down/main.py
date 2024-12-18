from person_class import Employee, Customer
from course import Course
from file_operations import FileOperations

def main():
    while True:
        print("\n--- Main Menu ---\n1. Add a new customer\n2. Add a new employee\n3. View all people\n4. Filter people\n5. Create a new course\n6. View all courses\n7. Add participant to a course\n8. Exit")

        choice = input("Enter selection: ")

        match(choice):
            case "1": #new customer
                print("\nEnter new Customer details:")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                customer = Customer(first_name, last_name)
                FileOperations.write_person(customer)

            case "2": #new employee
                print("\nEnter new Employee details:")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                position = input("Enter the employee position: ")
                employee = Employee(first_name, last_name, position)
                FileOperations.write_person(employee)

            case "3": # view all
                print("\nAll People in the system:")
                all_people = FileOperations.read_all_people()
                for person in all_people:
                    print(person)

            case "4": # filter
                print("\nFiltered People:")
                while True:
                    choice = input("Please enter (E)mployee or (C)ustomer: ")
                    if choice.upper() != "E" and choice.upper() != "C":
                        print("Please enter either E or C.")
                    else:
                        FileOperations.filter_by_type(choice.upper())
                        FileOperations.read_filtered_file()
                        break


            case "5": #new course
                course_name = input("Enter course name: ")
                description = input("Enter course description: ")
                employee_id = input("Enter the employee ID in charge of this course: ")
                course = Course(course_name, description, employee_id)
                FileOperations.write_course(course)

            case "6": #all courses
                print("\nAll Courses:")
                courses = FileOperations.read_all_courses()
                for course in courses:
                    print(course)

            case "7": #add participant
                print("\nSelect a course to add a participant:")
                courses = FileOperations.read_all_courses()
                for i, course in enumerate(courses, 1):
                    print(f"{i}. {course.course_name}")

                course_choice = int(input("Enter course number: ")) -1
                if 0 <= course_choice <len(courses):
                    course = courses[course_choice]
                    print(f"Adding participant to {course.course_name}")
                    person_id = input("Enter person ID: ")

                    all_people = FileOperations.read_all_people()
                    participant = None
                    for p in all_people:
                        if p.id == person_id:
                            participant = p
                            break
                    
                    if participant:
                        course.add_participant(participant)
                        FileOperations.write_course(course)
                    else:
                        print("Person not found.")
                else:
                    print("Invalid choice")
            
            case "8":
                print("Exiting")
                break
            case _:
                print("Invalid selection, please try again.")



if __name__ == "__main__":
    FileOperations.initialize_file()
    main()


