from base import Base
import uuid

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