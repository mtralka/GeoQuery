from flask_login import UserMixin
from . import db

""" Table Depicting Users """
class User(UserMixin, db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))
	queries = db.relationship('Query', backref= 'User', lazy= True) # 1 - M

""" Table Depicting User Queries """
class Query(db.Model):
	__tablename__ = 'Query'
	id = db.Column(db.String(150), primary_key= True) # celery task ID
	execution_time = db.Column(db.Integer, nullable= False) # SQLight has no support for DateTime

	lat = db.Column(db.Float, nullable= False)
	lon = db.Column(db.Float, nullable= False)
	min_taken = db.Column(db.Integer, nullable= True)
	max_taken = db.Column(db.Integer, nullable= True) 
	accuracy = db.Column(db.Integer, nullable= True)




