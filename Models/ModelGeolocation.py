from Models.ModelUser import db


class ModelGeolocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Integer, nullable=False)

    def __init__(self, latitude=None, longitude=None, radius=None):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    def add_geolocation_to_db(self):
        data = ModelGeolocation(self.latitude, self.longitude, self.radius)
        db.session.add(data)
        db.session.commit()

    def read_from_db_(self, geo_id):
        geo = ModelGeolocation.query.filter_by(id=geo_id).first()
        self.latitude = geo.latitude
        self.longitude = geo.longitude
        self.radius = geo.radius