from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import db
from .forms import FlickrSearch
from .model import User

main = Blueprint('main', __name__)

main.secret_key = 'SECRETKEY'
WTF_CSRF_SECRET_KEY = 'CSRFSECRET'



@main.route('/home')
def index():
	return render_template('home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():

	form = FlickrSearch()

	if form.is_submitted():

		if form.validate() == False:
			print('Failed Validation')
			flash('Failed Validation')
			return redirect(url_for('main.search'))

		else:
			data = request.form
			if 'lat' in data:
				lat = data['lat']
				print(lat)
			else:
				print('no')
		

	return render_template('search.html', form= form)

# TODO adjust and implement
@main.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


""""
@main.route('/search')
TODO: ADD PARAM
def search():
	return search results


"""