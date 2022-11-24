import os

from flask import Flask
from schema import *

# Configure application
app = Flask(__name__)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{username}${databasename}".format(
    username="",
    password="",
    hostname="",
    databasename=""
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    """Creates the database"""
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    """Run this file on creation of new database"""
    with app.app_context():
        main()