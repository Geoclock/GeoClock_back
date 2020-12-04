from flask import request
from app import app

from Controller.NotificationController import NotificationController
from Controller.GeolocationController import GeolocationController
from Controller.UserController import UserController


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
    read_user = user_controller.read(user_id)
    return "For " + read_user.user_login + " password : " + read_user.user_password


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
    read_geo = geo_controller.read(geo_id)
    return "Latitude : " + str(read_geo.latitude) + "   Longitude : " + str(read_geo.longitude) + "   Radius : " + str(
        read_geo.radius)


# link to try: http://127.0.0.1:5000/NotCreate?not=Have_a_good_day)

@app.route('/NotCreate', methods=['GET'])
def hello_not():
    notification_data = request.args
    notification_controler = NotificationController()
    if notification_controler.create(notification_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/NotRead?id=1

@app.route('/NotRead', methods=['GET'])
def read_not():
    notification_id = request.args.get('id')
    notification_controller = NotificationController()
    read_notification = notification_controller.read(notification_id)
    return "Message : " + read_notification.notification

