from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, RadioField, IntegerField, HiddenField, BooleanField, FormField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from wtforms.form import BaseForm, Form
from wtforms import validators, ValidationError, widgets

# TODO adjust imports for proj


WTF_CSRF_SECRET_KEY = 'CSRF STRING' # Todo pull from env 



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