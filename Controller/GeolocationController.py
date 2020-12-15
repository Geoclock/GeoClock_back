from Models.ModelGeolocation import ModelGeolocation
from Models.ModelUser import ModelUser
from Models.ModelNotification import ModelNotification
from Database import db

class GeolocationController(object):

    def create(self, geo_data=None):
        latitude = geo_data.get('lat')
        longitude = geo_data.get('lon')
        radius = geo_data.get('radius')
        user_creator = ModelUser.query.filter_by(user_login=geo_data.get('user_name')).first()
        if not latitude or not longitude or not radius or not user_creator:
            return 0
        geolocation = ModelGeolocation(latitude=latitude, longitude=longitude, radius=radius, user_creator=user_creator)
        geolocation.add_geolocation_to_db()
        return 1

    def read(self, geo_id=None):
        geolocation = ModelGeolocation.query.filter_by(id=geo_id).first()
        geolocation.read_from_db_(geo_id)
        return geolocation

    def delete(self, geo_id=None):
        if not geo_id:
            return 0
        geolocation_not = ModelNotification.query.filter_by(point_id=geo_id).all()
        for i in geolocation_not:
            i.delete_from_db_()
        geolocation = ModelGeolocation.query.filter_by(id=geo_id).first()
        if not geolocation:
            return 0
        geolocation.delete_from_db_()
        return 1

    def edit_geo(self, geo_id=None, geo_data=None):
        new_radius = geo_data.get('new_radius')
        geo = ModelGeolocation.query.filter_by(id=geo_id).first()

        if new_radius:
            geo.radius = new_radius
            db.session.add(geo)
            db.session.commit()
            return 1
        else:
            return 0
