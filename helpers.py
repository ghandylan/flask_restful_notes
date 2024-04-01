import os

from redis import Redis


def token_in_blacklist(jti):
    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
    # if token exists in blacklist
    if redis.get(jti) is not None:
        return True
