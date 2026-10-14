class Category():
    def __init__(self,name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({
            'amount': amount,
            'description': description
            })

    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            self.ledger.append({
            'amount': -amount,
            'description': description
            })
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self,amount,catagory):
        if self.check_funds(amount):
            self.withdraw(amount,f"Transfer to {catagory.name}")
            catagory.deposit(amount,f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self,amount):
        return amount <= self.getbalance

    def __str__(self):
        output = "*" * (30 - len(self.name))//2
        output += self.name
        output += "*" * (30 - len(output))

        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:.2f}"

            output += f"\n{description:<23}{amount:>7}"

        output += f"/ntotal: {self.get_balance():.2f}"
