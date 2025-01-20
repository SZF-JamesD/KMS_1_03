class Customer:
    def __init__(self, first_name, last_name, telephone_number, email, payment_choice, rental_date):
        self.first_name = first_name
        self.last_name = last_name
        self.telephone_number = telephone_number
        self.email = email  
        self.payment_choice = payment_choice

    def get_name(self):
        return self.first_name+" "+self.last_name
    
    def get_telephone_number(self):
        return self.telephone_number
    
    def get_email(self):
        return self.email
    
    def get_payment_choice(self):
        return self.payment_choice
    
    
    
    
    def to_dict(self):
        return {
            "name": self.get_name(),
            "telephone_number": self.telephone_number,
            "email": self.email,
            "payment_choice": self.payment_choice
            
        }
    
    @classmethod
    def from_dict(cls, data):
        customer = cls(data["first_name"],
                   data["last_name"],
                   data["telephone_number"],
                   data["email"],
                   data["payment_choice"])
        return customer
    
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}. Phone Number: {self.telephone_number}. Email: {self.email}. Payment Method: {self.payment_choice}"