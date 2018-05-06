from flask import request, render_template, jsonify
from functools import wraps # for decorators
import app

# Models
from mylib.models.all import *

# DAO
from mylib.dao import collections_dao

# Serializers
image_schema         = ImageSchema()
collection_schema    = CollectionSchema()

# Blueprint
from mylib import mylib
from flask import Blueprint

# Image Blueprint
image_blueprint = Blueprint('image_blueprint', __name__, url_prefix='/images')
collection_blueprint = Blueprint('collection_blueprint', __name__, url_prefix='/collections')
