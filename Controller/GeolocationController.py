from Models.ModelGeolocation import ModelGeolocation
from Models.ModelUser import ModelUser
from Models.ModelNotification import ModelNotification
from Database import db

class GeolocationController(object):

    @classmethod
    def create(cls, geo_data=None):
        latitude = geo_data.get('lat')
        longitude = geo_data.get('lon')
        radius = geo_data.get('radius')
        user_login=geo_data.get('user_login')
        user_creator = ModelUser.read_from_db(user_login=user_login)
        if not latitude or not longitude or not radius or not user_creator:
            return 0
        geolocation = ModelGeolocation(latitude=latitude, longitude=longitude, radius=radius, user_creator=user_creator)
        geolocation.add_geolocation_to_db()
        return 1

    @classmethod
    def read(cls, geo_id=None):
        read_geo = ModelGeolocation.read_from_db(geo_id=geo_id)
        if read_geo:
            return read_geo
        return None

    @classmethod
    def delete(cls, geo_id=None):
        list_of_geo_notification = ModelNotification.read_list_by_point_from_db(point_id=geo_id)
        for i in list_of_geo_notification:
            if not ModelNotification.delete_from_db(not_id=i.id):
                return 0
        if ModelGeolocation.delete_from_db(geo_id=geo_id):
            return 1
        return 0

    @classmethod
    def edit(cls, geo_id=None, geo_data=None):
        new_radius = geo_data.get('new_radius')
        edit_geo = ModelGeolocation.read_from_db(geo_id=geo_id)
        if not edit_geo:
            return 0
        edit_geo.edit_db(new_radius=new_radius)
        return 1
