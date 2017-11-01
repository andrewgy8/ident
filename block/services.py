from urllib.parse import urlparse
import requests


class NodeService:

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def register_node(self, addr):
        parsed_url = urlparse(addr)
        print(self.blockchain.nodes, parsed_url)
        self.blockchain.nodes.add(parsed_url)


class ConflictService:

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.blockchain.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.blockchain.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:

            response = requests.get(f'http://{node}/api/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.blockchain.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.blockchain.chain = new_chain
            return True

        return False


class ValidationService:

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.blockchain.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.blockchain.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

