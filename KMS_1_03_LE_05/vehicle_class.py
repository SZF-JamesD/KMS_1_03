class Vehicle:
    def __init__(self, brand, model, reg_no, vehicle_status):
        self.brand = brand
        self.model = model
        self.reg_no = reg_no
        self.vehicle_status = vehicle_status

    def get_brand(self):
        return self.brand
    
    def get_model(self):
        return self.model
    
    def get_reg_no(self):
        return self.reg_no
    
    def get_vehicle_status(self):
        return self.vehicle_status
    
    def set_vehicle_status(self, new_status):
        self.vehicle_status = new_status

    
    def to_dict(self):
        return{
            "brand": self.brand,
            "model": self.model,
            "reg_no": self.reg_no,
            "vehicle_status": self.vehicle_status,
        }
    
    @classmethod
    def from_dict(cls, data):
        vehicle = cls(data["brand"],
                      data["model"],
                      data["reg_no"],
                      data["vehicle_status"])
        return vehicle
    
    def __str__(self):
        return f"Brand: {self.brand}. Model: {self.model}. Registration No.: {self.reg_no}. Status: {self.vehicle_status}"