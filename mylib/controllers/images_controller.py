from app.constants import *
from . import *
from flask import request
from app.mylib.models.images import *
from app.mylib.models.collections import *

@mylib.route('/images', methods=['POST'])
def insert_image():
  title = request.args.get('title')

  image = Image(title)
  db.session.add(image)
  db.session.commit()

  return image_schema.dump(image).data

@mylib.route('/images', methods=['PUT'])
def update_collection_for_image():
  collection_id = request.args.get('collection_id')
  image_id = request.args.get('image_id')

  collection = Collection.query.filter_by(id=collection_id).first()
  collection.images += [image_id]
  
  image = Image.query.filter_by(id=image_id).first()
  image.collection_id = collection_id

  db.session.commit()

  return image_schema.dump(image).data
