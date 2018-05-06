from app import *
from flask import request, jsonify
from mylib.controllers import *
from mylib.models.all import *
from mylib.models.images import *
from mylib.models.collections import *

@mylib.route('/collections', methods=['POST'])
def insert_collection():
    title = request.args.get('title')

    collection = Collection(title)
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection_schema.dump(collection).data)

