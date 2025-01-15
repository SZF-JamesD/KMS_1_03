import csv, json, mysql.connector, customer, account
from faker import Faker

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)


    def execute_query(self, query, params=None):
        try:
            #print(f"Executing query: {query} with parameters: {params}")
            self.cursor.execute(query, params)
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_data_with_subquery(self, main_query, sub_query=None, sub_query_param_key=None):
        try:
            main_data = self.fetch_all(main_query)
            if sub_query and sub_query_param_key:
                for main_item in main_data:
                    param_value = main_item[sub_query_param_key]
                    sub_data = self.fetch_all(sub_query, (param_value,))
                    main_item['related_data'] = sub_data
            return main_data
        except Exception as e:
            print(f"Error fetching data with subquery: {e}")
            return []

    def save_data(self, main_query, check_query, update_query, sub_query=None, sub_check_query=None, sub_update_query=None, update_params=None, data=None, fetch_all_params = None):
        try:

            if self.connection.in_transaction:
                print("A transaction is already in progress, rolling back previous transaction.")
                self.connection.rollback()
            
            self.connection.start_transaction()

            for i, item in enumerate(data):               
                params = fetch_all_params[i]
                if self.fetch_all(check_query, params)[0]['COUNT(*)'] > 0:
                    main_params = update_params[i]
                    self.execute_query(update_query, main_params)
                else:
                    main_params = tuple(item.values())
                    self.execute_query(main_query, main_params)

                # Handle related data
                if sub_query and 'related_data' in item:
                    for related_item in item['related_data']:
                        sub_params = tuple(related_item.values())

                        # Check if the related record exists
                        if self.fetch_all(sub_check_query, (list(related_item.values())[0],))[0]['COUNT(*)'] > 0:
                            self.execute_query(sub_update_query, sub_params)
                        else:
                            self.execute_query(sub_query, sub_params)

            self.connection.commit()
            print(f"Saved successfully")
        except Exception as e:
            print(f"Error saving data: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()




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
                with open(file_path, mode="w", newline="") as file:
                    print("No objects to write. Creating an empty CSV file.")
                    fieldnames = []
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    return

        fieldnames = objects[0].keys() 

        with open(file_path, mode="w", newline="") as file:
            #print("wow")
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            #print("We got this far")
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


def test_customer_csv(file_path, amount_of_lines):
    fake = Faker()
    person_list = [] 
    for i in range(amount_of_lines):
        p = customer.Customer(i, fake.name(), fake.address())
        p.accounts = [fake.random_lowercase_letter()]
        p.to_dict()
        person_list.append(p)
    print(person_list)
    write_csv(file_path, person_list)
    
def test_account_csv(file_path, amount_of_lines):
    fake = Faker()
    event_list = []
    for i in range(amount_of_lines):
        e = account.Account(fake.random_int(min=1, max=20), fake.random_element(elements=["Savings", "Checking"])).to_dict()
        event_list.append(e)
    write_csv(file_path, event_list)

if __name__ == "__main__":
    test_customer_csv("KMS_1_03_LE_03/KMS_1_03_LE_03_03_Down/customers.csv", 15)
    test_account_csv("KMS_1_03_LE_03/KMS_1_03_LE_03_03_Down/accounts.csv", 15)