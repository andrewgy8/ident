from time import time
import json
import hashlib


class PersonalInformation:
    def __init__(self,
                 key,
                 **kwargs):

        self.key = key
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone_number')

    def lock(self, **kwargs):
        """
        Hashes personal information with key 
        so that it can not be compromised.
         
        :param kwargs: 
        :return: 
        """
        return

    def submit(self):
        return

    def _to_json(self):
        return


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.add_block_to_chain(proof=100, previous_hash=1)

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def length(self):
        return len(self.chain)

    def add_transaction(self, sender, receiver, payload):
        receipt = {
            'sender': sender,
            'receiver': receiver,
            'payload': payload
        }

        self.transactions.append(receipt)
        return self.last_block['index'] + 1

    def add_block_to_chain(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        do some form of de-hashing to match a particular proof
        :return: 
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, key="0000"):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == key

blockchain = Blockchain()
