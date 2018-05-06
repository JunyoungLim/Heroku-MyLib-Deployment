from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.register_blueprint(image_blueprint)
app.register_blueprint(collection_blueprint)

from models import Image, Collection

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


@app.route('/collections', methods=['POST'])
def insert_collection():
    title = request.args.get('title')

    collection = Collection(title)
    db.session.add(collection)
    db.session.commit()

    return collection_schema.dump(collection).data

@app.route('/images', methods=['POST'])
def insert_image():
    title = request.args.get('title')

    image = Image(title)
    db.session.add(image)
    db.session.commit()

    return image_schema.dump(image).data

@app.route('/images', methods=['PUT'])
def update_collection_for_image():
    collection_id = request.args.get('collection_id')
    image_id = request.args.get('image_id')

    collection = Collection.query.filter_by(id=collection_id).first()
    collection.images += [image_id]
  
    image = Image.query.filter_by(id=image_id).first()
    image.collection_id = collection_id

    db.session.commit()

    return image_schema.dump(image).data

if __name__ == '__main__':
    app.run()
