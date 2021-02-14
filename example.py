"""
    Onshape Example
    --------------

    Shows how to authorize users with Onshape.

"""
from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string, jsonify
from flask_onshape import Onshape
SECRET_KEY = 'development key'
DEBUG = True

# Set these values
ONSHAPE_CLIENT_ID = 'OTIIDXKUDAAJ4MHV74QMBHBEI32HNOCDYIPE63A='
ONSHAPE_CLIENT_SECRET = 'YAB2WADMORGADLS6ZHLJK7ERGZGEUKNYM5RBHEDZVDSXPX3XA3DA===='

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)

# setup onshape-flask
onshape = Onshape(app)


@app.route('/')
def index():
    return "hello"


@onshape.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.onshape_access_token


@app.route('/onshape-callback')
@onshape.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)
    session["onshape_token"] = access_token
    return redirect(next_url)


@app.route('/login')
def login():
    if session.get('onshape_token', None) is None:
        return onshape.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('onshape_token', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
