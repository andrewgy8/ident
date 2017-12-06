from flask_testing import TestCase

from src import test_app
from src.blockchain import blockchain
from tests.helpers.transaction_factory import TransactionFactory


class ChainAPITest(TestCase):

    def setUp(self):
        self.bc = blockchain

    def create_app(self):
        return test_app()

    def tearDown(self):
        self.bc = None

    def add_new_transactions(self, num):
        n_transactions = TransactionFactory(num)

        for transx in n_transactions.transactions:
            self.bc.new_transaction(transx.sender, transx.receiver, transx.amount)

    def add_block_to_chain(self):

        last_block = self.bc.last_block
        last_proof = last_block['proof']
        proof = self.bc.proof_of_work(last_proof)

        return self.bc.add_block_to_chain(proof)

    def test_calling_chain_returns_chain_value(self):
        self.add_new_transactions(10)
        block = self.add_block_to_chain()
        response = self.client.get("/chain/")

        self.assert_200(response)
        assert block in response.json['chain']
        assert self.bc.chain == response.json['chain']

    def test_no_transactions_pending_is_ok_to_mine(self):
        rv = self.client.get("/mine/")

        self.assert_200(rv)
        assert self.bc.transactions == rv.json['transactions']

        resp = self.client.get("/chain/")
        assert self.bc.chain == resp.json['chain']

    def test_mining_transactions(self):
        pass