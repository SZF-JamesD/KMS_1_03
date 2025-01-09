import csv, json, person
from faker import Faker

def read_csv(file_path):
    try:
        with open(file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


def write_csv(file_path, objects): # only really works if data is consistant
    try:
        if not objects:
            raise ValueError("No objects to write to CSV.")
        #print("objects",objects)
        fieldnames = objects[0].keys() 
        #print("fieldnames", fieldnames)
        with open(file_path, mode="w", newline="") as file:
            #print("wow")
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(obj for obj in objects)
            print(f"Data successfully written to {file_path}.")
            file.close()
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
  
'''
def write_csv(file_path, data, fieldnames): # can work with less consistant data, as you must provide the headings yourself.
    try:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {file_path}.")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
'''

def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            content = json.load(file)
            if not isinstance(content, list):
                print(f"Error: Expected a list in the JSON file, but got {type(content)}")
                return []
            return  content
    except FileNotFoundError:
        print(f"File not found: {file_path}. Returning an empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}. Returning an empty list.")
        return[]
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return []
    

def write_json(file_path, new_data):
    try:
        existing_data = read_json(file_path)

        if not isinstance(new_data, list) or not all(isinstance(item, dict) for item in new_data):
            raise ValueError("New data must be a list of dictionaries.")
        
        updated_data = existing_data + new_data

        with open(file_path, "w")as file:
            json.dump(updated_data, file, indent=4)

        print(f"Data successfully added to {file_path}.")
        
    except Exception as e:
        print(f"Error writing to JSON: {e}.")
        return


def test_csv(file_path, amount_of_lines):
    fake = Faker()
    person_list = [] 
    for i in range(amount_of_lines):
        p = person.Member(i, fake.first_name(), fake.last_name(), fake.email(), fake.date_this_decade(), "Member")
        person_list.append(p)
    write_csv(file_path, person_list)
    


if __name__ == "__main__":
    test_csv("KMS_1_03_LE_03\KMS_1_03_LE_03_02_Down\members.csv", 15)
 