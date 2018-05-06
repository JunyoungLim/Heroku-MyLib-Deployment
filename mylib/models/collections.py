from base import Base
from app import db
import uuid
from datetime import datetime

class Collection(Base):
    __tablename__ = 'collections'
    
    id             = db.Column(db.String, unique=True, primary_key=True)
    title          = db.Column(db.String, unique=True, nullable=False)
    images         = db.relationship('Image', cascade="all,delete", backref='collections', lazy=True)
    
    def __init__(self, title):
        """
        Constructor
        """
        self.id = str(uuid.uuid1())
        self.title = title
        self.images = []
    
    def __repr__(self):
        return '<id {}>'.format(self.id)