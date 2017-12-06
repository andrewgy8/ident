from flask import Flask

from src.api.chain import chain
from src.api.mine import mine
from src.api.nodes import nodes
from src.api.transactions import transactions
from src.blockchain import Blockchain


def run_app(debug=True, port=5100):
    api = Flask(__name__)

    api.register_blueprint(transactions, url_prefix='/transactions')
    api.register_blueprint(mine, url_prefix='/mine')
    api.register_blueprint(nodes, url_prefix='/nodes')
    api.register_blueprint(chain, url_prefix='/chain')
    return api.run(debug=debug,
                   port=port
                   )

