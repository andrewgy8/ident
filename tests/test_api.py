from flask_testing import TestCase
from flask import url_for
from src import test_app
from src.blockchain import blockchain
from tests.helpers.transaction_factory import TransactionFactory
import json


class BaseTest(TestCase):
    url = ''

    def setUp(self):
        self.bc = blockchain

    def create_app(self):
        return test_app()

    def tearDown(self):
        self.bc = None

    def get(self):
        return self.client.get(url_for(self.url))

    def post(self, params):
        return self.client.post(url_for(self.url),
                                data=json.dumps(params),
                                content_type='application/json')


class BaseFactory(BaseTest):

    def add_new_transactions(self, num):
        n_transactions = TransactionFactory(num)

        for transx in n_transactions.transactions:
            self.bc.add_transaction(transx.sender, transx.receiver, transx.payload, transx.key)

    def add_block_to_chain(self):

        last_block = self.bc.last_block
        last_proof = last_block['proof']
        proof = self.bc.proof_of_work(last_proof)

        return self.bc.add_block_to_chain(proof)


class TestChainEndpoint(BaseFactory):
    url = 'chain.full_chain'

    def test_calling_chain_returns_chain_value(self):
        self.add_new_transactions(10)
        block = self.add_block_to_chain()
        response = self.get()

        self.assert_200(response)
        assert block in response.json['chain']
        assert self.bc.chain == response.json['chain']


class TestMineEndpoint(BaseFactory):
    url = 'mine.mine_transactions'

    def test_no_transactions_pending_is_ok_to_mine(self):
        rv = self.get()

        self.assert_200(rv)
        assert self.bc.transactions == rv.json['transactions']

        resp = self.client.get("/chain/")
        assert self.bc.chain == resp.json['chain']


class TestTransactionEndpoint(BaseFactory):
    url = 'transactions.add_transaction'

    def test_proper_form_submittal(self):
        params = {
            'sender': 'Andrew',
            'recipient': 'Eva',
            'information': {
                'info': 'this is the secret info'
            },
            'key': 'secret_key'
        }
        res = self.post(params)
        assert res.status == '201 CREATED'

    def test_invalid_form_submittal(self):
        params = {
            'test':'nothing'
        }
        res = self.post(params)
        self.assert_400(res)