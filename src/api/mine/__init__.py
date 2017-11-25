from flask import Blueprint

mine = Blueprint('mine', __name__)

from . import views