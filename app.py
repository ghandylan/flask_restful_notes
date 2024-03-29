import config
import redis
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from routes import user, notes, test


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

    # register the routes
    app.register_blueprint(user.user_endpoint)
    app.register_blueprint(notes.notes_endpoint)
    app.register_blueprint(test.test_endpoint)
    return app


app_instance = create_app()

if __name__ == '__main__':
    app_instance.run()
