from flask import *
from . import api_endpoints
from block import blockchain


@api_endpoints.route('/chain', methods=['GET'])
def full_chain():

    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200
