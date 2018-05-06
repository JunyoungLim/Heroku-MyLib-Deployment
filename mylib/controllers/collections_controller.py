from app import *
from flask import request, jsonify
from mylib.controllers import *
from mylib.models.all import *
from mylib.models.images import *
from mylib.models.collections import *
from mylib.indexing.inverted_index import *
import pickle

@mylib.route('/collections', methods=['POST'])
def insert_collection():
    title = request.args.get('title')

    if Collection.query.filter_by(title=title).first():
        return jsonify({"message": "Collection title already taken."})

    collection = Collection(title)
    db.session.add(collection)
    db.session.commit()

    return jsonify(collection_schema.dump(collection).data)

@mylib.route('/collections', methods=['GET'])
def get_collection():
  title = request.args.get('title')
  collection = Collection.query.filter_by(title=title).first()
  return jsonify(collection_schema.dump(collection).data)

@mylib.route('/collections/all', methods=['GET'])
def get_all_collection():
  collections = Collection.query.all()
  ret = []
  for col in collections:
    ret += [collection_schema.dump(col).data]
  return jsonify(ret)


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

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index = Index()
    db.session.add(inv_index)
    db.session.commit()
    inv_index = inv_index.index
    inv_index = pickle.loads(inv_index)

  collection = Collection.query.filter_by(title=collection_title).first()
  for image in collection.images:
    db.session.delete(image)
    inv_index.remove(image.text, image.id)
    inv_index.remove(image.label, image.id)
    inv_index.remove(image.title, image.id)
  
  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index

  db.session.delete(collection)
  db.session.commit()

  return jsonify(collection_schema.dump(collection).data)

@mylib.route('/collections/all', methods=['DELETE'])
def delete_all_collection():
  collection = Collection.query.delete()
  db.session.commit()

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index = Index()
    db.session.add(inv_index)
    db.session.commit()
    inv_index = inv_index.index
    inv_index = pickle.loads(inv_index)

  inv_index.clear()

  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index
  db.session.commit()

  return jsonify({"success":"true"})

