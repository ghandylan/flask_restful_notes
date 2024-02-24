import os
import uuid

import bcrypt
from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import User, db, Note
from redis import Redis

endpoint = Blueprint('endpoints', __name__)


# Method: GET
# Description: This endpoint returns a simple greeting message in JSON format.
# Response: {'message': 'Hello World'}
@endpoint.route('/')
def index():
    return jsonify({'message': 'Hello World'})


# GET USER'S ID BY SUPPLYING USERNAME in path
@endpoint.route('/user/<string:username>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_user_id(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response(jsonify({'message': 'user not found'}), 404)
    return jsonify({'id': user.id})


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
        identity = {"username": user.username, "jti": str(uuid.uuid4())}
        # store username in claims for token
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)

    return jsonify({"message": "invalid credentials"}), 401


@endpoint.route("/logout", methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def logout():
    jti = get_jwt_identity()['jti']
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    redis.set(jti, '', ex=60 * 60 * 24)
    return jsonify({"message": "Successfully logged out"})


@endpoint.route("/note", methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def add_note():
    # get client's username from token claims
    current_user = get_jwt_identity()['username']

    # get jti from token claims
    jti = get_jwt_identity()['jti']

    # check if token is in redis
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    if redis.get(jti) is not None:
        return jsonify({"message": "You are logged out. Please log in again."}), 401

    # get json data from body
    title = request.json.get("title")
    content = request.json.get("content")

    # check if user exists on the database
    user = User.query.filter_by(username=current_user).first()
    if user is None:
        return jsonify({"message": "user does not exist"}), 404

    # if user exists, get user id from the database
    user_id = user.id

    # add note to the database
    new_note = Note(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "note added"}), 201


@endpoint.route("/note/<int:note_id>", methods=['PUT'])
@cross_origin(supports_credentials=True)
@jwt_required()
def edit_note(note_id):
    try:
        note = Note.query.get(note_id)
        if note is None:
            return make_response(jsonify({'message': 'note not found'}), 404)

        # get current user from jwt claims
        current_user = get_jwt_identity()

        # check if user exists on the database by passing in claims
        user = User.query.filter_by(username=current_user).first()
        if user is None:
            return make_response(jsonify({'message': 'user not found'}), 404)

        # prepare note for update
        note.title = request.json.get("title")
        note.content = request.json.get("content")
        # get user_id for note ownership
        note.user_id = user.id

        # commit to database
        db.session.add(note)
        db.session.commit()

        return make_response(jsonify({'message': 'note updated'}), 200)

    except Exception:
        return make_response(jsonify({'message': 'error updating note'}), 500)


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
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    redis.set(
        'test', 'Hello Redis!'
    )
    value = redis.get('test').decode('utf-8')
    return jsonify({'message': value,
                    'key': 'test'})
