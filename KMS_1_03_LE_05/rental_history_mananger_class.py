from datetime import datetime
from tkinter_utils import MessageBoxHandler
from validation_utils import is_valid_date
class RentalHistoryManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def add_rental(self, rental_data):
        for key, value in rental_data.items():
            if value == None and key != "rental_end":
                MessageBoxHandler.show_error("Error", "Please enter all rental info.")
                return
            elif key == "rental_start":
                if not is_valid_date(value):
                    print("date nto valid")
                    return
            elif key == "rental_end":
                if value == None:
                    value == 0
                
        cust_name = (rental_data["first_name"]+ " " + rental_data["last_name"],)
        reg_no = (rental_data["reg_no"],)

        query = "SELECT customer_id FROM customer_info WHERE customer_name = %s"
        params = cust_name
        cust_id_info = self.db_handler.fetch_one(query, params)

        query = "SELECT vehicle_id FROM vehicle_info WHERE reg_no = %s"
        params = reg_no
        vehicle_id_info = self.db_handler.fetch_one(query, params)
  
        if cust_id_info and vehicle_id_info:
            customer_id = cust_id_info["customer_id"]
            vehicle_id = vehicle_id_info["vehicle_id"]
            rental_data.pop("first_name")
            rental_data.pop("last_name")
            rental_data.pop("reg_no")
            rental_data = {"vehicle_id": vehicle_id, "customer_id": customer_id, **rental_data}


            main_value = ", ".join(f"{data}" for data in rental_data.keys())
            update_value = (rental_data["rental_end"], rental_data["vehicle_id"], rental_data["customer_id"])
            check_query = "SELECT COUNT(*) FROM rental_history WHERE vehicle_id = %s AND customer_id = %s"
            update_query = "UPDATE rental_history SET rental_end = % WHERE vehicle_id = %s and customer_id = %s"
            main_query = "INSERT INTO rental_history (" + main_value + ") VALUES (%s, %s, %s,%s)"

            self.db_handler.save_data(
                main_query=main_query,
                check_query=check_query,
                update_query=update_query,
                update_params=[update_value],
                data=[rental_data],
                fetch_all_params=[(str(rental_data["vehicle_id"]),str(rental_data["customer_id"])),]
            )
    

    def delete_rental(self, rental_data):
        for key, value in rental_data.items():
            if value == None and key != "rental_end":
                MessageBoxHandler.show_error("Error", "Please enter all rental info.")
                return
            elif key == "rental_start":
                if not is_valid_date(value):
                    return
            elif key == "rental_end":
                if value == None:
                    value == 0
                
        cust_name = rental_data["first_name"]+ " " + rental_data["last_name"]
        reg_no = (rental_data["reg_no"],)

        query = "SELECT customer_id FROM customer_info WHERE customer_name = %s"
        params = (cust_name,)
        cust_id_info = self.db_handler.fetch_one(query, params)

        query = "SELECT vehicle_id FROM vehicle_info WHERE reg_no = %s"
        params = reg_no
        vehicle_id_info = self.db_handler.fetch_one(query, params)

        if cust_id_info and vehicle_id_info:
            customer_id = cust_id_info["customer_id"]
            vehicle_id = vehicle_id_info["vehicle_id"]
            rental_data.pop("first_name")
            rental_data.pop("last_name")
            rental_data.pop("reg_no")
            rental_data = {"vehicle_id": vehicle_id, "customer_id": customer_id, **rental_data}

            query = "SELECT rental_id FROM rental_history WHERE vehicle_id = %s and customer_id = %s"
            params = (vehicle_id, customer_id)
            rental_id_info = self.db_handler.fetch_one(query, params)

            if rental_id_info:
                rental_id = rental_id_info["rental_id"]
                self.db_handler.delete_with_dependencies(
                    main_table="rental_history",
                    main_key="rental_id",
                    value=rental_id
            )
            