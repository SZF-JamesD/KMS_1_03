from customer import Customer
from tkinter_utils import MessageBoxHandler
from validation_utils import is_valid_address, is_valid_name

class CustomerManagement:
    def __init__(self, db_handler, account_manager):
        self.db_handler = db_handler
        self.customers = []
        self.account_manager = account_manager
        self.load_customers_from_db()

    def load_customers_from_db(self): 
        main_query = "SELECT * FROM Customers"
        sub_query = "SELECT * FROM Accounts WHERE customer_id = %s"

        customer_data = self.db_handler.fetch_data_with_subquery(
            main_query=main_query,
            sub_query=sub_query,
            sub_query_param_key="customer_id"
        )
        
        for item in customer_data:
            customer = Customer.from_dict(item)
            self.customers.append(customer)
        self.db_handler.connection.commit()
        print("Customers loaded successfully.")
        
    def save_customer_to_db(self):
        main_query = """INSERT INTO Customers (customer_id, name, address) VALUES (%s, %s, %s)"""
        check_query = "SELECT COUNT(*) FROM Customers WHERE customer_id = %s"
        update_query = "UPDATE Customers SET name = %s, address = %s WHERE customer_id = %s"
        
        data = []
        for customer in self.get_customers():
            data.append({
                "customer_id": customer.customer_id,
                "name": customer.name,
                "address": customer.address
            })
        fetch_all_params = [(customer['customer_id'],) for customer in data]
        self.db_handler.save_data(main_query, check_query, update_query, data=data, fetch_all_params=[fetch_all_params[i] for i in range(len(data))])

    def create_customer(self, customer_info):
        first_name = customer_info.get("first_name")
        last_name = customer_info.get("last_name")
        address = customer_info.get("address")
        customer_id = self._generate_customer_id()
        name = first_name + " " + last_name
        if not is_valid_name(name) or not is_valid_address(address):
            return
        try:
            new_customer = Customer(name, address, customer_id)
            self.customers.append(new_customer)
            MessageBoxHandler.show_info("Success", f"Customer: {name} created.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error creating customer: {e}")

    def _generate_customer_id(self):
        return str(len(self.customers) + 1).zfill(4)

    def get_customers(self):
        return self.customers
        
    def get_customer_by_id(self, customer_id):
        return next((customer for customer in self.customers if customer.get_customer_id() == customer_id), None)

    def delete_customer(self, customer_info):
        customer_id = customer_info.get("id")
        try:
            customer = self.get_customer_by_id(customer_id)
            if customer:
                self.customers.remove(customer)
                MessageBoxHandler.show_info("Success", f"Customer deleted.")
            else:
                raise Exception(f"Customer ID: '{customer_id}' not found.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error removing customer: {e}")
        
    def assign_account(self, account):
        customer = self.get_customer_by_id(account.get_customer_id())
        customer.add_account(account)