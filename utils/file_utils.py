import csv, json, datetime

def read_csv_data(file_path):
    months = []
    gasoline = []
    diesel = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            months.append(row['Month'])
            try:
                gasoline.append(float(row['Gasoline']))
                diesel.append(float(row['Diesel']))
            except ValueError:
                continue
    
    return months, gasoline, diesel


def write_csv_data(file_path, fuel_type, fuel_amount):
    mon, gas, dies = read_csv_data(file_path)

    month = datetime.datetime.now().strftime("%b")
    month_index = 0

    for m in range(len(mon)):
        if mon[m] == month:
            month_index = m
            if fuel_type == "Gasoline":
                gas[month_index] += fuel_amount
            elif fuel_type == "Diesel":
                dies[month_index] += fuel_amount
    
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Month", "Gasoline", "Diesel"])
        writer.writeheader()
        for i in range(len(mon)):
            
            writer.writerow({"Month": mon[i], "Gasoline":gas[i], "Diesel": dies[i]})
  


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


if __name__ == "__main__":
    pass
 