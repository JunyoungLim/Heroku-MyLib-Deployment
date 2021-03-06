# Heroku-MyLib-Deployment

## Part 1: PostgreSQL Backend
The backend is developed using PostgreSQL, Flask, SQLAlchemy, and python 2.7.14.

We have two tables: Collection and Image. Collection table is the "parent" table that has images associated with it, and Image table has all entries for images inserted. Both of them support CRUD interface (updating title, inserting new entry, deleting a sepcific entry, retrieving certain entry, etc), with the following additional features.

## Part 2: Optical Character Recognition (OCR)
The second feature of the backend is to extract texts from an image uri or byte-encoded string (for the production server, it only accepts image uri because byte-encoded string is too large to test the api call). In order for an app to extract meaningful texts from the given images, the server analyzes the image and extracts any texts detected and any labels computed.

The initial attempt was implementing the OCR feature using pytesseract library. Given a screenshot of a website or a picture of printed pages, the OCR detected texts really well, yet it barely recognized any of handwritten texts. To make the backend more useful, it was necessary to find some other way for text detection.

While browsing internet, we bumped into the Google's ML API. Google was providing various API's, including the ones that supports OCR and Label detection from a given image. So, as the second attempt, we used Google's vision API to solve the OCR feature. We created a wrapper class that format the json file given a list of image uri's (and image byte-encoded string using base64 format) and retrieves outputs. Once these informations are extracted, we stored them into each image object, which will be used when a user wants to search a list of images with certain keyword, or query, that they put in the search bar. However, merely searching through the entire database is too time-expensive, so we implemented the third feature.

### Note
If you want to deploy yourself after git cloning, make sure to export the following:

```bash
$ export APP_SETTINGS="config.DevelopmentConfig"
$ export DATABASE_URL="postgresql://localhost/<Your Database Name Here>"
$ export GOOGLE_ML_API_KEY="<Your API KEY Here>"
```

to the actual API_KEY you have with your Google Developer account for Google Vision API.

## Part 3: Inverted Indexing
The third feature of the backend is inverted indexing. More details about inverted indexing can be found here.

[Inverted Index Search](https://www.quora.com/What-is-inverted-index-It-is-a-well-known-fact-that-you-need-to-build-indexes-to-implement-efficient-searches-What-is-the-difference-between-index-and-inverted-index-and-how-does-one-build-inverted-index)

![alt text](https://qph.fs.quoracdn.net/main-qimg-64eb40af5510bc3e201726674197b3dc-c)

To make query search more efficient, we inverted image -> text to text -> image indexing, so that whenever a user inputs a query, we can directly map the query to a list of images associated with it. To permanently maintain the indexing dictionary, we serialized the object and stored it into the database; wenever there needs an update to the dictionary, it gets deserialized, updated, and re-serialized and then committed to the database.

## Server Address
Staging Server: https://cuappdev-mylib-2018-stage.herokuapp.com/

Production Server: https://cuappdev-mylib-2018-pro.herokuapp.com/

## Example API Request
POST: https://cuappdev-mylib-2018-pro.herokuapp.com/mylib/images?title=curious.png&content=https://i.stack.imgur.com/vrkIj.png

The above request will insert the image with the following image uri.

GET: https://cuappdev-mylib-2018-pro.herokuapp.com/mylib/images?keyword=curious

The above request will retrieve all the images that are associated with query "curious."
