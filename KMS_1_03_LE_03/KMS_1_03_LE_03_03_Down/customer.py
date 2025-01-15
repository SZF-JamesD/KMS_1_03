class Customer:
    def __init__(self, name, address, customer_id):
        self.name = name
        self.address = address 
        self.customer_id = customer_id
        self.accounts = []

    def get_name(self):
        return self.name
    
    def get_address(self):
        return self.address
    
    def get_customer_id(self):
        return self.customer_id
    
    def get_accounts(self):
        return self.accounts
    
    def get_account_by_number(self, account_no):
        try:
            return next(account for account in self.accounts if account.get_account_number() == account_no)
        except StopIteration:
            return None
    
    def add_account(self, account):
        self.accounts.append(account)

    def remove_account(self, account_number):
        account = self.get_account_by_number(account_number)
        if account:
            self.accounts.remove(account)

            
    def to_dict(self):
        import json
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "accounts": json.dumps([account.to_dict() for account in self.accounts])}

    @classmethod
    def from_dict(cls, data):
        from account import Account
        accounts_data = data.get("related_data", [])
        accounts = [Account.from_dict(acc) for acc in accounts_data]
        customer = cls(
            name=data["name"],
            address=data["address"],
            customer_id=data["customer_id"]
        )
        customer.accounts = accounts
        return customer