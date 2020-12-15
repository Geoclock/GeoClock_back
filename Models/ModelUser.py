from Database import db
from flask_login import UserMixin
from app import manager
from marshmallow import Schema, fields, validate, ValidationError


class ModelUser(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    # one to many (User -> Geolocation)


    def __init__(self, user_login=None, user_password=None):
        self.user_login = user_login
        self.user_password = user_password

    def add_users_to_db(self):
        data = ModelUser(self.user_login, self.user_password)
        db.session.add(data)
        db.session.commit()

    def read_from_db_(self, user_id=None, user_login=None):
        read_user = ModelUser()
        if user_id:
            print(1)
            # get user from db by his `id`
            read_user = ModelUser.query.filter_by(id=user_id).first()
        elif user_login:
            print(2)
            # get user from db by his `login`
            read_user = ModelUser.query.filter_by(user_login=user_login).first()
        else:
            print(3)
            # if id==login==None
            pass
        self.user_login = read_user.user_login
        self.user_password = read_user.user_password

class UserValidation(Schema):
    username = fields.String(required=True)
    password = fields.String(validate=validate.Length(min=4), required=True)

@manager.user_loader
def load_user(user_id):
    return ModelUser.query.get(user_id)
