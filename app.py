from flask import Flask, request
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from Database import db
from Manager import manager

db.init_app(app)
manager.init_app(app)

from Controller.NotificationController import NotificationController
from Controller.GeolocationController import GeolocationController
from Controller.UserController import UserController


migrate = Migrate(app, db)


@app.route("/start")
def Hello():
    return "Hello to everyoneeee!"


# link to try: http://127.0.0.1:5000/UserCreate?login=Buka&password=1111

@app.route('/UserCreate', methods=['GET'])
def hello_user():
    user_data = request.args
    user_controller = UserController()
    if user_controller.create(user_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/UserRead?id=3

@app.route('/UserRead', methods=['GET'])
def read_user():
    user_id = request.args.get('id')
    user_controller = UserController()
    user = user_controller.read(user_id)
    return "For " + user.user_login + " password : " + user.user_password


# link to try: http://127.0.0.1:5000/GeoCreate?lat=14.25&lon=21.52&radius=24

@app.route('/GeoCreate', methods=['GET'])
def hello_geo():
    geo_data = request.args
    geo_controller = GeolocationController()
    if geo_controller.create(geo_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/GeoRead?id=3

@app.route('/GeoRead', methods=['GET'])
def read_geo():
    geo_id = request.args.get('id')
    geo_controller = GeolocationController()
    geo = geo_controller.read(geo_id)
    return "Latitude : " + str(geo.latitude) + "   Longitude : " + str(geo.longitude) + "   Radius : " + str(geo.radius)

# link to try: http://127.0.0.1:5000/NotCreate?not=Have_a_good_day)

@app.route('/NotCreate', methods=['GET'])
def hello_not():
    not_data = request.args
    not_controler = NotificationController()
    if not_controler.create(not_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/NotRead?id=1

@app.route('/NotRead', methods=['GET'])
def read_not():
    not_id = request.args.get('id')
    not_controller = NotificationController()
    not_ = not_controller.read(not_id)
    return "Message : " + not_.notification




if __name__ == '__main__':
    app.run()
