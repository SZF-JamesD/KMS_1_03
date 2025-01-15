from file_utils import write_csv, read_csv
from account import Account
from tkinter_utils import MessageBoxHandler

class AccountManagement:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.accounts = []
        self.load_accounts_from_db()

    def load_accounts_from_db(self):
        main_query = "SELECT * FROM Accounts"
        account_data = self.db_handler.fetch_all(main_query)
        for item in account_data:
            account = Account(
                account_number=item['account_number'],
                account_type=item['account_type'],
                balance=item['balance'],
                customer_id=item['customer_id']  # Customer ID is now part of account
            )
            self.accounts.append(account)
        self.db_handler.connection.commit()
        print("Accounts loaded successfully.")

    def save_account_to_db(self):
        main_query = """INSERT INTO Accounts (account_number, account_type, balance, customer_id) VALUES (%s, %s, %s, %s)"""
        check_query = "SELECT COUNT(*) FROM Accounts WHERE account_number = %s AND customer_id = %s"
        update_query = "UPDATE Accounts SET account_type = %s, balance = %s WHERE account_number = %s AND customer_id = %s"
        data = []
        for account in self.get_accounts():
            data.append(account.to_dict())
        update_param_data = [(account['account_type'], account['balance'], account['account_number'], account['customer_id']) for account in data] 
        fetch_all_params = [(account['account_number'], account['customer_id']) for account in data]
        self.db_handler.save_data(main_query, check_query, update_query,update_params=update_param_data, data=data, fetch_all_params=[fetch_all_params[i] for i in range(len(data))])

    def create_account(self, account_data):
        customer_id = account_data.get("customer_id")
        account_type = account_data.get("dropdown_selection")
        try:
            if account_type in ["Checking", "Savings"]:
                account_number = self._generate_account_number()
                new_account = Account(account_number, account_type, 0, customer_id)
                self.accounts.append(new_account)
                account_data["account_no"] = account_number
                MessageBoxHandler.show_info("Success", f"Account '{account_number}' created successfully.")
                return new_account
            else:
                raise Exception("Please select a valid account type.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"{e}")

    def _generate_account_number(self):
        return str(len(self.accounts) + 1).zfill(6)

    def get_an_account(self, account_number):
        return next((account for account in self.accounts if account.get_account_number() == account_number), None)

    def get_accounts(self):
        return self.accounts
    
    def delete_account(self, account_data):
        account_number = account_data.get("account_no")
        try:
            account = self.get_an_account(account_number)
            if account:
                self.accounts.remove(account)
                MessageBoxHandler.show_info("Success", f"Account '{account_number}' deleted.")
            else:
                raise Exception(f"Account number '{account_number}' not found.")
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error removing account: {e}")


        
