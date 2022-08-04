from flask import Flask, request, jsonify, Response
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask-mongo'

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["flask-mongo"]
users_col = my_db["users"]


@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if not username or not email or not password:
        return bad_request()
    hashed_password = generate_password_hash(password)
    user_id = users_col.insert_one({
        'username': username,
        'email': email,
        'password': hashed_password
    })
    response = {
        'id': str(user_id.inserted_id),
        'username': username,
        'email': email
    }
    return response


@app.route('/users', methods=['GET'])
def get_users():
    users = users_col.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_col.find_one({'_id': ObjectId(user_id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response


@app.errorhandler(400)
def bad_request(error=None):
    response = jsonify({
        'message': 'Bad Request ' + request.url,
        'status': 400
    })
    response.status_code = 400
    return response


if __name__ == "__main__":
    app.run(debug=True)
