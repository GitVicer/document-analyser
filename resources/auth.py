from flask import redirect, url_for, session, request, render_template
from flask_smorest import Blueprint
from authlib.integrations.flask_client import OAuth
import os

blp = Blueprint("Auth", "auth")

# auth0 implementation

AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')

oauth = OAuth()

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url='https://{domain}'.format(domain=AUTH0_DOMAIN),
    access_token_url='https://{domain}/oauth/token'.format(domain=AUTH0_DOMAIN),
    authorize_url='https://{domain}/authorize'.format(domain=AUTH0_DOMAIN),
    client_kwargs={
        'scope': 'openid profile email',
        'scope': 'openid profile email read:users',
    },server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

#home

@blp.route('/home')
def home():
    return redirect('http://127.0.0.1:5500/login-logout.html')

#login
#email = vaibhav.dwivedi@biz4solutions.com
#password = Vaibhav@12345

@blp.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("Auth.callback", _external=True))

#callback

@blp.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    next_url = session.pop("next", None)
    if next_url:
        return redirect(next_url)
    else:
        return (render_template('crud.html'))

#logout

@blp.route('/logout')
def logout():
    session.clear()
    return redirect(oauth.auth0.api_base_url + '/v2/logout?' + 'client_id=9D6AjN9xfEPsDiLT4Fc6MadIwDQXcCDI')

# Function to check if a user is logged in using Auth0 authentication

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            session['next'] = request.url
            return redirect(url_for('Auth.login'))
        return f(*args, **kwargs)
    return decorated_function



    


