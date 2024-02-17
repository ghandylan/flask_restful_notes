from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))


class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    # owner of note
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
