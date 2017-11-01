from block_api.endpoints import api_endpoints
from flask import *
from block import blockchain
from block.services import ConflictService


@api_endpoints.route('/nodes/resolve', methods=['GET'])
def consensus():
    c = ConflictService(blockchain)
    replaced = c.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
