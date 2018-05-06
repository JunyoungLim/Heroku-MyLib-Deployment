from app.constants import *
from . import *
from app.mylib.models.images import *
from app.mylib.models.collections import *

"""
Add more methods below!!!
"""

def collection_by_id(collection_id):
  """
  Get board by ID
  """
  return Collection.query.filter_by(id=collection_id).first()
