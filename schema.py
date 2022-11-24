from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class users(db.Model):
    """Creates table recording users and their info"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(20), nullable=False, index=True)
    hash = db.Column(db.String(102), nullable=False)

    # Adds user to the database
    def add_user(name, password):
        user = users(username=name, hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    # Gets the object from its username
    def getby_name(name):
        return users.query.filter_by(username = name).first()

    # Gets the object from its id
    def getby_id(user_id):
        return users.query.get(user_id)

    # Gets username from user_id
    def get_username(user_id):
        return users.query.get(user_id).username

    # Gets all users except for the given user id
    def get_notid(not_id):
        return users.query.filter(users.id != not_id).all()

    def get_like_notid(not_id, like):
        return users.query.filter(users.id != not_id, users.username.like("%"+like+"%")).all()

    # Checks hash of the password with given password
    def check_hash(self, password):
        return check_password_hash(self.hash, password)

    # Change has of password for user
    def change_hash(self, password):
        self.hash = generate_password_hash(password)
        db.session.commit()


class dm(db.Model):
    """Creates table recording direct messages and their info"""

    __tablename__ = "dm"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(5000), nullable=False)
    message_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def add_dm(sender_id, reader_id, message):
        message = dm(sender_id = sender_id, reader_id = reader_id, message = message)
        db.session.add(message)
        db.session.commit()

    # Gets dm between sender and reader
    def get_dm(dm_sender_id, dm_reader_id):
        message = db.session.query(
            users.username.label("name"), dm.message.label("message")
        ).filter(
            users.id == dm.sender_id
        ).filter(
            (
                ((dm.sender_id == dm_sender_id) & (dm.reader_id == dm_reader_id)) |
                ((dm.sender_id == dm_reader_id) & (dm.reader_id == dm_sender_id))
            )
        ).all()
        return message