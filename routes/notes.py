from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers import token_in_blacklist
from models import User, db, Note
from sqlalchemy.exc import SQLAlchemyError

notes_endpoint = Blueprint('notes', __name__)


@notes_endpoint.route("/note", methods=["POST"])
@cross_origin(supports_credentials=True)
@jwt_required()
def add_note():
    # get client's username from token claims
    current_user = get_jwt_identity()['username']

    # get jti from token claims
    jti = get_jwt_identity()['jti']

    # check if token is in redis
    if token_in_blacklist(jti):
        return jsonify({"message": "you are logged out!"}), 401

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


# TODO:
@notes_endpoint.route("/note/<int:note_id>", methods=['PUT'])
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

    except SQLAlchemyError:
        return make_response(jsonify({'message': 'error updating note'}), 500)


# shows users notes based on username
@notes_endpoint.route('/notes', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def show_notes():
    try:
        # get username from claims
        current_user = get_jwt_identity()['username']

        # get jti from token claims
        jti = get_jwt_identity()['jti']

        # check if token is in redis
        if token_in_blacklist(jti):
            return jsonify({"message": "you are logged out!"}), 401

        # get user id by username
        user_query = User.query.filter_by(username=current_user).first()
        if user_query is None:
            return None
        user_id = user_query.id
        user_notes = Note.query.filter_by(user_id=user_id)

        # if user is empty
        if user_notes is None:
            return jsonify({"message": "User does not exist"}), 404

        # return list of notes
        users_notes = []
        for note in user_notes:
            users_notes.append({'id': note.id, 'title': note.title, 'content': note.content})

        # if user does not have notes
        if users_notes is None:
            return make_response(jsonify({'message': 'you dont have notes'}), 404)

        return jsonify(users_notes)

    except SQLAlchemyError:
        return make_response(jsonify({'message': 'Error showing notes'}), 500)
