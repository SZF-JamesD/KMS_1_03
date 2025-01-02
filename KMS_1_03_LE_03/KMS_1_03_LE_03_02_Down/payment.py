from datetime import date

class Payment:
    def __init__(self, payment_id, amount, payment_date, payment_deadline, payment_status):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_date = payment_date
        self.payment_deadline = payment_deadline
        self.payment_status = payment_status

    def process_payment(self, cost):
        print(f"Processing payment {self.payment_id}: ")
        if cost > self.amount:
            print(f"Payment not fully paid, remaining amount is {cost - self.amount}. Please pay the remaining amount by {self.payment_deadline}.")
            self.payment_status = "unpaid"
        else:
            print(f"Payment {self.payment_id} paid.")
            self.payment_status = "paid"
        return(f"ID {self.payment_id}\nDate: {self.payment_date}\nStatus: {self.payment_status}")