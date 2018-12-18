from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BaseMetal, Alloy, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Alloy Catalog App"


# Connect to Database and create database session
engine = create_engine('sqlite:///metalcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view serializad Basemetal and Alloy Information
@app.route('/basemetals/JSON')
def basemetalsJSON():
    basemetals = session.query(BaseMetal).all()
    return jsonify(basemetals=[i.serialize for i in basemetals])


@app.route('/basemetal/<int:basemetal_id>/JSON')
def alloyJSON(basemetal_id):
    basemetal = session.query(BaseMetal).filter_by(id=basemetal_id).one()
    alloy = session.query(Alloy).filter_by(basemetal_id=basemetal_id).all()
    return jsonify(Alloy_Item=[i.serialize for i in alloy])


# Show all base metals
@app.route('/')
@app.route('/basemetals/')
def showBaseMetals():
    basemetals = session.query(BaseMetal).order_by(asc(BaseMetal.name))
    if 'username' not in login_session:
        return render_template('publicBaseMetals.html', basemetals=basemetals)
    else:
        return render_template('baseMetals.html', basemetals=basemetals)


# Create a new base metal
@app.route('/basemetal/new', methods=['GET', 'POST'])
def newBaseMetal():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBaseMetal = BaseMetal(name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(newBaseMetal)
        flash('New Base Metal %s Successfully Created' % newBaseMetal.name)
        session.commit()
        return redirect(url_for('showBaseMetals'))
    else:
        return render_template('newBaseMetal.html')


# Edit a base metal
@app.route('/basemetal/<int:basemetal_id>/edit', methods=['GET', 'POST'])
def editBaseMetal(basemetal_id):
    editedBaseMetal = session.query(BaseMetal).filter_by(id=basemetal_id).one()
    if editedBaseMetal.user_id != login_session['user_id']:
        flash('Not allowed - Please create your own basemetal to edit')
        return redirect(url_for('showBaseMetals'))
    if request.method == 'POST':
        if request.form['name']:
            editedBaseMetal.name = request.form['name']
            flash('Base Metal Successfully Edited %s' % editedBaseMetal.name)
            return redirect(url_for('showBaseMetals'))
    else:
        return render_template('editBaseMetal.html', basemetal=editedBaseMetal)


# Delete a base metal
@app.route('/basemetal/<int:basemetal_id>/delete', methods=['GET', 'POST'])
def deleteBaseMetal(basemetal_id):
    baseMetalToDelete = session.query(BaseMetal).filter_by(
        id=basemetal_id).one()
    if baseMetalToDelete.user_id != login_session['user_id']:
        flash('Not allowed - Please create your own basemetal to delete')
        return redirect(url_for('showBaseMetals'))
    if request.method == 'POST':
        session.delete(baseMetalToDelete)
        flash('%s Successfully Deleted' % baseMetalToDelete.name)
        session.commit()
        return redirect(url_for('showBaseMetals'))
    else:
        return render_template(
            'deleteBaseMetal.html', basemetal=baseMetalToDelete)


# Show an alloy
@app.route('/basemetal/<int:basemetal_id>/')
@app.route('/basemetal/<int:basemetal_id>/alloy')
def showAlloy(basemetal_id):
    basemetal = session.query(BaseMetal).filter_by(id=basemetal_id).one()
    alloy = session.query(Alloy).filter_by(basemetal_id=basemetal_id).all()
    if 'username' not in login_session:
        return render_template(
            'publicAlloys.html', basemetal=basemetal, alloy=alloy)
    else:
        return render_template('alloys.html', basemetal=basemetal, alloy=alloy)


# Create a new alloy
@app.route('/basemetal/<int:basemetal_id>/alloy/new', methods=['GET', 'POST'])
def newAlloy(basemetal_id):
    basemetal = session.query(BaseMetal).filter_by(id=basemetal.id).one()
    if request.method == 'POST':
        newItem = Alloy(name=request.form['name'],
                        description=request.form['descrption'],
                        basemetal_id=basemetal_id, user_id=basemetal.user_id)
        session.add(newItem)
        session.commit()
        flash('New Alloy %s Successfully Created' % (newItem.name))
        return redirect(url_for('showAlloy', basemetal_id=basemetal_id))
    else:
        return render_template('newAlloy.html', basemetal_id=basemetal_id)


# Edit an alloy
@app.route('/basemetal/<int:basemetal_id>/alloy/<int:alloy_id>/edit',
           methods=['GET', 'POST'])
def editAlloy(basemetal_id, alloy_id):
    editedItem = session.query(Alloy).filter_by(id=alloy_id).one()
    basemetal = session.query(BaseMetal).filter_by(id=basemetal_id).one()
    if editedItem.user_id != login_session['user_id']:
        flash('Not allowed - Please create your own alloy to edit')
        return redirect(url_for('showBaseMetals'))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Alloy Successfully Edited')
        return redirect(url_for('showAlloy', basemetal_id=basemetal_id))
    else:
        return render_template('editAlloy.html', basemetal=basemetal,
                               basemetal_id=basemetal_id, alloy_id=alloy_id,
                               alloy=editedItem)


# Delete an alloy
@app.route('/basemetal/<int:basemetal_id>/alloy/<int:alloy_id>/delete',
           methods=['GET', 'POST'])
def deleteAlloy(basemetal_id, alloy_id):
    basemetal = session.query(BaseMetal).filter_by(id=basemetal_id).one()
    itemToDelete = session.query(Alloy).filter_by(id=alloy_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        flash('Not allowed - Please create your own alloy to delete')
        return redirect(url_for('showBaseMetals'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Alloy Successfully Deleted')
        return redirect(url_for('showAlloy', basemetal_id=basemetal_id))
    else:
        return render_template('deleteAlloy.html', basemetal=basemetal,
                               basemetal_id=basemetal_id, alloy=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    gdisconnect()
    flash("You have successfully been logged out.")
    basemetals = session.query(BaseMetal).order_by(asc(BaseMetal.name))
    return render_template('publicBaseMetals.html', basemetals=basemetals)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
