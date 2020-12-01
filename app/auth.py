from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from . import db
from .forms import LoginForm
from .forms import SignUp
from .model import User


WTF_CSRF_SECRET_KEY = "CSRFSTRING"

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        if form.validate() == False:
            flash("All fields are required.")
            return render_template("login.html", form=form)

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return render_template("login.html", form=form)

        login_user(user, remember=remember)

        return redirect(url_for("main.landing"))

    return render_template("login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    form = SignUp()

    if form.validate_on_submit():

        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        if form.validate() == False:
            flash("All fields are required.")
            return render_template("signup.html", form=form)

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return render_template("signup.html", form=form)

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


@auth.route("/logout")
def logout():

    logout_user()
    session.clear()
    return redirect(url_for("main.index"))
