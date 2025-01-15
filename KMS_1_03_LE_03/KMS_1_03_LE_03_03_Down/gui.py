from tkinter_utils import *
import tkinter as tk
from tkinter import ttk
from customer_management_class import CustomerManagement
from account_management_class import AccountManagement
from account import Account
from file_utils import DatabaseHandler
from transaction_manager import TransactionManager

class AccountManagementApp(NotebookBasedGui):
    def __init__(self, root, title="Account Management", geometry="800x600", resizable=(False, False)):
        super().__init__(root, title, geometry, resizable)
        
        self.db_handler = DatabaseHandler(host="localhost", user="root", password="", database="account_management")
        self.account_manager = AccountManagement(self.db_handler)
        self.customer_manager = CustomerManagement(self.db_handler, self.account_manager)
        self.transaction_manager = TransactionManager(self.customer_manager, self.account_manager)
        self.account = Account

        self.add_frames([
            CustomerManager,
            AccountManager,
            BalanceManager,
        ])


class CustomerManager(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.max_name_length = max((len(customer.get_name()) for customer in self.controller.customer_manager.get_customers()),default=0)

        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)

        self.tab1 = InnerNotebookTab(self.inner_notebook, "Add Customer",
            widgets=[
            (InputFields, {"field_list": [("First Name", "first_name"), ("Last Name", "last_name"), ("Address", "address")]}),
            ]
        )
        
        self.tab2 = InnerNotebookTab(self.inner_notebook, "Remove Customer",
            widgets=[
                (InputFields, {"field_list": [("ID", "id")]})
            ]
        )

        self.tab3 = InnerNotebookTab(self.inner_notebook, "View Customer Records",
            widgets=[   
                (ScrollableListbox, {"items": [f"ID: {str(customer.get_customer_id()).ljust(6)} Name: {customer.get_name().ljust(self.max_name_length+4)} Accounts: {[(account.get_account_number()) + " " + (str(account.get_balance())) + " " + (account.get_account_type()) for account  in customer.get_accounts()]}"for customer in self.controller.customer_manager.get_customers()],
                                    "scrollbar2": "horizontal",
                                    "scroll_side2": "bottom",
                                    })
            ])
        
        Buttons(2, (self.tab1.get_tab_frame(), self.tab2.get_tab_frame()),
                ("Add new Customer", "Remove Customer"),
                (lambda: self.controller.customer_manager.create_customer(self.tab1.get_field_values()),
                lambda:self.controller.customer_manager.delete_customer(self.tab2.get_field_values())),
                (tk.TOP,)*2, ("w",)*2, (5,)*2, (5,)*2
                )

        self.inner_notebook.bind(
            "<<NotebookTabChanged>>",
            lambda event: self.tab3.update_inner_tab(
            event,
            "View Customer Records", 
            [f"ID: {str(customer.get_customer_id()).ljust(6)} Name: {customer.get_name().ljust(self.max_name_length+4)} Accounts: {[(account.get_account_number())+  " " + (str(account.get_balance())) + " "  +(account.get_account_type()) for account in customer.get_accounts()]}"
                for customer in self.controller.customer_manager.get_customers()], 
            0  
            )
        )


class AccountManager(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.inner_notebook = ttk.Notebook(self)
        self.inner_notebook.pack(expand=True, fill=tk.BOTH)


        self.tab1 = InnerNotebookTab(self.inner_notebook, "Create Account",
            widgets=[
            (DropdownMenu, {"options":  ["Checking", "Savings"], "side": tk.TOP, "anchor": "w", "padx": 5, "pady": 5, "default": "Select Account Type"}),
            (InputFields, {"field_list": [("Customer ID", "customer_id")]}),                                  
            ]
        )
        
        self.tab2 = InnerNotebookTab(self.inner_notebook, "Delete Account",
            widgets=[
                (InputFields, {"field_list": [("Customer ID", "customer_id"), ("Account No,", "account_no")]})
            ]
        )
        
        Buttons(2,(self.tab1.get_tab_frame(), self.tab2.get_tab_frame()),
            ("Add new Account", "Delete an Account"),
            (lambda: self.controller.customer_manager.assign_account(self.controller.account_manager.create_account(self.tab1.get_field_values())),
            lambda: self.controller.customer_manager.delete_account(self.controller.account_manager.delete_account(self.tab2.get_field_values())),   
            ),(tk.TOP,)*2,("w",)*2,(5,)*2,(5,)*2,)

class BalanceManager(ttk.Frame):
    def __init__ (self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.transaction_label = ttk.Label(self, text="Deposit or Withdraw")
        self.transaction_label.pack(side=tk.TOP, anchor="w", padx=5, pady=5)

        inputs = InputFields(self, field_list= [("Customer ID", "customer_id"),("Account Number", "account_no"), ("Amount", "amount")])


        Buttons(2, (self, self),
                ("Deposit", "Withdraw"),
                (lambda: (self.controller.transaction_manager.perform_transaction(inputs.get_input_field_values(), "deposit")),
                lambda: (self.controller.transaction_manager.perform_transaction(inputs.get_input_field_values(), "withdraw"))),
                (tk.TOP,)*2, ("w",)*2, (5,)*2, (5,)*2
                )



if __name__ == "__main__":
    root = tk.Tk()
    app = AccountManagementApp(root, title="Account Management" )
    def on_close():
        try:
            app.customer_manager.save_customer_to_db()
            app.account_manager.save_account_to_db()
        except Exception as e:
            MessageBoxHandler.show_error("Error", f"Error saving to database: {e}")
        finally:
            app.db_handler.close()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()