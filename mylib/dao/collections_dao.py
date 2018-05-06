from . import *
from mylib.models.images import *
from mylib.models.collections import *

"""
Add more methods below!!!
"""

def collection_by_id(collection_id):
  """
  Get board by ID
  """
  return Collection.query.filter_by(id=collection_id).first()
