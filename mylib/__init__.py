from flask import Blueprint

# MyLib Blueprint
mylib = Blueprint('mylib', __name__, url_prefix='/mylib')

# Import all endpoints
from controllers.images_controller import *
from controllers.collections_controller import *
