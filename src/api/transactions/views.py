from flask import request, jsonify
from src.blockchain import blockchain
from . import transactions
import json


@transactions.route('/add', methods=['POST'])
def add_transaction():
    values = request.json


    required = ['sender', 'recipient', 'information', 'key']

    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(**values)
    response = {
        'message': f'Transaction will be added to Block {index}'
    }
    return jsonify(response), 201
