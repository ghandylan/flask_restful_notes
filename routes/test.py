import os

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from redis import Redis

test_endpoint = Blueprint('test', __name__)


@test_endpoint.route('/')
def index():
    return jsonify({'message': 'Hello World'})


@test_endpoint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@test_endpoint.route('/redis-test', methods=['GET'])
def redis_test():
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    redis.set(
        'test', 'Hello Redis!'
    )
    value = redis.get('test').decode('utf-8')
    return jsonify({'message': value,
                    'key': 'test'})
