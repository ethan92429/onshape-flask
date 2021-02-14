Onshape-Flask
============

.. module:: flask_onshape

Onshape-Flask is an extension to `Flask`_ that allows you authenticate your
users via Onshape using `OAuth`_ protocol and call `Onshape API`_ methods.

Onshape-Flask depends on the `requests`_ library.

.. _Flask: http://flask.pocoo.org/
.. _OAuth: http://oauth.net/
.. _Onshape API: http://developer.onshape.com/v3/
.. _requests: http://python-requests.org/


Installation
------------

Install the extension with the following command:

.. code-block:: bash

    $ pip install Onshape-Flask


Configuration
-------------

Here’s an example of how Onshape-Flask is typically initialized and configured:

.. code-block:: python

    from flask import Flask
    from flask_onshape import Onshape

    app = Flask(__name__)
    app.config['ONSHAPE_CLIENT_ID'] = 'XXX'
    app.config['ONSHAPE_CLIENT_SECRET'] = 'YYY'

    # For Onshape Enterprise
    app.config['ONSHAPE_BASE_URL'] = 'https://HOSTNAME/api/v3/'
    app.config['ONSHAPE_AUTH_URL'] = 'https://HOSTNAME/login/oauth/'

    onshape = Onshape(app)

The following configuration settings exist for Onshape-Flask:

=================================== ==========================================
`ONSHAPE_CLIENT_ID`                  Your Onshape application's client id. Go to
                                    https://onshape.com/settings/applications
                                    to register new application.

`ONSHAPE_CLIENT_SECRET`              Your Onshape application's client secret.

`ONSHAPE_BASE_URL`                   Base URL for API requests. Override this
                                    to use with Onshape Enterprise. Default is
                                    "https://api.onshape.com/".

`ONSHAPE_AUTH_URL`                   Base authentication endpoint. Override this
                                    to use with Onshape Enterprise. Default is
                                    "https://onshape.com/login/oauth/".
=================================== ==========================================


Authenticating / Authorizing Users
----------------------------------

To authenticate your users with Onshape simply call
:meth:`~flask_onshape.Onshape.authorize` at your login handler:

.. code-block:: python

    @app.route('/login')
    def login():
        return onshape.authorize()


It will redirect the user to Onshape. If the user accepts the authorization
request Onshape will redirect the user to your callback URL with the
OAuth ``code`` parameter. Then the extension will make another request to
Onshape to obtain access token and call your
:meth:`~flask_onshape.Onshape.authorized_handler` function with that token.
If the authorization fails ``oauth_token`` parameter will be ``None``:

.. code-block:: python

    @app.route('/onshape-callback')
    @onshape.authorized_handler
    def authorized(oauth_token):
        next_url = request.args.get('next') or url_for('index')
        if oauth_token is None:
            flash("Authorization failed.")
            return redirect(next_url)

        user = User.query.filter_by(onshape_access_token=oauth_token).first()
        if user is None:
            user = User(oauth_token)
            db_session.add(user)

        user.onshape_access_token = oauth_token
        db_session.commit()
        return redirect(next_url)

Store this token somewhere securely. It is needed later to make requests on
behalf of the user.


Invoking Remote Methods
-----------------------

We need to register a function as a token getter for Onshape-Flask extension.
It will be called automatically by the extension to get the access token of
the user. It should return the access token or ``None``:

.. code-block:: python

    @onshape.access_token_getter
    def token_getter():
        user = g.user
        if user is not None:
            return user.onshape_access_token

After setting up you can use the
:meth:`~flask_onshape.Onshape.get`,  :meth:`~flask_onshape.Onshape.post`
or other verb methods of the :class:`~flask_onshape.Onshape` object.
They will return a dictionary representation of the given API endpoint.

.. code-block:: python

    @app.route('/repo')
    def repo():
        repo_dict = onshape.get('repos/cenkalti/onshape-flask')
        return str(repo_dict)


Full Example
------------

A full example can be found in `example.py`_ file.
Install the required `Flask-SQLAlchemy`_ package first.
Then edit the file and change
``ONSHAPE_CLIENT_ID`` and ``ONSHAPE_CLIENT_SECRET`` settings.
Then you can run it as a python script:

.. code-block:: bash

    $ pip install Flask-SQLAlchemy
    $ python example.py

.. _example.py: https://onshape.com/cenkalti/onshape-flask/blob/master/example.py
.. _Flask-SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/

API Reference
-------------

.. autoclass:: Onshape
   :members:

.. autoclass:: OnshapeError
   :members:
