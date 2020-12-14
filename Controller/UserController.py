from Models.ModelUser import ModelUser
from werkzeug.security import check_password_hash, generate_password_hash
from Database import db
from app import app
from flask import redirect, flash, render_template, url_for, request

class UserController(object):

    def read(self, user_id=None, user_login=None):
        user = ModelUser().read_from_db_(user_id=user_id, user_login=user_login)
        return user
