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


WTF_CSRF_SECRET_KEY = "CSRFSECRET"

auth = Blueprint("auth", __name__)
auth.secret_key = "SECRETKEY"


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    
    if form.is_submitted():
        if not form.validate():
            
            flash("Validation Error")
            return render_template("login.html", form=form, title='Login')
    
    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            # TODO implement flash
            flash("Please check your login details and try again.")
            return render_template("login.html", form=form, title='Login')

        login_user(user, remember=remember)

        return redirect(url_for("main.index"))

    return render_template("login.html", form=form, title='Login')


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    form = SignUp()

    if form.validate_on_submit():

        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        if form.validate() is False:
            flash("All fields are required.")
            return render_template("signup.html", form=form, title='Sign Up')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return render_template("signup.html", form=form, title='Sign Up')

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form, title='Sign Up')


@auth.route("/logout")
def logout():

    logout_user()
    session.clear()
    return redirect(url_for("main.index"))
