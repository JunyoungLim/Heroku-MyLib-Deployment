from . import *
from flask import request, jsonify
from mylib.models.images import *
from mylib.models.collections import *
from mylib.ocr.google_vis import ocr
from mylib.indexing.inverted_index import *
import pickle

@mylib.route('/images', methods=['POST'])
def insert_image():
  title = request.args.get('title')
  content = request.args.get('content')

  image = Image(title)

  if Image.query.filter_by(title=title).first():
    return jsonify({"message": "Image title already taken."})

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index_entry = Index()
    db.session.add(inv_index_entry)
    db.session.commit()
    inv_index = inv_index_entry.index
    inv_index = pickle.loads(inv_index)
  
  inv_index.add(title, image.id)

  text_extracted, label_extracted = ocr.extract_text_and_label([content])
  if text_extracted:
    inv_index.add(text_extracted[0], image.id)
    image.text = text_extracted[0]
  if label_extracted:
    inv_index.add(label_extracted[0], image.id)
    image.label = label_extracted[0]

  db.session.add(image)

  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index

  db.session.commit()

  return jsonify(image_schema.dump(image).data)

@mylib.route('/images', methods=['GET'])
def get_image():
  keyword = request.args.get('keyword')

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index_entry = Index()
    db.session.add(inv_index_entry)
    db.session.commit()
    inv_index = inv_index_entry.index
    inv_index = pickle.loads(inv_index)

  id_list = inv_index.lookup(keyword)

  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index
  db.session.commit()

  ret = []
  for img_id in id_list:
    img = Image.query.filter_by(id=img_id).first()
    ret += [image_schema.dump(img).data]

  return jsonify(ret)

@mylib.route('/images/all', methods=['GET'])
def get_all_image():
  images = Image.query.all()

  ret = []
  for img in images:
    ret += [image_schema.dump(img).data]
  return jsonify(ret)

@mylib.route('/images', methods=['PUT'])
def update_image():
  if request.args.get('collection_title'):
    collection_title = request.args.get('collection_title')
    image_title = request.args.get('image_title')

    collection = Collection.query.filter_by(title=collection_title).first()
    collection.images += [Image.query.filter_by(title=image_title).first()]
  
    image = Image.query.filter_by(title=image_title).first()
    image.collection_id = collection.id

    db.session.commit()

    return jsonify(image_schema.dump(image).data)

  elif request.args.get('title'):
    new_title = request.args.get('new_title')
    image_id = request.args.get('image_title')

    image = Image.query.filter_by(title=image_title).first()
    image.title = new_title

    db.session.commit()

    return jsonify(image_schema.dump(image).data)


@mylib.route('/images', methods=['DELETE'])
def delete_image():
  image_title = request.args.get('title')

  image = Image.query.filter_by(title=image_title).first()
  db.session.delete(image)
  db.session.commit()

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index_entry = Index()
    db.session.add(inv_index_entry)
    db.session.commit()
    inv_index = inv_index_entry.index
    inv_index = pickle.loads(inv_index)

  inv_index.remove(image.text, image.id)
  inv_index.remove(image.label, image.id)
  inv_index.remove(image.title, image.id)

  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index
  db.session.commit()

  return jsonify(image_schema.dump(image).data)

@mylib.route('/images/all', methods=['DELETE'])
def delete_all_image():
  image = Image.query.delete()
  db.session.commit()

  inv_index_entry = Index.query.filter_by(id="inv_index").first()
  if inv_index_entry:
    inv_index = pickle.loads(inv_index_entry.index)
  else:
    inv_index_entry = Index()
    db.session.add(inv_index_entry)
    db.session.commit()
    inv_index = inv_index_entry.index
    inv_index = pickle.loads(inv_index)

  inv_index.clear()

  inv_index = pickle.dumps(inv_index)
  inv_index_entry.index = inv_index
  db.session.commit()

  return jsonify({"success":"true"})

