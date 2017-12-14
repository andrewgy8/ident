from faker import Faker
import random

fake = Faker()


class Transaction(object):
    def __init__(self):
        self.sender = fake.name()
        self.receiver = fake.name()
        self.payload = dict(name='Andrew', surname='Graham')
        self.key = 'secret'


class TransactionFactory(object):
    def __init__(self, quantity):
        self.transactions = []
        self.quantity = quantity
        self._make_transactions()

    def _make_transactions(self):
        for _ in range(self.quantity):
            self.transactions.append(Transaction())




