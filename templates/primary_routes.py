from flask import request
from app import app
from Database import db
from flask import request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from Controller.NotificationController import NotificationController
from Controller.GeolocationController import GeolocationController
from Controller.UserController import UserController
from Models.ModelUser import ModelUser, UserValidation
from marshmallow import ValidationError


@app.route("/home")
def Hello():
    return render_template('home.html', user=current_user)


# link to try: http://127.0.0.1:5000/register
@app.route("/register", methods=['GET', 'POST'])
def Register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not login or not password or not password2:
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            ModelUser(user_login=login, user_password=hash_pwd).add_users_to_db()
            return redirect(url_for('Login'))
    return render_template('register.html')


# LOGIN
# link to try: http://127.0.0.1:5000/login
@app.route("/login", methods=['GET', 'POST'])
def Login():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        # user founded in db by entered login
        user = ModelUser.read_from_db(user_login=login)
        # checking existing & entered password
        if user and check_password_hash(user.user_password, password):
            login_user(user, remember=True)
            return redirect(url_for('Hello'))
            # поки не юзаєм цього
            # то переадресація не некст сторіночку, куда може попасти залогований юзер
            """
            # redirecting user to the next page
            next_href = request.args.get('next')
            redirect(next_href)
            """
        else:
            flash('Login or password do not match')
    else:
        flash('Enter login and password fields')
    return render_template('login.html')



# LOGOUT
@app.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Hello'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('Login'))
    return response


# link to try: http://127.0.0.1:5000/UserRead
@app.route('/UserRead', methods=['GET'])
@login_required
def read_user():
    #user_id = request.args.get('id')
    read_user = UserController.read(user_id=current_user.id)
    if read_user:
        return "For " + read_user.user_login + " password : " + read_user.user_password
    else:
        return "Error!"

# link to try: http://127.0.0.1:5000/GeoCreate?lat=14.25&lon=21.52&radius=24
@app.route('/GeoCreate', methods=['POST'])
@login_required
def hello_geo():
    geo_data = request.form
    if GeolocationController.create(geo_data=geo_data, user_login=current_user.user_login):
        #return "Success!"
        flash('Successfully created geolocation!')
    else:
        #return "Create failed!"
        flash('Creation failed!')
    return redirect(url_for('Hello'))



#by user_id
# link to try: http://127.0.0.1:5000/GeoRead?id=21
@app.route('/GeoRead', methods=['GET'])
@login_required
def read_geo():
    user_id = request.args.get('id')
    read_geo = GeolocationController.read(user_id=user_id)
    return read_geo


# link to try: http://127.0.0.1:5000/GeoEdit?id=1&new_radius=20
@app.route('/GeoEdit', methods=['PUT'])
@login_required
def update_geo():
    geo_id = request.args.get('id')
    geo_data = request.args
    if GeolocationController.edit(geo_id=geo_id, geo_data=geo_data):
        return "Successfully edited"
    else:
        return "ERROR"


# link to try: http://127.0.0.1:5000/GeoDelete?id=1
@app.route('/GeoDelete', methods=['DELETE'])
@login_required
def delete_geo():
    geolocation_id = request.args.get('id')
    if GeolocationController.delete(geo_id=geolocation_id):
        return "Successfully deleted"
    else:
        return "ERROR"


# link to try: http://127.0.0.1:5000/NotCreate?not=Have_a_good_day&geo_id=1)
@app.route('/NotCreate', methods=['POST'])
@login_required
def hello_not():
    notification_data = request.args
    if NotificationController.create(not_data=notification_data):
        return "Success!"
    else:
        return "Create failed!"


# link to try: http://127.0.0.1:5000/NotRead?id=1
@app.route('/NotRead', methods=['GET'])
@login_required
def read_not():
    notification_id = request.args.get('id')
    read_notification = NotificationController.read(not_id=notification_id)
    if read_notification:
        return "Message : " + read_notification.notification
    else:
        return "Error!"


# link to try: http://127.0.0.1:5000/NotDelete?id=1
@app.route('/NotDelete', methods=['DELETE'])
@login_required
def delete_not():
    notification_id = request.args.get('id')
    if NotificationController.delete(not_id=notification_id):
        return "Successfully deleted"
    else:
        return "Error!"


# link to try: http://127.0.0.1:5000/NotEdit?id=1&notification=newtext
@app.route('/NotEdit', methods=['PUT'])
@login_required
def update_notification():
    not_data = request.args
    not_id = request.args.get('id')
    if NotificationController.edit(not_id=not_id, not_data=not_data):
        return "Successfully edited"
    else:
        return "ERROR"

