from tkinter_utils import MessageBoxHandler

class VehicleManager:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def add_vehicle(self, vehicle_data):
        for  value in vehicle_data.values():
            if value == None:
                MessageBoxHandler.show_error("Error", "Please enter all vehicle info.")
                return
            
   
        main_value = ", ".join(f"{data}" for data in vehicle_data.keys())
        update_value = (vehicle_data["vehicle_status"], vehicle_data["reg_no"])
        check_query = "SELECT COUNT(*) FROM vehicle_info WHERE reg_no = %s"
        update_query = "UPDATE vehicle_info SET vehicle_status = %s WHERE reg_no = %s"
        main_query = "INSERT INTO vehicle_info (" + main_value + ") VALUES (%s, %s, %s,%s)"

        self.db_handler.save_data(
            main_query=main_query,
            check_query=check_query,
            update_query=update_query,
            update_params=[update_value],
            data=[vehicle_data],
            fetch_all_params=[(value, ) for key, value in vehicle_data.items() if key == "reg_no"]
        )

    def delete_vehicle(self, vehicle_data):
        reg_no = (vehicle_data["reg_no"],)
        print(reg_no)
        # Query to get vehicle_id from the reg_no
        query = "SELECT vehicle_id FROM vehicle_info WHERE reg_no = %s"
        params = reg_no
        id_info = self.db_handler.fetch_one(query, params)

        if id_info:
            vehicle_id = id_info["vehicle_id"]
            self.db_handler.delete_with_dependencies(
                main_table="vehicle_info",
                main_key="vehicle_id",
                value=vehicle_id
        )
