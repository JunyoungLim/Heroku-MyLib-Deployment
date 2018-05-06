from marshmallow_sqlalchemy import ModelSchema
from app import db

class Base(db.Model):
  """
  Base database model
  """
  __abstract__ = True
  created_at = db.Column(db.DateTime, default = db.func.now())
  updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())
