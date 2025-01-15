class Account:
    def __init__(self, account_number, account_type, balance, customer_id):
        self.account_number = account_number
        self.account_type = account_type
        self._balance = balance
        self.customer_id = customer_id


    def get_account_number(self):
        return self.account_number

    def get_account_type(self):
        return self.account_type

    def get_balance(self):
        return self._balance
    
    def set_balance(self, new_balance):
        self._balance = new_balance
    
    def get_customer_id(self):
        return self.customer_id

    def to_dict(self):
        return{
            "account_number": self.account_number,
            "account_type": self.account_type,
            "balance": self._balance,
            "customer_id": self.customer_id
        }
    
    @classmethod
    def from_dict(cls, data):
        account = cls(
            account_number=data.get("account_number"),
            account_type=data.get("account_type"),
            balance=data.get("balance"),
            customer_id=data.get("customer_id"))
        return account

        
