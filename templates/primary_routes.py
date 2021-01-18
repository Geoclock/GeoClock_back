from flask import request
from app import app,oauth,google
from Database import db
from Email import Email
from flask_mail import Message
from flask import request, redirect, flash, render_template, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from Controller.NotificationController import NotificationController
from Controller.GeolocationController import GeolocationController
from Controller.UserController import UserController
from Controller.FolderController import FolderController
from Models.ModelUser import ModelUser, UserValidation
from marshmallow import ValidationError
import random
import string


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
            flash('Please, fill all fields!')
        elif ModelUser.read_from_db(user_login=login) or ModelUser.read_from_db(user_email=email):
            flash('User with such login/email already exist!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            try:
                UserValidation().load(request.form)
                hash_pwd = generate_password_hash(password)
                new_user = ModelUser(user_login=login, user_email=email, user_password=hash_pwd)
                new_user.add_users_to_db()
                """При створенні нового юзера створюємо йому дефолтну папочку"""
                FolderController.create(user_id=new_user.id, folder_data={'created_by_user': True})
                return redirect(url_for('Login'))
            except ValidationError as error:
                flash(error)
    return render_template('register.html')





# LOGIN
# link to try: http://127.0.0.1:5000/login
@app.route("/Login", methods=['GET', 'POST'])
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


# Google register
@app.route('/register')
def google_register():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize_new_account', _external=True)
    return google.authorize_redirect(redirect_uri)

# Google login
@app.route('/login')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# google authorize
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()
    print(user)
    print(user_info)
    user_email=user_info['email']
    user = ModelUser.read_from_db(user_email=user_email)
    # checking existing & entered password
    if user:
        login_user(user, remember=True)
        return redirect(url_for('Hello'))
    flash('User isn`t registered. Start with register!')
    return render_template('login.html')


@app.route('/authorize_new_account')
def authorize_new_account():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    login = user_info['name']
    email = user_info['email']
    print(user_info)
    #return GoogleRegister(login=login,email=email)
    return render_template('google_register.html',login=login,email=email)

@app.route("/GoogleRegister", methods=['GET', 'POST'])
def GoogleRegister():
    login = request.form.get('login')
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not password or not password2:
            flash('Please, fill all fields!')
        elif ModelUser.read_from_db(user_login=login) or ModelUser.read_from_db(user_email=email):
            flash('User with such login/email already exist!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            try:
                UserValidation().load(request.form)
                hash_pwd = generate_password_hash(password)
                new_user = ModelUser(user_login=login, user_email=email, user_password=hash_pwd)
                new_user.add_users_to_db()
                """При створенні нового юзера створюємо йому дефолтну папочку"""
                FolderController.create(user_id=new_user.id, folder_data={'created_by_user': True})
                return redirect(url_for('Login'))
            except ValidationError as error:
                flash(error)
    return render_template('google_register.html',login=login,email=email)



# LOGOUT
@app.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Hello'))


@app.route('/ResetPassword', methods=["POST", "GET"])
def ResetPassword():
    if request.method == "POST":
        mail = request.form['email']
        check = ModelUser.read_from_db(user_email=mail)

        if check:
            with app.app_context():
                hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
                check.hash_code = hashCode
                check.commit_changes_to_db()
                msg = Message('Confirm Password Change', sender=app.config.get('MAIL_USERNAME'), recipients=[mail])
                msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hash_code
                Email.send(msg)
                flash("The letter was sent. Please, follow the instructions in the letter")
        else:
            flash("The user with such email was not found!")
    return render_template('reset_password.html')


@app.route("/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    check = ModelUser.read_from_db(hash_code=hashCode)
    if check:
        if request.method == 'POST':
            password = request.form['password']
            check_password = request.form['check_password']
            if password == check_password:
                check.user_password = generate_password_hash(password)
                check.hash_code = None
                check.commit_changes_to_db()
                return redirect(url_for('Hello'))
            else:
                flash('Passwords are different!')
    return render_template("new_password.html")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('Login'))
    return response


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


@app.route('/NoteCreate', methods=['POST', 'GET', 'PUT'])
@login_required
def create_note():
    if request.method == "POST":
        note_data = request.form.to_dict()
        NotificationController.create(user_id=current_user.id,
                                      not_data=note_data)
    return render_create_note()


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
