from base import Base
from app import db
import uuid
from datetime import datetime

class Image(Base):
    __tablename__ = 'images'
    
    id             = db.Column(db.String, unique=True, primary_key=True)
    title          = db.Column(db.String, nullable=False)
    collection_id  = db.Column(db.String, db.ForeignKey('collections.id'), nullable=True)
    
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