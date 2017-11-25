from flask import jsonify

from src.blockchain import blockchain
from config import node_identifier
from . import mine


@mine.route('/', methods=['GET'])
def mine_transactions():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        receiver=node_identifier,
        payload=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.add_block_to_chain(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
