from flask import *
from block_api.endpoints import api_endpoints


api = Flask(__name__)

api.register_blueprint(api_endpoints, url_prefix='/api')

