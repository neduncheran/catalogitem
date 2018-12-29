#!/usr/bin/python2
#
# Sport Catalog project
#
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem, User
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
APPLICATION_NAME = "SportsCatalog Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///sportscatalog.db')
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


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    print("hi")
    print(request.args.get('state'))
    print(login_session['state'])
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&'
           'client_secret=%s&fb_exchange_token=%s' % (
                app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
    Due to the formatting for the result
    from the server token exchange we have to
    split the token first on commas and
    select the first index which gives us the key : value
    for the server access token then we
    split it on colons to pull out the actual token value
    and replace the remaining quotes with
    nothing so that it can be used directly in the graph
    api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?'
           'access_token=%s&fields=name,id,email' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = ('https://graph.facebook.com/v2.8/me/picture?'
           'access_token=%s&redirect=0&height=200&width=200' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;" '
    output += ' " height: 300px;border-radius: 150px;" '
    output += ' "-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/'
           '%s/permissions?access_token=%s' % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print("cool")
    print(request.args.get('state'))
    print(login_session['state'])
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization  code into a credentials object
        print("oauth_flow")
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        print("oauth_flow")
        print(oauth_flow)
        oauth_flow.redirect_uri = 'postmessage'
        print("cool11111111119191")
        print("cool11111111119191wwww")
        print(code)
        print("cool11111111119191tt")
        credentials = oauth_flow.step2_exchange(code)
        print("cool111111111159999")
        print(credentials)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print(response)
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
        print("cool11111111113")
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
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    print("cool1111111111")
    print(user_id)
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;" '
    output += ' " height: 300px;border-radius: 150px;" '
    output += ' "-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions

# get the user from user table
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
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
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all sportscatalog
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    catalogItems = session.query(
        CatalogItem).order_by(CatalogItem.id.desc()).limit(10)
    print(catalogs)
    if 'username' not in login_session:
        return render_template('publiccatalog.html',
                               catalogs=catalogs, catalogItems=catalogItems)
    else:
        return render_template('catalogs.html',
                               catalogs=catalogs, catalogItems=catalogItems)

# create new catalog ITEM


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalogItem = CatalogItem(
            title=request.form['title'],
            description=request.form['description'],
            catalog_id=request.form['comp_select'],
            user_id=login_session['user_id'])
        catalog = session.query(
            Catalog).filter_by(id=newCatalogItem.catalog_id).one()
        print(catalog.name)
        newCatalogItem.category = catalog.name
        session.add(newCatalogItem)
        flash('New CatalogItem %s Successfully Created' % newCatalogItem.title)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        catalogs = session.query(Catalog).order_by(asc(Catalog.name))
        return render_template('newCatalog.html', catalogs=catalogs)

# @app.route('/catalog/<string:name>/')


@app.route('/catalog/<string:name>/items/')
def showCatalogItem(name):
    catalogs = session.query(
        Catalog).order_by(asc(Catalog.name))
    catalog = session.query(Catalog).filter_by(name=name).one()
    creator = getUserInfo(catalog.user_id)
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog.id).all()
    itemsize = len(items)
    if itemsize == 0:
        flash("No recorder founded")
    return render_template('publiccatalogitems.html',
                           items=items, catalog=catalog,
                           creator=creator, itemsize=itemsize,
                           catalogs=catalogs)


# view the description
@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def viewDescription(catalog_name, item_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    creator = getUserInfo(catalog.user_id)
    itemDescription = session.query(CatalogItem).filter_by(
        title=item_name, category=catalog_name).one()
    print('log session id\n')

    print('creator id\n')
    print(creator.id)
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template('viewdescription.html',
                               catalog=catalog, creator=creator,
                               itemDescription=itemDescription)
    else:
        return render_template('viewdescriptionloginuser.html',
                               catalog=catalog, creator=creator,
                               itemDescription=itemDescription)


@app.route('/catalog.json')
def catalogJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


# Disconnect based on provider


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))

# edit option for log in user and view only normal user


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editCatalogItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    editCatlogItem = session.query(
        CatalogItem).filter_by(title=item_name).one()
    allCatalogs = session.query(
        Catalog).order_by(asc(Catalog.name))
    currentCatalog = session.query(
        Catalog).filter_by(id=editCatlogItem.catalog_id).one()
    print(currentCatalog.name)
    if login_session['user_id'] != currentCatalog.user_id:
        output = "<script>function myFunction() "
        output += "{alert('You are not authorized');}"
        output += "</script><body onload='myFunction()'>"
        return output
    if request.method == 'POST':
        if request.form['title']:
            editCatlogItem.title = request.form['title']
        if request.form['description']:
            editCatlogItem.description = request.form['description']
        if request.form['comp_select']:
            editCatlogItem.catalog_id = request.form['comp_select']
            print(editCatlogItem.catalog_id)
            editedcurrentCatalog = session.query(
                Catalog).filter_by(id=editCatlogItem.catalog_id).one()
            editCatlogItem.category = editedcurrentCatalog.name

        session.add(editCatlogItem)
        session.commit()
        flash('Catalog Item Successfully Edited')
        return redirect(url_for('viewDescription',
                                catalog_name=editedcurrentCatalog.name,
                                item_name=editCatlogItem.title))
    else:
        return render_template('editcatalogitem.html',
                               currentCatalog=currentCatalog,
                               allCatalogs=allCatalogs, item=editCatlogItem)

# option for log in user


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteCatalogItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(
        CatalogItem).filter_by(title=item_name).one()
    catalog = session.query(
        Catalog).filter_by(id=itemToDelete.catalog_id).one()
    if login_session['user_id'] != catalog.user_id:
        output = "<script>function myFunction()"
        output += "{alert('You are not authorized to delete CatalogItem');}"
        output += "</script><body onload='myFunction()'>"
        return output
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Catalog Item Successfully Deleted')
        return redirect(url_for('showCatalogItem', name=catalog.name))
    else:
        return render_template('deletecatalogitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
