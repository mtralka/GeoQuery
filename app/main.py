from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import db
# from .forms import MY FORMS
from .model import User


main = Blueprint('main', __name__)

main.secret_key = 'SECRET KEY'
WTF_CSRF_SECRET_KEY = 'CSRF SECRET'


@main.route('/')
def index():
	return render_template('index.html')



""""
@main.route('/search')
TODO: ADD PARAM
def search():
	return search results


"""