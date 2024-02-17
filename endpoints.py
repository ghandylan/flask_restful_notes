import os

import bcrypt
from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import User, db

endpoint = Blueprint('endpoints', __name__)


# Method: GET
# Description: This endpoint returns a simple greeting message in JSON format.
# Response: {'message': 'Hello World'}
@endpoint.route('/')
def index():
    return jsonify({'message': 'Hello World'})


@endpoint.route('/user/<int:user_id>', methods=['GET'])
def show_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return make_response(jsonify({'message': 'user does not exist'}))
    user_data = {'id': user.id, 'name': user.name, 'phone': user.phone}
    return jsonify(user_data)


# Method: GET
# Description: This endpoint retrieves all users from the database and returns them in a list of JSON objects.
# Response: A list of user objects. Each object contains id, name, and phone.
@endpoint.route('/users', methods=['GET'])
def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({'id': user.id, 'username': user.username, 'password': user.password})

    if not users_list:
        return make_response(jsonify({'message': 'empty'}))

    return jsonify(users_list)


# Method: POST
# Description: This endpoint adds a new user to the database. It checks if the user already exists before adding.
# Request: JSON object containing name and phone.
# Response: A message indicating whether the user was added successfully or not.
@endpoint.route('/user', methods=['POST'])
@cross_origin(supports_credentials=True)
def register_user():
    try:
        # get json data from body
        data = request.get_json()

        # check if user exists on the database
        user = User.query.filter_by(username=data['username']).first()
        if user is not None:
            return make_response(jsonify({'message': 'user already exists'}), 409)

        # assign new user values
        new_username = data['username']
        new_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=new_username, password=new_password)

        # commit to database then return 201
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user registered'}), 201)

    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'error adding user'}), 500)


@endpoint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # check if user exists on the database
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"message": "user does not exist"}), 404

    # check is credentials are correct
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # if correct, provide JWT
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"message": "invalid credentials"}), 401


# Method: DELETE
# Description: This endpoint deletes a user from the database based on the provided user ID.
# Request: User ID in the URL.
# Response: A message indicating whether the user was deleted successfully or not.
@endpoint.route('/user/<int:user_id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify({'message': 'user not found'}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'user deleted'}), 200)
    except Exception:
        return make_response(jsonify({'message': 'error deleting user'}), 500)


# Method: PUT
# Description: This endpoint updates a user's details in the database based on the provided user ID.
# Request: User ID in the URL and a JSON object containing name and phone.
# Response: A message indicating whether the user was updated successfully or not.

# TODO: turn this into note, i am upgrading user crud to note crud
@endpoint.route('/user/<int:user_id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return make_response((jsonify({'message': 'user not found'})), 404)
        # get updated data from json body
        updated_data = request.get_json()
        user.name = updated_data['name']
        user.phone = updated_data['phone']
        db.session.add(user)
        db.session.commit()
        return make_response((jsonify({'message': 'user updated'})), 201)

    except Exception:
        return make_response(jsonify({'message': 'error updating user'}), 500)


@endpoint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@endpoint.route('/redis-test', methods=['GET'])
def redis_test():
    from redis import Redis
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    redis.set(
        'test', 'Hello Redis!'
    )
    value = redis.get('test').decode('utf-8')
    return jsonify({'message': value,
                    'key': 'test'})
