from Database import db


class ModelGeolocation(db.Model):

    __tablename__ = 'geolocation'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    # id of user that own this geolocation
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    # one to one (Geolocation -> Notification)
    message = db.relationship('ModelNotification', backref='point', uselist=False)

    def __init__(self, latitude=None, longitude=None, radius=None, creator=None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.creator = creator

    def add_geolocation_to_db(self):
        data = ModelGeolocation(self.latitude, self.longitude, self.radius, self.creator)
        db.session.add(data)
        db.session.commit()

    def read_from_db_(self, geo_id):
        read_geo = ModelGeolocation.query.filter_by(id=geo_id).first()
        self.latitude = read_geo.latitude
        self.longitude = read_geo.longitude
        self.radius = read_geo.radius
        #self.creator = geo.creator