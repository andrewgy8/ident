from flask import Blueprint

api_endpoints = Blueprint('api_endpoints', __name__)

from . import chain, mine, new_transaction
from .nodes import resgister, resolve