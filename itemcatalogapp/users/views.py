import datetime, random, string
from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import desc

# Blueprint declaration
usersbp = Blueprint("usersbp", __name__)

# Session
from flask import session as login_session
# Flask-Login
from flask.ext.login import login_user, logout_user, current_user

# myAuth
from werkzeug import generate_password_hash

# oauth2 authorization flow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError, OAuth2Credentials
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('itemcatalogapp/users/client_secrets.json','r').read())['web']['client_id']

# Import classes and dbhelper
from models import User
from .. import dbhelper

# Import session data
from .forms import RegisterForm, LoginForm



################
# Sign Up ######
################

@usersbp.route('/signup')
def showSignUp():
    register_form = RegisterForm()
    return render_template('register.html', register_form = register_form)

@usersbp.route('/register', methods=['POST'])
def myRegister():
    
    # create Sign Up Form
    form = RegisterForm()
    
    # if POST request
    if form.validate_on_submit():
        try:
            # check if user email already in DB - if yes, redirect to Login page
            user = dbhelper.getUserFromEmail(form.email.data)
            flash('user email already in db, please login')
            return redirect(url_for('usersbp.showLogin'))   
        
        # should I use something different from try..catch here?
        except:
            # if user email not already in db
            # create user and insert in DB
            user = User()
            user.password = generate_password_hash(form.pwd.data)
            print user.password
            form.populate_obj(user)
    
            dbhelper.addUser(user)
            
            
            # populate session
            '''login_session['provider'] = 'myauth'
            login_session['username'] = user.name
            login_session['email'] = user.email
            login_session['user_id'] = getUserID(login_session['email'])
            login_session['picture'] = user.picture'''
            login_user(user)
            return redirect(url_for('itemcatalogbp.catalog'))
    else:
        
        # if GET request or invalid POST request, simply render page
        flash(form.errors)
        return redirect(url_for('usersbp.showLogin'))   




################
# Sign In ######
################

# Create a state token to prevent request forgery
# Store it in the session for later validation
@usersbp.route('/login')
def showLogin():
    print('here')
    login_form = LoginForm()
    STATE = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = STATE
    return render_template('login.html', STATE = login_session['state'], login_form = login_form)


# G+ SignIn ####
@usersbp.route('/gconnect', methods=['POST'])
def gconnect():
    # token match: user is making request, not a malicious script
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    code = request.data
    try:
        # Upgrade the authorization code into  a credentials object
        oauth_flow = flow_from_clientsecrets('itemcatalogapp/users/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    # if there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user id doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client id doesn't match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Store the access token in the session for later use
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id
    
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params = params)
    data = json.loads(answer.text)
    
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    
    # Check if user exists in db, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    
    output = '<h1>Welcome, %s!</h1>' % login_session['username']
    output += '<img src="%s" style="width:300px; height:300px; border-radius:150px; -webkit-border-radius:150px; -moz-border-radius:150px;"></img>' % login_session['picture']
    #flash("you are now logged in as %s" % login_session['username'])
    return output
    

# FB SignIn ####
@usersbp.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    
    # Exchange short-lived token with long-lived server-side token
    app_id = json.loads(open('itemcatalogapp/users/fb_client_secrets.json','r').read())['web']['app_id']
    app_secret = json.loads(open('itemcatalogapp/users/fb_client_secrets.json','r').read())['web']['app_secret']
    
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    
    # use token to get info from API
    userinfo_url = 'https://graph.facebook.com/v2.3/me'
    # strip expire tag from the access token
    token = result.split('&')[0]
    
    url = 'https://graph.facebook.com/v2.3/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    
    # get user picture
    url = 'https://graph.facebook.com/%s/picture?%s&redirect=0&height=200&width=200' % (login_session['facebook_id'], token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    resultdata = json.loads(result)
    login_session['picture'] = resultdata["data"]["url"]

    # Check if user exists in db, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    
    output = '<h1>Welcome, %s!</h1>' % login_session['username']
    output += '<img src="%s" style="width:300px; height:300px; border-radius:150px; -webkit-border-radius:150px; -moz-border-radius:150px;"></img>' % login_session['picture']
    #flash("you are now logged in as %s" % login_session['username'])
    return output


# myAuth - SignIn ######
@usersbp.route('/login', methods=['POST'])
def myLogin():
    
    # create Form
    form = LoginForm()
    ## print(form.email.data)
    
    # if POST request
    if form.validate_on_submit():   
        try:
            # check if user email in DB
            user = dbhelper.getUserFromEmail(form.email.data)
        except:
            
            # if user email not in DB, alert user
            flash('email not found')
            return redirect(url_for('usersbp.showLogin'))
        
        # if user email in db:
        # if password is empty, user previously logged in with oAuth - alert user to log in again with oAuth
        if user.password is None:
            flash('user already in db but previously logged with oAuth, please login with oAuth')
            return redirect(url_for('usersbp.showLogin'))
        
        # else if password is not empty, check for match
        if user.check_password(form.password.data): 
            
            # if password correct, set login_session
            '''login_session['provider'] = 'myauth'
            login_session['username'] = user.name
            login_session['email'] = user.email
            login_session['user_id'] = getUserID(login_session['email'])
            login_session['picture'] = user.picture'''
            login_user(user)
            return redirect(url_for('itemcatalogbp.catalog'))
        else:
            
            # if password not correct, alert user
            flash('incorrect password')
            return redirect(url_for('usersbp.showLogin'))
            
    # if GET request or invalid POST request, simply render page
    flash('Login data not correct')
    return redirect(url_for('usersbp.showLogin'))



#################
# disconnect ####
#################

@usersbp.route('/disconnect')
def disconnect():
   

    # Only disconnect a connected user
    if not current_user.is_authenticated():
        flash("No user connected")
        return redirect(url_for('itemcatalogbp.catalog'))
       
    # disconnect from google / facebook oAuth
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['credentials']
            del login_session['gplus_id']
        elif login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
    
    # Flask-login clean session
    logout_user()
	
    #flash("You have successfully been logged out")
    return redirect(url_for('itemcatalogbp.catalog'))

def fbdisconnect():
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

def gdisconnect():  
    # Fetch credentials from session
    credential_json = login_session.get('credentials')
    
    if credential_json is None:
        response = make_response(json.dumps("Failed to fetch credentials"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    credentials = OAuth2Credentials.from_json(credential_json)
    # Execute HTTP GET request to revoke current token
    access_token = credentials.access_token
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
    h = httplib2.Http()
    
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Token revoked.
        response = make_response(json.dumps("Successfully disconnected"), 200)
        response.headers['Content-Type'] = 'application/json'
        print("Token revoked ")
        return redirect(url_for('itemcatalogbp.catalog'))
    else:
        # For whatever reason, the given token was invalid (Could have already been revoked)
        response = make_response(json.dumps("Failed to revoke token for given user"), 401)
        response.headers['Content-Type'] = 'application/json'
        print("Failed to revoke token for given user")
        return redirect(url_for('itemcatalogbp.catalog'))



###############
# helper ######
###############


def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    dbhelper.add(newUser)
    
    user = dbhelper.getUserFromEmail(login_session['email'])
    return user.id
    
def getUserInfo(user_id):
    user = dbhelper.getUserFromID(user_id)
    return user

def getUserID(email):
    try:
        user = dbhelper.getUserFromEmail(email)
        return user.id
    except:
        return None

