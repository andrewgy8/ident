from faker import Faker
import random

fake = Faker()


class Transaction(object):
    def __init__(self):
        self.sender = fake.name()
        self.receiver = fake.name()
        self.amount = random.randint(1, 1000)


class TransactionFactory(object):
    def __init__(self, quantity):
        self.transactions = []
        self.quantity = quantity
        self.make_transactions()

    def make_transactions(self):
        for _ in range(self.quantity):
            self.transactions.append(Transaction())




