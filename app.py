from flask import Flask
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS

from Database import db
from Manager import manager
from Email import Email
import smtplib

app = Flask(__name__)
CORS(app)
app.secret_key = 'hehehe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "geoclock.app@gmail.com"
app.config['MAIL_PASSWORD'] = "GeoClock.app2021"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

Email.init_app(app)


oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="744227890838-ieq7ui7qsitm3m9fh7rou484l91lfdva.apps.googleusercontent.com",
    client_secret="kNj2joV3cojVeu12jhOz8lQt",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


from templates import primary_routes

db.init_app(app)
manager.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
