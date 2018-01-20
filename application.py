from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
import time
from models import users, groups

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # ensure username input not blank
        if not request.form.get("username"):
            return render_template("register.html")

        # ensure password not blank
        elif not request.form.get("password"):
            return render_template("register.html")

        # ensure same password filled in again
        if request.form.get("password") != request.form.get("passwordcheck"):
            return render_template("register.html")

            # ensure first name not blank
        if not request.form.get("first_name"):
            return render_template("register.html")

        # ensure last name not blank
        elif not request.form.get("last_name"):
            return render_template("register.html")


        # retrieve user after register
        register = users.User.register(request.form.get("username"),
                                       request.form.get("password"),
                                       request.form.get("first_name"),
                                       request.form.get("last_name"))

        # if username already exists
        if register is None:
            return render_template("register.html")

        # if register successful
        else:

            # log user in
            session["user_id"] = register["user_id"]

            # redirect user to homepage
            return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in. """

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", missing_name = "Username missing")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", missing_pass = "Password missing")

        # retrieve user after login
        login = users.User.login(request.form.get("username"), request.form.get("password"))

        # if login unsuccessful
        if login is None:
            return render_template("login.html", failure = "Login unsuccessful!")

        # if login successful
        else:

            # log user in
            session["user_id"] = login["user_id"]

            # redirect to index
            return redirect(url_for("index"))

    # user reached page via GET
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():

    #TODO
    return render_template("post.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        # if any form blank
        if not request.form.get("current_password"):
            return render_template("settings.html", missingcurrent = "Current password missing")

        if not request.form.get("new_password"):
            return render_template("settings.html", missingnew = "New password missing")

        if not request.form.get("check_password"):
            return render_template("settings.html", missingcheck = "Password check missing")

        # check if new password and password match
        if request.form.get("new_password") != request.form.get("check_password"):
            return render_template("settings.html", nomatch = "Passwords do not match")

        # instantiate user
        user = users.User(session["user_id"])

        # change password
        change = user.change_password(request.form.get("current_password"),
                                      request.form.get("new_password"),
                                      request.form.get("check_password"))

        # if change successful
        if change == True:
            return render_template("settings.html", success= "Password changed!")

        else:
            return render_template("settings.html", failure = "Current password is incorrect!")

    else:
        return render_template("settings.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    #TODO
    return render_template("profile.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":
        if not request.form.get("title"):
            return render_template("create.html", missingtitle = "The title is missing")

        elif not request.form.get("description"):
            return render_template("create.html", missingdesc = "The description is missing")

        description = request.form.get("description")
        title = request.form.get("title")
        group = groups.Group(description, title, session["user_id"])

        create = group.create()
        if create == None:
            return render_template("create.html", missingtitle = "The title already exists")

        return render_template("groupfeed.html")
    else:
        return render_template("create.html")