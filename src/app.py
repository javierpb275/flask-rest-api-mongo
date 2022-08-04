from flask import Flask, request, jsonify
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

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
