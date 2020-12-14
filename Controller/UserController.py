from Models.ModelUser import ModelUser
from werkzeug.security import check_password_hash, generate_password_hash
from Database import db
from app import app
from flask import redirect, flash, render_template, url_for, request

class UserController(object):

    def __init__(self, model_user=ModelUser()):
        self.model_user = model_user

    def read(self, user_id=None, user_login=None):
        self.model_user.read_from_db_(user_id=user_id, user_login=user_login)
        return self.model_user
