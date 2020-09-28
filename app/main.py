from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import db
# from .forms import MY FORMS
from .model import User

main = Blueprint('main', __name__)

main.secret_key = 'SECRETKEY'
WTF_CSRF_SECRET_KEY = 'CSRFSECRET'


@main.route('/')
def index():
	return render_template('home.html')



""""
@main.route('/search')
TODO: ADD PARAM
def search():
	return search results


"""