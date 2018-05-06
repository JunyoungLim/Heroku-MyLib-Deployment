from models.base import Base
from 

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