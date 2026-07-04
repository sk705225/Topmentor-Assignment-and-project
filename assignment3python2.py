# Bank Transaction Simulator using Class and Object

class BankAccount:

    def __init__(self):
        self.balance = 0

    # Deposit money
    def deposit(self, amount):
        self.balance = self.balance + amount
        print("Deposited:", amount)

    # Withdraw money
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance = self.balance - amount
            print("Withdrawn:", amount)
        else:
            print("Insufficient Balance")

    # Check current balance
    def check_balance(self):
        print("Current Balance:", self.balance)


# Create object
account = BankAccount()

# Perform transactions
account.deposit(5000)
account.withdraw(1500)
account.check_balance()