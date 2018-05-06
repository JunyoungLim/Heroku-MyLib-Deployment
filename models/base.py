class Base(db.Model):
  """
  Base database model
  """
  __abstract__ = True
  created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default = db.func.current_timestamp())

class CollectionSchema(ModelSchema):
    class Meta:
      model = Collection

class ImageSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Image

collection_schema = CollectionSchema()
image_schema = ImageSchema()