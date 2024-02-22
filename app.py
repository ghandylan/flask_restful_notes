import config
import endpoints
import redis
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db


def create_app():
    # initialize the app
    app = Flask(__name__)
    # cross-origin resource sharing
    CORS(app, origins="http://localhost:4200", supports_credentials=True)
    # read env variables from config.py
    app.config.from_object(config.Config)
    # initialize the database models
    db.init_app(app)
    # migration
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    # json web token integration
    jwt = JWTManager(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        redis_instance = redis.Redis(host=config.Config.REDIS_HOST, port=config.Config.REDIS_PORT)
        entry = redis_instance.get(jti)
        return entry is not None  # if the token is in redis, return True

    # register the endpoints
    app.register_blueprint(endpoints.endpoint)
    return app


app_instance = create_app()

if __name__ == '__main__':
    app_instance.run()
