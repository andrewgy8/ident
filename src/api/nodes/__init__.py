from flask import Blueprint

nodes = Blueprint("nodes", __name__)

from . import resgister