import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
from app import db
from base64 import b64encode

# download punkt sentence tokenizer
nltk.download('punkt')
nltk.download('stopwords')
 
###############################################################################
# Inverted Index Data Structure
# Assumes English (stopwords, etc)
# Inspired by: https://nlpforhackers.io/, How to build an inverted index
###############################################################################

class InvIndex:
    def __init__(self, tokenizer=nltk.word_tokenize, stemmer=None, stopwords=None):
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.stopwords = set(stopwords) if stopwords else set()

        self.index = defaultdict(list)
    
    def clear(self):
        self.index = defaultdict(list)

    def process(self, word):
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)
        return word

    def lookup(self, word):
        word = self.process(word)
        lst = self.index.get(word)
        if lst:
            return [id in lst]
        else:
            return []
    
    def remove(self, text, document_id):
        for token in [t for t in self.tokenizer(text)]:
            token = self.process(token)

            if token in self.stopwords:
                continue
            
            self.index[token].remove(document_id)

    def add(self, text, document_id):
        for token in [t for t in self.tokenizer(text)]:
            token = self.process(token)
            
            if token in self.stopwords:
                continue

            if document_id not in self.index[token]:
                self.index[token].append(document_id)

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
        self.index = b64encode(inv_index)
