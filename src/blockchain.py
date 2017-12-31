from time import time
import json
import hashlib
import jwt


class SecretInformation:
    """
    The kwargs can be a dict of any information that will encoded with
    the users key.  
    """
    def __init__(self,
                 key,
                 **kwargs):
        self.key = key
        self.encoded_info = self.__encode(**kwargs)
        self.info_str = self.encoded_info.decode('utf-8')

    def __encode(self, **kwargs):
        return jwt.encode({**kwargs}, key=self.key, algorithm='HS256')

    def is_valid(self, **kwargs):
        decoded = jwt.decode(self.encoded_info, self.key)
        try:
            assert decoded == {**kwargs}
        except AssertionError:
            return False
        else:
            return True


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

    def add_transaction(self, sender, recipient, information, key):
        secret = SecretInformation(key=key, **information)
        receipt = {
            'sender': sender,
            'recipient': recipient,
            'information': secret.info_str
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
