from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, RadioField, IntegerField, HiddenField, BooleanField, FormField, SelectField, TextAreaField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from wtforms.form import BaseForm, Form
from wtforms import validators, ValidationError, widgets

# TODO adjust imports for proj


WTF_CSRF_SECRET_KEY = 'CSRFSTRING' # Todo pull from env 



class LoginForm(FlaskForm):
	
	email = TextField("Email", validators=[InputRequired("Please enter your email"), Email("Please enter an email")])
	password = PasswordField("Password", validators=[DataRequired("Enter your password")])
	submit = SubmitField("Login")

class SignUp(FlaskForm):
	
	name = TextField("Name", validators=[InputRequired(message = "Please enter your name")])
	email = TextField("Email", validators=[InputRequired(message = "Please enter your email"), Email("Please enter an email")])
	password = PasswordField("Password", validators=[InputRequired(message = "Enter your password"), Length(min = 4, message = "Minimum password length 4")])
	password_confirm = PasswordField("Password Confirm", validators=[InputRequired(message = "Enter your password"), EqualTo('password', message = "Passwords must match")])
	submit = SubmitField("Sign Up")



class FlickrSearch(FlaskForm):
	"""
	min lat
	min long
	max lat
	max long
	"""
	# radius search
	lat = DecimalField('Latitude', places= 5, rounding= None)
	lon = DecimalField('Longitude', places= 5, rounding= None)
	radius = IntegerField('Radius')
	radius_units = SelectField('Radius Units', choices= [ ('km', 'KM'), ('mi', 'MI') ])

	tags = StringField('Search Tags', validators=[Length(max= 50, message= 'Maximum tag length reached')])
	min_taken = DateField('Minimum Date Taken', format='%Y-%m-%d')
	max_taken = DateField('Maximum Date Taken', format='%Y-%m-%d')
	accuracy = IntegerField('Accuracy', validators=[Length(max= 16, min= 1, message='Accuracy is defined from 1 - 16')])
	search = SubmitField('Execute Search')