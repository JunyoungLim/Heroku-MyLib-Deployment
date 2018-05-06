from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from mylib.indexing.inverted_index import Index
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from mylib import mylib as mylib
app.register_blueprint(mylib)

@app.route('/')
def hello():
    inv_index = Index()
    db.session.add(inv_index)
    db.session.commit()
    return render_template("index.html")

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
