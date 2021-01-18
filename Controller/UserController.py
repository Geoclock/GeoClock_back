from Models.ModelUser import ModelUser
from werkzeug.security import check_password_hash, generate_password_hash
from Database import db
from app import app
from flask import redirect, flash, render_template, url_for, request


class UserController(object):

    @classmethod
    def read(cls, user_id=None, user_login=None):
        read_user = ModelUser.read_from_db(user_id=user_id, user_login=user_login)
        if read_user:
            return read_user
        return None
