from app import *
from flask import request, jsonify
from mylib.controllers import *
from mylib.models.all import *
from mylib.models.images import *
from mylib.models.collections import *
from mylib.indexing.inverted_index import *

@mylib.route('/collections', methods=['POST'])
def insert_collection():
    title = request.args.get('title')

    if Collection.query.filter_by(title=title).first():
        return jsonify({"success": "false"})

    collection = Collection(title)
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection_schema.dump(collection).data)

@mylib.route('/collections', methods=['PUT'])
def update_collection():
  new_title = request.args.get('new_title')
  collection_title = request.args.get('collection_title')
  
  collection = Collection.query.filter_by(title=collection_title).first()
  collection.title = new_title
  
  db.session.commit()
  
  return jsonify(collection_schema.dump(collection).data)


@mylib.route('/collections', methods=['DELETE'])
def delete_collection():
  collection_title = request.args.get('title')

  collection = Collection.query.filter_by(title=collection_title).first()
  for image in collection.images:
      db.session.delete(image)
      inv_index.remove(image.text, image.id)
      inv_index.remove(image.label, image.id)

  db.session.delete(collection)
  db.session.commit()

  return jsonify(collection_schema.dump(collection).data)

