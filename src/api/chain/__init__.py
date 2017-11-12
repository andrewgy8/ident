from flask import Blueprint

chain = Blueprint('chain', __name__)

from . import views