from flask import Blueprint

transactions = Blueprint('transactions', __name__)

from . import views