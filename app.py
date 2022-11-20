import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from schema import *

# Configure application
app = Flask(__name__)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)),"dms.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
"""
with app.app_context():
    db.create_all()
"""

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show tasks todo list"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Sends direct message to database
        reader = users.query.filter_by(username = request.args.get("name", type=str)).first()
        dms = dm(sender_id=session.get("user_id"), reader_id = reader.id, message = request.form.get("message"))
        db.session.add(dms)
        db.session.commit()

        # Redirects back to the person being texted
        url = "/?name=" + request.args.get("name", type=str)
        return redirect(url)

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Ensure session is in place
        if session.get("user_id") is None:
            return apology("must have user session in place", 400)

        # Queries all users except the current user and the queries the current user
        names = users.query.filter(users.id != session["user_id"]).all()
        
        myuser = users.query.get(session["user_id"]).username

        if request.args.get("name", type=str) is None:
            return render_template("index.html", users=names, myuser=myuser)
        
        reader = users.query.filter_by(username = request.args.get("name", type=str)).first()

        # Queries all messages from sender and reader
        messages = db.session.query(
            users.username.label("name"), dm.message.label("message")
        ).filter(
            users.id == dm.sender_id
        ).filter(
            (
                ((dm.sender_id == session.get("user_id")) & (dm.reader_id == reader.id)) | 
                ((dm.sender_id == reader.id) & (dm.reader_id == session.get("user_id")))
            )
        ).all()
        
        # Renders the index template with information about users
        return render_template("index.html", users=names, reader=reader, myuser=myuser, messages=messages)


@app.route("/text/<int:id>")
def text(id):
    """Shows the text message interaction between two users"""

    # Queries all messages from sender and reader
    messages = db.session.query(
        users.username.label("name"), dm.message.label("message")
    ).filter(
        users.id == dm.sender_id
    ).filter(
        (
            ((dm.sender_id == session.get("user_id")) & (dm.reader_id == id)) | 
            ((dm.sender_id == id) & (dm.reader_id == session.get("user_id")))
        )
    ).all()
    
    # Renders template with messages
    return render_template("text.html", messages=messages)


@app.route("/usernames")
def usernames():
    """Shows all users"""

    q = request.args.get("q")
    if q:
        # Changes the name for the use of LIKE statement and the executes a query for those users
        names = users.query.filter(users.id != session["user_id"], users.username.like("%"+q+"%")).all()
    else:
        # Queries all users except the current user
        names = users.query.filter(users.id != session["user_id"]).all()
    
    # Renders template with users
    return render_template("users.html", users=names)
        

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        user = users.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Sends user a message that says that the user has logged in
        flash("User logged in")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Sends user a message that says that the user has logged out
    flash("User logged out")

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        if not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Ensure username doesn't exist in table already
        userExists = users.query.filter_by(username=request.form.get("username")).first() is not None
        if userExists:
            return apology("username already exists", 400)

        # Checks whether password and confirmation password match
        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("password and confirmation password do not match", 400)

        # Inserts data into the database
        user = users(username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()

        # Sends user a message stating that the user is registered
        flash("User Registered")

        # Redirect user to index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change user's password."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        if not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)

        # Query database for user
        user = users.query.get(session["user_id"])

        # Ensure user exists and password is correct
        if not check_password_hash(user.hash, request.form.get("old_password")):
            return apology("invalid old password", 400)

        # Checks whether password and confirmation password match
        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("new password and confirmation password do not match", 400)

        # Updates has in the database
        user.hash = generate_password_hash(request.form.get("password"))
        db.session.commit()

        # Sends user a message stating that the user is registered
        flash("Password changed")

        # Redirect user to index page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")

