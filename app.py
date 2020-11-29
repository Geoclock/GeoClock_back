from flask import Flask, request
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


# link to try: http://127.0.0.1:5000/UserC?login=Buka&password=1111


@app.route('/UserC', methods=['GET'])
def hello_user():
    user_data = request.args
    user_controler = UserController()
    if user_controler.create(user_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/GeoC?lat=14.19.25&lon=47.21.52&radius=24


@app.route('/GeoC', methods=['GET'])
def hello_geo():
    geo_data = request.args
    geo_controler = GeolocationController()
    if geo_controler.create(geo_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/NotC?not=Have_a_good_day)


@app.route('/NotC', methods=['GET'])
def hello_not():
    not_data = request.args
    not_controler = NotificationController()
    if not_controler.create(not_data):
        return "Success!"
    else:
        return "Create failed!"


class ModelUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)

    def __init__(self, user_login=None, user_password=None):
        self.user_login = user_login
        self.user_password = user_password

    def add_users_to_db(self):
        data = ModelUser(self.user_login, self.user_password)
        db.session.add(data)
        db.session.commit()


class ModelGeolocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Integer, nullable=False)

    def __init__(self, latitude=None, longitude=None, radius=None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    def add_geolocation_to_db(self):
        data = ModelGeolocation(self.latitude, self.longitude, self.radius)
        db.session.add(data)
        db.session.commit()


class ModelNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)

    def __init__(self, notification=None):
        self.notification = notification

    def add_notification_to_db(self):
        data = ModelNotification(self.notification)
        db.session.add(data)
        db.session.commit()


class UserController(object):

    def __init__(self, model_user=ModelUser()):
        self.model_user = model_user

    def create(self, user_data=None):
        self.model_user.user_login = user_data.get('login')
        self.model_user.user_password = user_data.get('password')
        self.model_user.add_users_to_db()
        if self.model_user.user_login != None and self.model_user.user_password != None:
            return 1
        else:
            return 0


class GeolocationController(object):
    def __init__(self, model_geolocation=ModelGeolocation()):
        self.model_geolocation = model_geolocation

    def create(self, geo_data=None):
        self.model_geolocation.latitude = geo_data.get('lat')
        self.model_geolocation.longitude = geo_data.get('lon')
        self.model_geolocation.radius = geo_data.get('radius')

        self.model_geolocation.add_geolocation_to_db()

        if self.model_geolocation.latitude != None and self.model_geolocation.longitude != None and self.model_geolocation.radius != None:
            return 1
        else:
            return 0


class NotificationController(object):
    def __init__(self, model_notification=ModelNotification()):
        self.model_notification = model_notification

    def create(self, not_data=None):
        self.model_notification.notification = not_data.get('not')

        self.model_notification.add_notification_to_db()

        if self.model_notification.notification != None:
            return 1
        else:
            return 0


if __name__ == '__main__':
    manager.run()
