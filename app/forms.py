from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import DecimalField
from wtforms import FormField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import RadioField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import TextField
from wtforms import ValidationError
from wtforms import validators
from wtforms import widgets
from wtforms.fields.html5 import DateField
from wtforms.form import BaseForm
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import Optional


# TODO adjust imports for proj


WTF_CSRF_SECRET_KEY = 'CSRFSTRING' # Todo pull from env 


class LoginForm(FlaskForm):	
	email = TextField("Email", validators=[
		InputRequired("Please enter your email"), Email("Please enter an email")])
	password = PasswordField("Password", validators=[
		DataRequired("Enter your password")])
	submit = SubmitField("Login")


class SignUp(FlaskForm):
	name = TextField("Name", validators=[
		InputRequired(message="Please enter your name")])
	email = TextField("Email", validators=[
		InputRequired(message="Please enter your email"), Email(
			"Please enter an email")])
	password = PasswordField("Password", validators=[
		InputRequired(message="Enter your password"), Length(
			min= 4, message="Minimum password length 4")])
	password_confirm = PasswordField("Password Confirm", validators=[
		InputRequired(message="Enter your password"), EqualTo(
			'password', message="Passwords must match")])
	submit = SubmitField("Sign Up")


class FlickrSearch(FlaskForm):
	 # TODO Adjust messages
	 # TODO Create custom validator check for dates
	"""
	min lat
	min long
	max lat
	max long
	"""
	# radius search
	lat = DecimalField('Latitude', places=5, rounding=None, validators=[
		InputRequired(message='Input Required')])
	lon = DecimalField('Longitude', places=5, rounding=None, validators=[
		InputRequired(message='Input Required')])
	radius = IntegerField('Radius', validators=[Optional()])
	radius_units = SelectField('Radius Units', choices=[('km', 'KM'), ('mi', 'MI')])

	tags = StringField('Search Tags', validators=[
		Length(max=50, message='Maximum tag length reached'), Optional()])
	min_taken_date = DateField(
		'Minimum Date Taken', format='%Y-%m-%d', validators=[Optional()])
	max_taken_date = DateField(
		'Maximum Date Taken', format='%Y-%m-%d', validators=[Optional()])
	accuracy = IntegerField(
		'Accuracy', validators=[NumberRange(
			max=16, min=0, message='Accuracy is defined from 1 - 16'), Optional()])
	search = SubmitField('Execute Search')
