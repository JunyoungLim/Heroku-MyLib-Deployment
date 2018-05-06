from app import db
import pickle

class Index(db.Model):
    __tablename__ = 'indices'
    id           = db.Column(db.String, unique=True, primary_key=True)
    index        = db.Column(db.String)
    
    def __init__(self):
        """
        Constructor
        """
        self.id = "inv_index"

        inv_index = InvIndex(nltk.word_tokenize, 
              EnglishStemmer(), 
              nltk.corpus.stopwords.words('english'))
        self.index = pickle.dumps(inv_index)