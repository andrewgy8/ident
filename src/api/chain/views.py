from flask import *
from src.blockchain import blockchain
from . import chain


@chain.route('/', methods=['GET'])
def full_chain():

    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200
