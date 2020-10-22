from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .forms import FlickrSearch
from .model import User, Query
from .wrapper import newSearch
import time
from celery import Celery
from . import celery

main = Blueprint('main', __name__)

main.secret_key = 'SECRETKEY'
WTF_CSRF_SECRET_KEY = 'CSRFSECRET'

@main.route('/')
def index():
	
	return render_template('index.html')

@main.route('/about')
def about():
	
	return render_template('about.html')

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

			# TODO set id from time to random, asign to database as associated
			# self.id?
			task = newSearch.delay(data, user, str(time.time()))
			print(task.state)
			print(task.id)

			# Create and Submit DB Query Entry
			query = Query(task.id, lat= data.get('lat'), lon= data.get('lon'), min_taken= data.get('min_taken'),
				max_taken = data.get('max_taken'), accuracy= data.get('accuracy'), radius= data.get('radius'), 
				radius_unit= data.get('radius_units'), tags= data.get('tags') )
			
			db.session.add(query)
			db.session.commit()
			
			return redirect(f'/status/{task.id}')

	return render_template('search.html', form= form)

@main.route('/status', methods=['GET', 'POST'])
def status_landing():

	# TODO implement status landing
	return render_template('statusSarch.html')


# User interface about status of their task
# TODO NEXT
@main.route('/status/<task_id>')
def status_dash(task_id):



	return render_template('status.html', task_id = task_id)


@main.route('/info/<task_id>', methods=['GET'])
def status_endpoint(task_id):
	task = newSearch.AsyncResult(task_id)
	print(task.state)
	
	# recode this
	# used from example

	if task.state == 'PENDING':
		# job did not start yet
		response = {
		'state': task.state,
		'current': 0,
		'total': 1,
		'status': 'Pending...'
		}
	elif task.state != 'FAILURE':
		response = {
		'state': task.state,
		'current': task.info.get('current', 0),
		'total': task.info.get('total', 1),
		'status': task.info.get('status', '')
		}
		if 'result' in task.info:
			response['result'] = task.info['result']
	else:
		# wrong
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info),  # this is the exception raised
		}
	return jsonify(response)
	


# TODO adjust and implement
@main.errorhandler(404)
def page_not_found(error):

   return render_template('404.html', title = '404'), 404