import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer

# download punkt sentence tokenizer
nltk.download('punkt')
nltk.download('stopwords')
 
###############################################################################
# Inverted Index Data Structure
# Assumes English (stopwords, etc)
# Inspired by: https://nlpforhackers.io/, How to build an inverted index
###############################################################################

class InvIndex:
    def __init__(self, tokenizer, stemmer=None, stopwords=None):
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
        return [id in self.index.get(word)]
    
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
    

# Inverse Indexing initialized
inv_index = InvIndex(nltk.word_tokenize, 
              EnglishStemmer(), 
              nltk.corpus.stopwords.words('english'))