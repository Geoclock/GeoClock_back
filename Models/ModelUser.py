from Database import db
from flask_login import UserMixin
from app import manager


class ModelUser(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(50), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    # one to many (User -> Geolocation)
    list_of_points = db.relationship('ModelGeolocation', backref='user')

    def __init__(self, user_login=None, user_password=None):
        self.user_login = user_login
        self.user_password = user_password

    def add_users_to_db(self):
        data = ModelUser(self.user_login, self.user_password)
        db.session.add(data)
        db.session.commit()


    def read_from_db_(self, user_id=None, user_login=None):

        if user_id:
            # get user from db by his `id`
            read_user = ModelUser.query.filter_by(id=user_id).first()
        elif user_login:
            # get user from db by his `login`
            read_user = ModelUser.query.filter_by(user_login=user_login).first()
        else:
            # if id==login==None
            pass

        self.user_login = read_user.user_login
        self.user_password = read_user.user_password


@manager.user_loader
def load_user(user_id):
    return ModelUser.query.get(user_id)
