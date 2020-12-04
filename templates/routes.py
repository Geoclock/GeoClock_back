from flask import request, redirect, flash, render_template
from flask_login import login_user
from werkzeug.security import check_password_hash
from app import app

from Models.ModelUser import ModelUser

# LOGIN
# link to try: http://127.0.0.1:5000/login


@app.route("/login", methods=['GET', 'POST'])
def Login():

    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:

        # user founded in db by entered login
        user = ModelUser()
        user.read_from_db_(user_login=login)

        # checking existing & entered password
        if check_password_hash(user.user_password, password):

            login_user(user)

            return render_template('logged_in.html', user=user)

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


# REGISTER
# назву методу лишаєте таку ж, в нас на вас ссилочка)) решту дописуйте


@app.route("/register", methods=['GET', 'POST'])
def Register():
    return render_template('register.html')
