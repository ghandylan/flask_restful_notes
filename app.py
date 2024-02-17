import config
import endpoints
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
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
    JWTManager(app)
    # register the endpoints
    app.register_blueprint(endpoints.endpoint)
    return app


app_instance = create_app()

if __name__ == '__main__':
    app_instance.run()
