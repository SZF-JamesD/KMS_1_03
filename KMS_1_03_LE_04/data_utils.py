import csv, json, mysql.connector
from mysql.connector import Error
from faker import Faker
from tkinter_utils import MessageBoxHandler

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.messagebox = MessageBoxHandler()
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.connection.autocommit = False
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to the database.")
        except Error as e:
            self.messagebox.show_error("Database Connection Error", f"Error connecting to the database: {e}")
            raise
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during initialization: {e}")
            raise

    def execute_query(self, query, params=None):
        #Execute a query with optional parameters.
        try:
            self.cursor.execute(query, params)
            
        except Error as e:
            self.messagebox.show_error("This Query Execution Error", f"Error executing query: {e}")
            self.connection.rollback()
            raise
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during query execution: {e}")
            self.connection.rollback()
            raise

    def fetch_all(self, query, params=None):
        #Fetch all rows for a query.
        try:      
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            self.messagebox.show_error("Data Fetch Error", f"Error fetching data: {e}")
            return []
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during data fetch: {e}")
            return []

    def fetch_one(self, query, params=None):
        #Fetch a single row for a query.
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as e:
            self.messagebox.show_error("Single Data Fetch Error", f"Error fetching single row: {e}")
            return None
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during single fetch: {e}")
            return None

    def fetch_data_with_subquery(self, main_query, sub_query=None, sub_query_param_key=None):
        try:
            # Fetch the main data
            main_data = self.fetch_all(main_query)
            
            # If subquery and subquery_param_key are provided, fetch related data for each main item
            if sub_query and sub_query_param_key:
                # Create a mapping of main item parameters to related tracks
                related_data_mapping = {}
                for main_item in main_data:
                    param_value = main_item[sub_query_param_key]
                    if param_value not in related_data_mapping:
                        # Fetch related tracks for each unique parameter only once
                        sub_data = self.fetch_all(sub_query, (param_value,))
                        related_data_mapping[param_value] = sub_data
                
                # Add related tracks to each main item from the mapping
                for main_item in main_data:
                    param_value = main_item[sub_query_param_key]
                    main_item['related_data'] = related_data_mapping.get(param_value, [])
            
            return main_data
        except Error as e:
            self.messagebox.show_error("Fetch Data With Subquery Error", f"Error fetching data with subquery: {e}")
            return []
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during subquery fetch: {e}")
            return []

    def delete_with_dependencies(self, main_table,  main_key, value, dependent_table=None, dependent_key=None):
        """
        Delete a record from the main table along with its related records in a dependent table.
        
        Args:
            main_table (str): The name of the main table.
            dependent_table (str): The name of the dependent table.
            main_key (str): The column name in the main table to match the value.
            dependent_key (str): The column name in the dependent table to match the value.
            value (str): The value to match for deletion.
        """
        try:
            # Start a transaction
            if self.connection.in_transaction:
                print("Rolling back previous transaction before starting a new one.")
                self.connection.rollback()
            self.connection.start_transaction()
            
            # Delete records from the dependent table 
            if dependent_key and dependent_table:
                self.execute_query(f"DELETE FROM {dependent_table} WHERE {dependent_key} = %s", (value,))
            
            # Delete record from the main table
            self.execute_query(f"DELETE FROM {main_table} WHERE {main_key} = %s", (value,))
            
            # Commit the transaction
            self.connection.commit()
            self.messagebox.show_info("Success", f"Records related to {value} have been successfully deleted.")
        except Error as e:
            self.connection.rollback()
            self.messagebox.show_error("Deletion Error", f"An error occured during deletaion: {e}")
        except Exception as e:
            # Rollback changes on error
            self.connection.rollback()
            self.messagebox.show_error("Deletion Error", f"An error occurred during deletion: {e}")



    def save_data(self, main_query, check_query, update_query, sub_query=None, sub_check_query=None, sub_update_query=None, sub_query_update_params=None, update_params=None, data=None, fetch_all_params=None):
        #Save or update main and related data.
        try:
            if self.connection.in_transaction:
                print("A transaction is already in progress, rolling back previous transaction.")
                self.connection.rollback()
            
            self.connection.start_transaction()

            for i, item in enumerate(data):
                # Handling the check for existing records (whether to update or insert)
                params = fetch_all_params[i]

                if self.fetch_all(check_query, params)[0]['COUNT(*)'] > 0:
                    # Update existing record
                    main_params = update_params[i]
                    self.execute_query(update_query, main_params)
                else:
                    # Insert new record
                    main_params = tuple(item.values())
                    self.execute_query(main_query, main_params)

                # Handle related data (subqueries)
                if sub_query and 'related_data' in item:
                    for related_item in item['related_data']:
                       

                        # Check if related record exists
                        if self.fetch_all(sub_check_query, (list(related_item.values())[0],))[0]['COUNT(*)'] > 0:
                            self.execute_query(sub_update_query, sub_query_update_params)
                        else: 
                            sub_params = tuple(related_item.values())
                            self.execute_query(sub_query, sub_params)

            self.connection.commit()
            self.messagebox.show_info("Save Successful", "Data saved successfully.")
        except Error as e:
            self.messagebox.show_error("Save Data Error", f"Error saving data: {e}")
            self.connection.rollback()
        except Exception as e:
            self.messagebox.show_error("Save Data Error", f"Error saving data: {e}")
            self.connection.rollback()

    def close(self):
        #Close the connection.
        try:
            if self.connection:
                self.connection.close()
                print("Database connection closed.")
        except Error as e:
            self.messagebox.show_error("Connection Close Error", f"Error closing the database connection: {e}")
        except Exception as e:
            self.messagebox.show_error("Unexpected Error", f"An unexpected error occurred during connection close: {e}")




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

'''
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
    test_account_csv("KMS_1_03_LE_03/KMS_1_03_LE_03_03_Down/accounts.csv", 15)'''