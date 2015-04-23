from functools import wraps
from flask import g, request, redirect, url_for

from flask.ext.login import current_user

from users.views import login_session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('usersbp.showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# not working
import dbhelper
from flask import flash
	
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print roles
            if get_current_user_role() not in roles:
                flash('No authorization to view the requested page')
		return redirect(url_for('itemcatalogbp.catalog', next=request.url))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
	
def get_current_user_role():
	roles = dbhelper.getRolesFromUserID(current_user.id)
	print [role.name for role in roles]
	return (role.name for role in roles)
