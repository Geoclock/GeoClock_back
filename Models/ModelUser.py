from Database import db
from flask_login import UserMixin
from app import manager
from marshmallow import Schema, fields, validate, ValidationError


class ModelUser(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    hash_code = db.Column(db.String(120))
    default_folder_id = db.Column(db.Integer)

    def __init__(self, user_login=None,
                 user_email=None,
                 user_password=None,
                 hash_code=None):
        self.user_login = user_login
        self.user_email = user_email
        self.user_password = user_password
        self.hash_code = hash_code
        self.default_folder_id = None

    def add_users_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_changes_to_db(self):
        db.session.commit()

    @classmethod
    def read_from_db(cls, user_id=None,
                     user_login=None,
                     user_email=None,
                     hash_code=None):
        if user_id:
            # get user from db by his `id`
            return ModelUser.query.filter_by(id=user_id).first()
        if user_login:
            # get user from db by his `login`
            return ModelUser.query.filter_by(user_login=user_login).first()
        if user_email:
            # get user from db by his `email`
            return ModelUser.query.filter_by(user_email=user_email).first()
        if hash_code:
            # get user from db by his `hash_code`
            return ModelUser.query.filter_by(hash_code=hash_code).first()
        return None


class UserValidation(Schema):
    login = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=4), required=True)
    password2 = fields.String(validate=validate.Length(min=4), required=True)


@manager.user_loader
def load_user(user_id):
    return ModelUser.query.get(user_id)
