from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask-mongo'

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=True)
