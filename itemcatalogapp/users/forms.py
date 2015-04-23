
from wtforms import TextField, validators

from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [validators.Required()])
    last_name = TextField('Last Name', [validators.Required()])

