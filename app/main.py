from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .forms import FlickrSearch
from .model import User, Query
from .wrapper import newSearch
from .utilities import create_unique_id
import time
from celery import Celery
from . import celery
from datetime import datetime

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
			
			#user = current_user.id
			user = 'test_user_2' # for testing only
			task_time = str(time.time())
			friendly_id = create_unique_id()

			# Async Task Register
			task = newSearch.delay(data, user, task_time)

			print(task.state)
			print(task.id)

			# Create and Submit DB Query Entry
			query = Query(id= str(task.id), user_id= user, friendly_id= friendly_id , execution_time= task_time,
				lat= data.get('lat'), lon= data.get('lon'), min_taken= data.get('min_taken'),
				max_taken = data.get('max_taken'), accuracy= data.get('accuracy'), radius= data.get('radius'), 
				radius_units= data.get('radius_units'), tags= data.get('tags'))
			
			db.session.add(query)
			db.session.commit()
			
			return redirect(f'/results/{friendly_id}')

	return render_template('search.html', form= form)

@main.route('/status', methods=['GET', 'POST'])
def status_landing():

	# TODO implement input page for manual status search w/ friendly id
	return render_template('status.html')


# User interface about status of their task
# TODO
@main.route('/results/<task_id>')
def status_dash(task_id):

	task = Query.query.filter_by(friendly_id= task_id).first()
	started = datetime.fromtimestamp(task.execution_time).strftime('%Y-%m-%d %H:%M')

	return render_template('results_testing.html', task_id = task_id, task=task, started=started)


@main.route('/info/<task_id>', methods=['GET'])
def status_endpoint(task_id):

	friendly = Query.query.filter_by(friendly_id= task_id).first()

	task = newSearch.AsyncResult(friendly.id)
	print(task.state)
	

	if task.state == 'PENDING':
		response = {
		'state': task.state,
		'current': 'waiting',
		'total': 'waiting',
		'status': 'waiting'
		}
	elif task.state != 'FAILURE':
		response = {
		'state': task.state,
		'current': task.info.get('current'),
		'total': task.info.get('total'),
		'status': task.info.get('status')
		}
		
	else:
		# wrong
		response = {
			'state': task.state,
			'current': 1,
			'total': 1,
			'status': str(task.info), 
		}
	return jsonify(response)
	


# TODO adjust and implement
@main.errorhandler(404)
def page_not_found(error):

   return render_template('404.html', title = '404'), 404