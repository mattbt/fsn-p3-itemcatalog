from functools import wraps
from flask import g, request, redirect, url_for

from users.views import login_session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('usersbp.showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function