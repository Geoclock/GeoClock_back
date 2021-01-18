from flask import jsonify
from Models.ModelGeolocation import ModelGeolocation
from Models.ModelUser import ModelUser
from Models.ModelNotification import ModelNotification
from Models.ModelFolder import ModelFolder
from Database import db


class GeolocationController(object):

    @classmethod
    def create(cls, geo_data=None, user_id=None):
        try:
            latitude = geo_data.get('lat')
            longitude = geo_data.get('lon')
            geo_name = geo_data.get('name')
            geo_address = geo_data.get('geo_address')
            creator = ModelUser.read_from_db(user_id=user_id)
        except:
            return 0
        if geo_data.get('folder_id'):
            folder_id = geo_data.get('folder_id')
            folder = ModelFolder.read_from_db(folder_id=folder_id)
        else:
            folder = ModelFolder.read_from_db(folder_id=creator.default_folder_id)
        geolocation = ModelGeolocation(latitude=latitude,
                                       longitude=longitude,
                                       geo_name=geo_name,
                                       geo_address=geo_address,
                                       creator=creator,
                                       folder=folder)
        geolocation.add_geolocation_to_db()
        return 1

    @classmethod
    def read(cls, user_id=None, folder_id=None, geo_id=None):
        if user_id:
            return ModelGeolocation.read_from_db(user_id=user_id)
        if folder_id:
            return ModelGeolocation.read_from_db(folder_id=folder_id)
        if geo_id:
            return ModelGeolocation.read_from_db(geo_id=geo_id)
        return None

    @classmethod
    def delete(cls, geo_id=None, folder_id=None):
        if geo_id:
            try:
                ModelGeolocation.delete_from_db(geo_id=geo_id)
            except:
                return 0
        if folder_id:
            try:
                ModelGeolocation.delete_from_db(folder_id=folder_id)
            except:
                return 0

    @classmethod
    def edit(cls, geo_id=None, geo_data=None):
        edit_geo = ModelGeolocation.read_from_db(geo_id=geo_id)
        if geo_data.get('new_name'):
            new_geo_name = geo_data.get('new_name')
            edit_geo.edit_db(new_geo_name=new_geo_name)
        if geo_data.get('folder_id'):
            folder_id = geo_data.get('folder_id')
            edit_geo.edit_db(folder_id=folder_id)
        return 1
