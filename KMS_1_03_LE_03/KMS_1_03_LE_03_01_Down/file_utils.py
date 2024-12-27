import csv, json, random, vehicle_class

def read_csv_data(file_path):
    months = []
    gasoline = []
    diesel = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            months.append(row['Month'])
            try:
                gasoline.append(float(row['Gasoline (Liters)']))
                diesel.append(float(row['Diesel (Liters)']))
            except ValueError:
                continue
    
    return months, gasoline, diesel


def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            content = json.load(file)
            return  content
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return []
    

def write_json(file_path, data):
    existing_data = {item.__dict__ for item in data.items()}
    try:
        with open(file_path, "w") as file:
                json.dump(existing_data, file, indent=4)   
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return



def generate_vehicle_data(num_vehicles):
    vehicles = []
    for _ in range(num_vehicles):
        vehicle_type = random.choice(["Car", "Truck", "Motorcycle", "Bicycle"])
        registration_no = f"{vehicle_type[:3].upper()}{random.randint(100, 999)}"
        brand = random.choice(["Toyota", "Ford", "Volvo", "Honda", "BMW", "Giant", "Harley-Davidson", "Specialized"])
        mileage = random.randint(500, 100000)
        status = random.choice(["active", "maintenance", "retired"])
        fuel_capacity = random.randint(10, 200) if vehicle_type != "Bicycle" else 0
        current_fuel_level = random.randint(0, fuel_capacity) if fuel_capacity > 0 else 0

        if vehicle_type == "Car":
            vehicle = {
                "type": "Car",
                "registration_no": registration_no,
                "brand": brand,
                "mileage": mileage,
                "status": status,
                "fuel_capacity": fuel_capacity,
                "current_fuel_level": current_fuel_level,
                "no_seats": random.randint(2, 7),
                "trunk_capacity": random.randint(200, 800)
            }
        elif vehicle_type == "Truck":
            vehicle = {
                "type": "Truck",
                "registration_no": registration_no,
                "brand": brand,
                "mileage": mileage,
                "status": status,
                "fuel_capacity": fuel_capacity,
                "current_fuel_level": current_fuel_level,
                "no_axles": random.randint(2, 8),
                "cargo_capacity": random.randint(5000, 20000)
            }
        elif vehicle_type == "Motorcycle":
            vehicle = {
                "type": "Motorcycle",
                "registration_no": registration_no,
                "brand": brand,
                "mileage": mileage,
                "status": status,
                "fuel_capacity": fuel_capacity,
                "current_fuel_level": current_fuel_level,
                "engine_displacement": random.randint(100, 2000),
                "sidecar": random.choice([True, False])
            }
        elif vehicle_type == "Bicycle":
            vehicle = {
                "type": "Bicycle",
                "registration_no": registration_no,
                "brand": brand,
                "mileage": mileage,
                "status": status,
                "fuel_capacity": 0,
                "current_fuel_level": 0,
                "bike_type": random.choice(["Mountain", "Road", "Hybrid"]),
                "basket": random.choice([True, False])
            }
        vehicles.append(vehicle)
    return vehicles

if __name__ == "__main__":
    d = (read_json("company_vehicles.json"))
    print(d)
    for items in d:
       print(items)
    '''
    vehicles_data = generate_vehicle_data(100)


    with open("company_vehicles.json", "w") as file:
        json.dump(vehicles_data, file, indent=4)

    print("File 'company_vehicles.json' has been created.")
''' 