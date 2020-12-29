from Database import db
from Models.ModelUser import ModelUser


class ModelGeolocation(db.Model):

    __tablename__ = 'geolocation'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    geo_name = db.Column(db.String, nullable=False)
    geo_address = db.Column(db.String, nullable=False)
    # id of user that own this geolocation
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_creator = db.relationship('ModelUser', backref='user')
    # one to one (Geolocation -> Notification)

    def __init__(self, latitude=None, longitude=None, user_creator=None, geo_name=None, geo_address=None):
        self.latitude = latitude
        self.longitude = longitude
        self.user_creator = user_creator
        self.geo_name = geo_name
        self.geo_address = geo_address

    def add_geolocation_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read_from_db(cls, user_id=None):
        return ModelGeolocation.query.filter_by(creator=user_id).first()

    @classmethod
    def delete_from_db(cls, geo_id=None):
        cls = ModelGeolocation.read_from_db(geo_id=geo_id)
        if not cls:
            return 0
        db.session.delete(cls)
        db.session.commit()
        return 1

    def edit_db(self, new_radius=None):
        self.radius = new_radius
        db.session.commit()
