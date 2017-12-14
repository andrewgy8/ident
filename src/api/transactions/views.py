from flask import request, jsonify
from src.blockchain import blockchain
from . import transactions


@transactions.route('/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'information', 'key']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.add_transaction(**values)

    response = {
        'message': f'Transaction will be added to Block {index}'
    }
    return jsonify(response), 201
