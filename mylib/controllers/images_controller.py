from . import *
from flask import request, jsonify
from mylib.models.images import *
from mylib.models.collections import *
from mylib.ocr.google_vis import ocr
from mylib.indexing.inverted_index import inv_index

@mylib.route('/images', methods=['POST'])
def insert_image():
  title = request.args.get('title')
  content = request.args.get('content')

  image = Image(title)

  text_extracted, label_extracted = ocr.extract_text_and_label([content])
  inv_index.add(text_extracted[0], image.id)
  inv_index.add(label_extracted[0], image.id)

  image.text = text_extracted[0]
  image.label = label_extracted[0]

  db.session.add(image)
  db.session.commit()

  return jsonify(image_schema.dump(image).data)

@mylib.route('/images', methods=['GET'])
def get_image():
  title = request.args.get('title')

  image = Image.query.filter_by(title=title).first()

  return jsonify(image_schema.dump(image).data)

@mylib.route('/images/all', methods=['GET'])
def get_all_image():
  title = request.args.get('title')

  images = Image.query.all()

  return jsonify(image_schema.dump(images).data)


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

  inv_index.remove(image.text, image.id)
  inv_index.remove(image.label, image.id)

  return jsonify(image_schema.dump(image).data)
