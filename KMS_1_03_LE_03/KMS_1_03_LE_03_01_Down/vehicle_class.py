from abc import ABC, abstractmethod

class Vehicle(ABC):
    total_vehicles = 0
    total_mileage = 0.0

    def __init__(self, registration_no, brand, mileage, status, fuel_capacity, current_fuel_level):
        self.registration_no = registration_no
        self.brand = brand
        self.mileage = mileage
        self.status = status
        self.fuel_capacity = fuel_capacity
        self.current_fuel_level = current_fuel_level
        Vehicle.total_vehicles += 1
        Vehicle.total_mileage += mileage

    @abstractmethod
    def update_mileage(self):
        pass

    @abstractmethod
    def maintenance(self):
        pass

    def refuel(self, amount):
        self.current_fuel_level = min(self.fuel_capacity, self.current_fuel_level + amount)

    def calculate_efficiency(self):
        return self.mileage / self.fuel_capacity

    @classmethod
    def get_total_vehicles(cls):
        return cls.total_vehicles

    @classmethod
    def get_total_mileage(cls):
        return cls.total_mileage
    
from vehicle import Vehicle

class Bicycle(Vehicle):
    def __init__(self, registration_no, brand, mileage, status, fuel_capacity, current_fuel_level, bike_type, basket):
        super().__init__(registration_no, brand, mileage, status, fuel_capacity, current_fuel_level)
        self.bike_type = bike_type
        self.basket = basket

    def update_mileage(self, new_mileage):
        self.mileage = new_mileage

    def maintenance(self):
        print(f"Bicycle {self.registration_no} is undergoing maintenance.")

from vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, registration_no, brand, mileage, status, fuel_capacity, current_fuel_level, no_seats, trunk_capacity):
        super().__init__(registration_no, brand, mileage, status, fuel_capacity, current_fuel_level)
        self.no_seats = no_seats
        self.trunk_capacity = trunk_capacity

    def update_mileage(self, new_mileage):
        self.mileage = new_mileage

    def maintenance(self):
        print(f"Car {self.registration_no} is undergoing maintenance.")

from vehicle import Vehicle

class Motorcycle(Vehicle):
    def __init__(self, registration_no, brand, mileage, status, fuel_capacity, current_fuel_level, engine_displacement, sidecar):
        super().__init__(registration_no, brand, mileage, status, fuel_capacity, current_fuel_level)
        self.engine_displacement = engine_displacement
        self.sidecar = sidecar

    def update_mileage(self, new_mileage):
        self.mileage = new_mileage

    def maintenance(self):
        print(f"Motorcycle {self.registration_no} is undergoing maintenance.")

from vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, registration_no, brand, mileage, status, fuel_capacity, current_fuel_level, no_axles, cargo_capacity):
        super().__init__(registration_no, brand, mileage, status, fuel_capacity, current_fuel_level)
        self.no_axles = no_axles
        self.cargo_capacity = cargo_capacity

    def update_mileage(self, new_mileage):
        self.mileage = new_mileage

    def maintenance(self):
        print(f"Truck {self.registration_no} is undergoing maintenance.")

    
class Driver:
    def __init__(self, name, license_no, assigned_vehicle):
        self.name = name
        self.license_no = license_no
        self.assigned_vehicle = assigned_vehicle


#class for other vehicle types? 
#ability to add new vehicles