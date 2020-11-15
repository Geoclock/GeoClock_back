
from flask import Flask, json, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def db_create():
    db.create_all()


@app.route("/start")
def Hello():
    return "Hello to everyoneeee!"



#link to try: http://127.0.0.1:5000/UserC?login=Buka&password=1111
@app.route('/UserC', methods=['GET'])
def hello_user():
    user_data = request.args
    user_controler = UserController()
    if user_controler.create(user_data):
        return "Success!"
    else:
        return "Create failed!"


#link to try: http://127.0.0.1:5000/GeoC?lat=14.19.25&lon=47.21.52&radius=24
@app.route('/GeoC', methods=['GET'])
def hello_geo():
    geo_data = request.args
    geo_controler = GeolocationController()
    if geo_controler.create(geo_data):
        return "Success!"
    else:
        return "Create failed!"


#link to try: http://127.0.0.1:5000/NotC?not=Have_a_good_day)
@app.route('/NotC', methods=['GET'])
def hello_not():
    not_data = request.args
    not_controler = NotificationController()
    if not_controler.create(not_data):
        return "Success!"
    else:
        return "Create failed!"


class ModelUser(object):

    def __init__(self, user_login=None, user_password=None):
        self.user_login = user_login
        self.user_password = user_password


class ModelGeolocation(object):

    def __init__(self, latitude=None, longitude=None, radius=None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius


class ModelNotification(object):

    def __init__(self, notification=None):
        self.notification = notification


class UserController(object):

    def __init__(self, model_user=ModelUser()):
        self.model_user = model_user

    def create(self, user_data=None):
        self.model_user.user_login = user_data.get('login')
        self.model_user.user_password = user_data.get('password')
        if self.model_user.user_login != None and self.model_user.user_password != None:
            return 1
        else:
            return 0


class GeolocationController(object):

    def __init__(self, model_geolocation=ModelGeolocation()):
        self.model_geolocation = model_geolocation

    def create(self,geo_data=None):
        self.model_geolocation.latitude=geo_data.get('lat')
        self.model_geolocation.longitude=geo_data.get('lon')
        self.model_geolocation.radius=geo_data.get('radius')
        if self.model_geolocation.latitude != None and self.model_geolocation.longitude!=None and self.model_geolocation.radius!=None:
            return 1
        else:
            return 0


class NotificationController(object):

    def __init__(self, model_notification=ModelNotification()):
        self.model_notification = model_notification

    def create(self,not_data=None):
        self.model_notification.notification=not_data.get('not')
        if self.model_notification.notification!=None:
            return 1
        else:
            return 0


if __name__ == '__main__':
    manager.run()