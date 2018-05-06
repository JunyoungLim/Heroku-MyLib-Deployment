from app import db
from sqlalchemy.dialects.postgresql import JSON
import uuid

class Base(db.Model):
  """
  Base database model
  """
  __abstract__ = True
  created_at = db.Column(db.DateTime, default = db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default = db.func.current_timestamp())

class Image(Base):
    __tablename__ = 'images'
    
    id             = db.Column(db.Integer, unique=True, primary_key=True)
    title          = db.Column(db.String(), nullable=False)
    collection_id  = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=False)
    
    def __init__(self, title):
        """
        Constructor
        """
        self.id = str(uuid.uuid1())
        self.title = title
        self.collection_id = None
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
        
    def has_collection(self):
        if (self.collection_id is None):
            return False
        return True

class Collection(Base):
    __tablename__ = 'images'
    
    id             = db.Column(db.Integer, unique=True, primary_key=True)
    title          = db.Column(db.String(), nullable=False)
    images         = db.relationship('Image', backref='collections', lazy=True)
    
    def __init__(self, title):
        """
        Constructor
        """
        self.id = str(uuid.uuid1())
        self.title = title
        self.images = []
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
