import os

from flask import Flask
from schema import *

# Configure application
app = Flask(__name__)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)),"dms.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    """Creates the database"""
    db.create_all()

if __name__ == "__main__":
    """Run this file on creation of new database"""
    with app.app_context():
        main()