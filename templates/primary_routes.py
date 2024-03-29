from flask import request
from app import app
from Database import db
from Email import Email
from flask_mail import Message
from flask import request, redirect, flash, render_template, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from Controller.NotificationController import NotificationController
from Controller.GeolocationController import GeolocationController
from Controller.UserController import UserController
from Controller.FolderController import FolderController
from Models.ModelUser import ModelUser, UserValidation
from Models.NoteSubjection import NoteSubjection
from marshmallow import ValidationError
import random
import string
import json


@app.route("/home")
def Hello():
    return render_template('home.html', user=current_user)


@app.route("/ERROR")
def ERROR():
    return "OOPS..."


# link to try: http://127.0.0.1:5000/register
@app.route("/Register", methods=['GET', 'POST'])
def Register():
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not login or not email or not password or not password2:
            return jsonify(status=404, message='Missing values!')
        elif ModelUser.read_from_db(user_login=login) or ModelUser.read_from_db(user_email=email):
            return jsonify(status=404, message='User with such login/email already exist!')
        elif password != password2:
            return jsonify(status=400, message='Passwords are not equal!')
        else:
            try:
                UserValidation().load(request.form)
                hash_pwd = generate_password_hash(password)
                new_user = ModelUser(user_login=login, user_email=email, user_password=hash_pwd)
                new_user.add_users_to_db()
                login_user(new_user, remember=True)
                """При створенні нового юзера створюємо йому дефолтну папочку"""
                FolderController.create(user_id=new_user.id, folder_data={'created_by_user': True})
                return jsonify(status=200, message='OK!')
            except ValidationError as error:
                return jsonify(status=400, message='Wrong input!')


@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        if login and password:
            user = ModelUser.read_from_db(user_login=login)
            if user and check_password_hash(user.user_password, password):
                login_user(user, remember=True)
                return jsonify(status=200, message='OK!', id=user.id)
            else:
                return jsonify(status=404, message='Login or password do not match')
        else:
            return jsonify(status=400, message='Enter login and password fields')


@app.route("/GoogleLogin", methods=['GET', 'POST'])
def GoogleLogin():
    if request.method == "POST":
        login = request.form['login']
        email = request.form['email']
        if login and email:
            user = ModelUser.read_from_db(user_login=login)
            if user:
                login_user(user, remember=True)
                return jsonify(status=200, message='OK!', id=user.id)
            else:
                return jsonify(status=404, message='The user was not found!')
        else:
            return jsonify(status=400, message='Enter login and email fields')


# LOGOUT
@app.route('/logout')
@login_required
def Logout():
    logout_user()
    return jsonify(status=200, message='OK!')


@app.route('/ResetPassword', methods=["POST", "GET"])
def ResetPassword():
    if request.method == "POST":
        mail = request.form['email']
        if not mail:
            return jsonify(status=400, message='Please, enter your email!')
        check = ModelUser.read_from_db(user_email=mail)
        if check:
            with app.app_context():
                hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                check.hash_code = hashCode
                check.commit_changes_to_db()
                msg = Message('Confirm Password Change', sender=app.config.get('MAIL_USERNAME'), recipients=[mail])
                msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, enter the code in your app and than enter your new password\n\n" + check.hash_code
                Email.send(msg)
        else:
            return jsonify(status=404, message='There is no user with such email!')
        return jsonify(status=200, message='OK!')


@app.route("/Code", methods=["GET", "POST"])
def EnterCode():
    if request.method == "POST":
        if not request.form['code']:
            return jsonify(status=400, message='Please, enter the code!')
        check = ModelUser.read_from_db(hash_code=request.form['code'])
        if check:
            return jsonify(status=200, message='OK!')
        else:
            return jsonify(status=404, message='Wrong code!')


@app.route("/New_password/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    if request.method == 'POST':
        check = ModelUser.read_from_db(hash_code=hashCode)
        password = request.form['password']
        check_password = request.form['check_password']
        if not password or not check_password:
            return jsonify(status=400, message="Missing values!")
        if password == check_password:
            check.user_password = generate_password_hash(password)
            check.hash_code = None
            check.commit_changes_to_db()
            return jsonify(status=200, message="OK!")
        else:
            return jsonify(status=400, message='Passwords are different!')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('Login'))
    return response


@app.route('/UserRead', methods=['GET', 'POST'])
def read_user():
    id = request.form['id']
    data = UserController.read(user_id=id)
    # return jsonify(status=200, userdata='UserController.read(user_id=id)')
    return jsonify(status=200, userdata={'id': data.id,
                                         'user_login': data.user_login,
                                         'user_email': data.user_email,
                                         'default_folder_id': data.default_folder_id})


@app.route('/AllNotificationRead', methods=['GET', 'POST'])
def all_notification_read():
    user_id = request.form['user_id']
    notifications = NotificationController.read(user_id=user_id)
    list=[]
    for notification in notifications:
        list.append({
            'id': notification.id,
            'notification': notification.notification,
            'radius': notification.radius
        })
    return jsonify(status=200, notifications=list)

@app.route('/AllNoteSubjectionsRead', methods=['GET', 'POST'])
def all_notesubjections_read():
    user_id = request.form['user_id']
    notesubjections = NoteSubjection.query.filter_by(creator_id=user_id).all()
    list=[]
    for notesubjection in notesubjections:
        list.append({
            'id': notesubjection.id,
            'geo_id': notesubjection.geolocation_id,
            'note_id': notesubjection.notification_id
        })
    return jsonify(status=200, notesubjections=list)


@app.route('/AllGeolocationsRead', methods=['GET', 'POST'])
def all_geolocations_read():
    user_id = request.form['user_id']
    geolocations = GeolocationController.read(user_id=user_id)
    list=[]
    for geolocation in geolocations:
        list.append({
            'id': geolocation.id,
            'geo_name': geolocation.geo_name,
            'latitude': geolocation.latitude,
            'longitude': geolocation.longitude,
            'address':geolocation.geo_address,
            'folder_id':geolocation.folder_id
        })
    return jsonify(status=200, geolocations=list)



@app.route('/AllFoldersRead', methods=['GET', 'POST'])
def all_folders_read():
    user_id = request.form['user_id']
    folders = FolderController.read(user_id=user_id)
    list=[]
    for folder in folders:
        list.append({
            'id': folder.id,
            'folder_name': folder.folder_name
        })
    return jsonify(status=200, folders=list)



@app.route('/NoteCreate', methods=['POST', 'GET', 'PUT'])
def create_note():
    note_data = request.form
    user_id = request.form['user_id']
    print(note_data)
    data = NotificationController.create(user_id=user_id,
                                  not_data=note_data)
    print(data)
    return jsonify(status=200, notedata={'id': data.id,
                                         'notification': data.notification,
                                         'radius': data.radius})







@app.route('/FolderRead', methods=['GET'])
@login_required
def read_folder():
    return FolderController.read(user_id=current_user.id)


def render_create_folder():
    folder_list = read_folder()
    geo_list = FolderController.read_folders_geo(folder_list=folder_list)
    return render_template('create_folder.html',
                           folder_list=folder_list,
                           geo_list=geo_list)


@app.route('/FolderCreate', methods=['POST', 'GET', 'PUT'])
@login_required
def create_folder():
    if request.method == "POST":
        folder_data = request.form.to_dict()
        folder_data['created_by_user'] = 1
        FolderController.create(user_id=current_user.id,
                                folder_data=folder_data)
    return render_create_folder()


@app.route('/FolderEdit', methods=['POST', 'GET', 'PUT'])
@login_required
def edit_folder():
    if request.method == "POST":
        folder_data = request.form.to_dict()
        folder_id = folder_data.get('id')
        FolderController.edit(folder_id=folder_id,
                              folder_data=folder_data)
    return render_create_folder()


@app.route('/FolderDelete', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def delete_folder():
    if request.method == "POST":
        folder_data = request.form.to_dict()
        folder_id = folder_data.get('id')
        FolderController.delete(folder_id=folder_id)
    return render_create_folder()


def render_create_geo():
    folder_list = read_folder()
    geo_list = FolderController.read_folders_geo(folder_list=folder_list)
    return render_template('create_geo.html',
                           folder_list=folder_list,
                           geo_list=geo_list)


@app.route('/GeoCreate', methods=['POST', 'GET', 'PUT'])
@login_required
def create_geo():
    if request.method == "POST":
        geo_data = request.form.to_dict()
        GeolocationController.create(user_id=current_user.id,
                                     geo_data=geo_data)
    return render_create_geo()


@app.route('/GeoEdit', methods=['POST', 'GET', 'PUT'])
@login_required
def edit_geo():
    if request.method == "POST":
        geo_data = request.form.to_dict()
        geo_id = geo_data.get('id')
        GeolocationController.edit(geo_data=geo_data,
                                   geo_id=geo_id)
    return render_create_geo()


@app.route('/GeoDelete', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def delete_geo():
    if request.method == "POST":
        geo_data = request.form.to_dict()
        geo_id = geo_data.get('id')
        GeolocationController.delete(geo_id=geo_id)
    return render_create_geo()


def render_create_note():
    folder_list = read_folder()
    geo_list = FolderController.read_folders_geo(folder_list=folder_list)
    note_list = NotificationController.read(user_id=current_user.id)
    notes_geos = NotificationController.read_notes_geo(note_list=note_list)
    return render_template('create_note.html',
                           note_list=note_list,
                           notes_geos=notes_geos,
                           folder_list=folder_list,
                           geo_list=geo_list)




@app.route('/NoteEdit', methods=['POST', 'GET', 'PUT'])
@login_required
def edit_note():
    if request.method == "POST":
        note_data = request.form.to_dict()
        not_id = note_data.get('id')
        NotificationController.edit(not_id=not_id,
                                    not_data=note_data)
    return render_create_note()


@app.route('/NoteDelete', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def delete_note():
    if request.method == "POST":
        note_data = request.form.to_dict()
        not_id = note_data.get('id')
        NotificationController.delete(not_id=not_id)
    return render_create_note()
