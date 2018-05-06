from app.constants import *
from . import *
from flask import request
from app.mylib.models.all import *
from app.mylib.models.images import *
from app.mylib.models.collections import *

@mylib.route('/collections', methods=['POST'])
def insert_collection():
  title = request.args.get('title')

  collection = Collection(title)
  db.session.add(collection)
  db.session.commit()

  return collection_schema.dump(collection).data

