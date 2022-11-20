from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String, nullable=False, index=True)
    hash = db.Column(db.Integer, nullable=False)

class dm(db.Model):
    __tablename__ = "dm"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String, nullable=False)
    message_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())