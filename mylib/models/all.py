from marshmallow_sqlalchemy import field_for, ModelSchema
from mylib.models.images import *
from mylib.models.collections import *
from mylib.indexing.inverted_index import Index

class CollectionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
      model = Collection

class ImageSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Image

class IndexSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Index
