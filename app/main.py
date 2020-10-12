from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import db
from .forms import FlickrSearch
from .model import User
from .wrapper import newSearch
import time

main = Blueprint('main', __name__)

main.secret_key = 'SECRETKEY'
WTF_CSRF_SECRET_KEY = 'CSRFSECRET'

@main.route('/home')
def index():
	return render_template('home.html')


@main.route('/search', methods=['GET', 'POST'])
def search():

	form = FlickrSearch()

	if form.validate_on_submit():

		if form.validate() == False:
			flash('Failed Validation')
			return redirect(url_for('main.search'))

		else:

			data = request.form
			
			# TODO pull from flask login
			user = 'test_user'

			# TODO Add search to Celery que
			newSearch(data, user, str(time.time()))

			# TODO redirect to waiting page
			flash('Success')
			return redirect(url_for('main.search'))
	
	return render_template('search.html', form= form)



# TODO adjust and implement
@main.errorhandler(404)
def page_not_found(error):

   return render_template('404.html', title = '404'), 404