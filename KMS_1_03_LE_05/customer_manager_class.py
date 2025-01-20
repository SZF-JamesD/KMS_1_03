from tkinter_utils import MessageBoxHandler
from validation_utils import is_valid_name, is_valid_phone_number, is_valid_email_address

class CustomerManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def validate_customer(self, customer_data):
        for key, value in customer_data.items():
            if key == "customer_name":
                if not is_valid_name(value):
                    print("invalid name")
                    return False
            elif key == "telephone_number":
                if not is_valid_phone_number(value):
                    print("invalid phone")
                    return False
            elif key == "email":
                if not is_valid_email_address(value):
                    print("invalid email")
                    return False
        return True

    def add_customer(self, customer_data):
        for value in customer_data.values():
            if value == None:
                MessageBoxHandler.show_error("Error", "Please enter all customer info.")
                return
            
        full_name = customer_data["first_name"] + " " + customer_data["last_name"]
        customer_data.pop("first_name")
        customer_data.pop("last_name")
        customer_data = {"customer_name": full_name, **customer_data}

        if not self.validate_customer(customer_data):
            print("Not valid")
            return

        main_value = ", ".join(f"{data}" for data in customer_data.keys())
        update_value = (customer_data["telephone_number"], customer_data["email"], customer_data["payment_choice"], customer_data["customer_name"])
        check_query = "SELECT COUNT(*) FROM customer_info WHERE customer_name = %s"
        update_query = "UPDATE customer_info SET telephone_number = %s, email = %s, payment_choice = %s WHERE customer_name = %s" 
        main_query = "INSERT INTO customer_info (" + main_value + ") VALUES (%s, %s, %s,%s)"

        self.db_handler.save_data(
            main_query=main_query,
            check_query=check_query,
            update_query=update_query,
            update_params=[update_value],
            data=[customer_data],
            fetch_all_params=[(value,) for key, value in customer_data.items() if key == "customer_name"]
        )

    def delete_customer(self, customer_data):
        for key, value in customer_data.items():
            if key == "first_name":
                if value == None:
                    MessageBoxHandler.show_error("Error", "Please enter first name info.")
                    return
            elif key == "last_name":
                if value == None:
                    MessageBoxHandler.show_error("Error", "Please enter last name info.")
                    return
                
        full_name = customer_data["first_name"] + " " + customer_data["last_name"]
        customer_data.pop("first_name")
        customer_data.pop("last_name")
        customer_data = {"customer_name": full_name, **customer_data}

        if not self.validate_customer(customer_data):
            return


        query = "SELECT customer_id FROM customer_info WHERE customer_name = %s"
        params = (customer_data["customer_name"],)
        id_info = self.db_handler.fetch_one(query, params)

        if id_info:
            customer_id = id_info["customer_id"]
            self.db_handler.delete_with_dependencies(
                main_table="customer_info",
                main_key="customer_id",
                value=customer_id
        )
        