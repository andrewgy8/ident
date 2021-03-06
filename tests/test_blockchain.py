import unittest
from urllib.parse import ParseResult
from time import time
from src.api.nodes.services import NodeService
from src.blockchain import Blockchain
from tests.helpers.transaction_factory import TransactionFactory, Transaction


class TestBlockchainTransactions(unittest.TestCase):

    def setUp(self):
        self.bc = Blockchain()

    def tearDown(self):
        self.bc = None

    def add_transactions(self, num):
        n_transactions = TransactionFactory(num)

        for transx in n_transactions.transactions:
            self.bc.add_transaction(transx.sender, transx.receiver, transx.payload, transx.key)

    def test_should_add_a_block_to_the_chain_through_transactions(self):
        t = Transaction()
        self.bc.add_transaction(t.sender, t.receiver, t.payload, t.key)

        trans_1 = self.bc.transactions[0]
        self.assertEqual(t.sender, trans_1['sender'])
        self.assertEqual(t.receiver, trans_1['recipient'])
        # self.assertEqual(t.payload, trans_1['information'])
        self.assertIs(len(self.bc.transactions), 1)

        count = 4
        n_transactions = TransactionFactory(count)

        for transx in n_transactions.transactions:
            self.bc.add_transaction(transx.sender, transx.receiver, transx.payload, t.key)

        self.assertIs(len(self.bc.transactions), count + 1)

    def test_add_block_to_chain(self):
        count = 10
        self.add_transactions(count)

        self.assertIs(len(self.bc.transactions), count)

        last_block = self.bc.last_block
        last_proof = last_block.get('proof')
        proof = self.bc.proof_of_work(last_proof)

        block = self.bc.add_block_to_chain(proof)
        self.assertEqual(len(block.get('transactions')), count)
        self.assertEqual(self.bc.length, 2)

    def test_should_hash_and_de_hash(self):
        block = {
            'index': 1,
            'timestamp': time(),
            'transactions': [],
            'proof': 1,
            'previous_hash': 'abcd',
        }
        res = Blockchain.hash(block)
        assert res
        proof = 0
        while Blockchain.valid_proof(1, proof) is False:
            proof += 1
        assert isinstance(proof, int)


class TestBlockChainNodes(unittest.TestCase):
    def setUp(self):
        self.bc = Blockchain()

    def tearDown(self):
        self.bc = None

    def test_should_add_nodes_to_blockchain_without_duplicates(self):
        """
        Adding multiple nodes to the blockchain and silently passing over duplicates.  
        
        A duplicatied node that has been registered should only have one instance in the Blockchain
        
        :return: 
        """
        addr_1 = 'localhost:8000'
        addr_2 = 'localhost:8001'
        n = NodeService(self.bc)
        n.register_node(addr_1)

        e = next(iter(self.bc.nodes))
        self.assertIsInstance(e, ParseResult)
        assert addr_1 in e

        n.register_node(addr_2)

        n.register_node(addr_2)
        assert len(self.bc.nodes) == 2
