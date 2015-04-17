from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, validators

# Register Form
class RegisterForm(Form):
	name = TextField('name', [validators.Required()], description = "Name")
	password = PasswordField('password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')], description = "Password")
	confirm = PasswordField('password', [validators.Required()], description = "Confirm Password")
	email = TextField('email', [validators.Required(), validators.Email()], description = "Email")
	accept_tos = BooleanField('I accept the TOS', [validators.Required()], description = "I accept the TOS")

# Login Form
class LoginForm(Form):
	email = TextField('email', [validators.Required()], description = "Email")
	password = PasswordField('Password', [validators.Required()], description = "Password")
