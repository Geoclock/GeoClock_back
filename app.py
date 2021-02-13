from flask import Flask
from flask_migrate import Migrate
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



from templates import primary_routes

db.init_app(app)
manager.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
