from tkinter_utils import MessageBoxHandler

class TransactionManager:
    def __init__(self, customer_manager, account_manager):
        self.customer_manager = customer_manager
        self.account_manager = account_manager

    def perform_transaction(self, transaction_data, transaction_type):
        try:
            customer_id = transaction_data.get("customer_id")
            account_no = transaction_data.get("account_no")
            amount = int(transaction_data.get("amount"))

            if transaction_type == "deposit":
                message = self.deposit(customer_id, account_no, amount)
            elif transaction_type == "withdraw":
                message = self.withdraw(customer_id, account_no, amount)
            else:
                raise ValueError("Invalid transaction type.")

            MessageBoxHandler.show_info("Success", message)
        except Exception as e:
            MessageBoxHandler.show_error("Error", str(e))

    def deposit(self, customer_id, account_no, amount):
        customer = self.customer_manager.get_customer_by_id(customer_id)
        account_obj = self.account_manager.get_an_account(account_no)
        if not customer:
            raise Exception(f"Customer with ID {customer_id} not found.")
        account = next((acc for acc in customer.get_accounts() if acc.get_account_number() == account_no), None)
        if not account:
            raise Exception(f"Account {account_no} not found.")

        if amount <= 0:
            raise Exception("Deposit amount must be greater than 0.")

        account._balance += amount
        account.set_balance(account._balance)
        account_obj.set_balance(account._balance)
        return f"Deposited €{amount}. New Balance: €{account.get_balance()}."

    def withdraw(self, customer_id, account_no, amount):
        customer = self.customer_manager.get_customer_by_id(customer_id)
        account_obj = self.account_manager.get_an_account(account_no)
        if not customer:
            raise Exception(f"Customer with ID {customer_id} not found.")

        account = next((acc for acc in customer.get_accounts() if acc.get_account_number() == account_no), None)
        if not account:
            raise Exception(f"Account {account_no} not found.")

        if amount <= 0 or amount > account.get_balance():
            raise Exception("Withdrawal amount must be greater than 0 and less than or equal to the current balance.")

        account._balance -= amount
        account.set_balance(account._balance)
        account_obj.set_balance(account._balance)
        return f"Withdrew €{amount}. New Balance: €{account.get_balance()}."

