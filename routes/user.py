import os
import uuid

import bcrypt
from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import User, db
from redis import Redis

user_endpoint = Blueprint('user', __name__)


# GET USER'S ID BY SUPPLYING USERNAME in json body
# def get_user_id_by_username(username):
#     user_query = User.query.filter_by(username=username).first()
#
#     if user_query is None:
#         return None
#     user_id = user_query.id
#
#     return user_id


# GET USER'S ID BY SUPPLYING USERNAME in path
@user_endpoint.route('/user/<string:username>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_user_id(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return make_response(jsonify({'message': 'user not found'}), 404)
    return jsonify({'id': user.id})


# Method: POST
# Description: This endpoint adds a new user to the database. It checks if the user already exists before adding.
# Request: JSON object containing name and phone.
# Response: A message indicating whether the user was added successfully or not.
@user_endpoint.route('/user', methods=['POST'])
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


@user_endpoint.route("/login", methods=["POST"])
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


@user_endpoint.route("/logout", methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def logout():
    jti = get_jwt_identity()['jti']
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    redis.set(jti, '', ex=60 * 60 * 24)
    return jsonify({"message": "Successfully logged out"})


# Method: PUT
# Description: This endpoint updates a user's details in the database based on the provided user ID.
# Request: User ID in the URL and a JSON object containing name and phone.
# Response: A message indicating whether the user was updated successfully or not.

# TODO: turn this into note, i am upgrading user crud to note crud
@user_endpoint.route('/user/<int:user_id>', methods=['PUT'])
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
