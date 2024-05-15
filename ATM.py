class ATM:
    SECRET_CODE = "CloseItDown"

    def __init__(self, bank):
        self._account = None
        self._bank = bank
        self._method = {
            "1": self._get_balance,
            "2": self._deposit,
            "3": self._withdraw,
            "4": self._quit
        }

    def run(self):
        while True:
            name = input("Enter your name: ")
            if name == ATM.SECRET_CODE:
                break
            pin = input("Enter your pin: ")
            self._account = self._bank.get(pin)
            if not self._account:
                create_account = input(
                    "No account found. Do you want to create a new account? (y/n): ")
                if create_account.lower() == "y":
                    self._account = self._create_account(name, pin)
                else:
                    print("Exiting...")
                    break
            elif self._account.get_name() != name:
                print("Error, unrecognized name")
                self._account = None
            else:
                self._process_account()
        else:
            self._process_account()

    def _create_account(self, name, pin):
        account = Account(pin, name)
        self._bank.add(account)
        print("Account created successfully!")
        return account

    def _process_account(self):
        while True:
            print("1  View your Balance")
            print("2  Make a deposit")
            print("3  Make a withdrawal")
            print("4  Quit\n")
            number = input("Enter a number: ")
            the_method = self._method.get(number)
            if the_method is None:
                print("Unrecognized number")
            else:
                the_method()
                if not self._account:
                    break

    def _get_balance(self):
        print("Your Balance is $", self._account.get_balance())

    def _deposit(self):
        try:
            amount = float(input("Enter the amount to deposit: "))
            self._account.deposit(amount)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def _withdraw(self):
        try:
            amount = float(input("Enter the amount to withdraw: "))
            self._account.withdraw(amount)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def _quit(self):
        self._bank.save()
        self._account = None
        print("Have a nice day!")


class Bank:
    def __init__(self):
        self.accounts = {}

    def get(self, account_no):
        return self.accounts.get(account_no)

    def add(self, account):
        self.accounts[account.number] = account

    def save(self):
        # Implement saving account information to a file
        with open("accounts.txt", "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.number},{account.get_name()},{
                           account.get_balance()}\n")


class Account:
    def __init__(self, number, name, balance=0):
        self.number = number
        self.name = name
        self.balance = balance

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient balance")

    def deposit(self, amount):
        self.balance += amount


def main():
    bank = Bank()
    atm = ATM(bank)
    atm.run()


if __name__ == "__main__":
    main()
