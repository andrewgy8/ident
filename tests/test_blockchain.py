import unittest
from urllib.parse import ParseResult

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
            self.bc.add_transaction(transx.sender, transx.receiver, transx.amount)

    def test_should_add_a_block_to_the_chain_through_transactions(self):
        t = Transaction()
        self.bc.add_transaction(t.sender, t.receiver, t.amount)

        t_1 = self.bc.transactions[0]
        self.assertEqual(t.sender, t_1['sender'])
        self.assertEqual(t.receiver, t_1['receiver'])
        self.assertEqual(t.amount, t_1['payload'])
        self.assertIs(len(self.bc.transactions), 1)

        num_trans_to_make = 4
        n_transactions = TransactionFactory(num_trans_to_make)

        for transx in n_transactions.transactions:
            self.bc.add_transaction(transx.sender, transx.receiver, transx.amount)

        self.assertIs(len(self.bc.transactions), num_trans_to_make + 1)

    def test_add_block_to_chain(self):
        tansx_count = 10
        self.add_transactions(tansx_count)

        self.assertIs(len(self.bc.transactions), tansx_count)

        last_block = self.bc.last_block
        last_proof = last_block.get('proof')
        proof = self.bc.proof_of_work(last_proof)

        block = self.bc.add_block_to_chain(proof)
        self.assertEqual(len(block.get('transactions')), tansx_count)
        self.assertEqual(self.bc.length, 2)

    def test_should_hash_and_de_hash(self):
        pass


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
