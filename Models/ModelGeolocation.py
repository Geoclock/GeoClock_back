from Database import db
from Models.ModelUser import ModelUser
from Models.ModelFolder import ModelFolder
from Models.NoteSubjection import NoteSubjection


class ModelGeolocation(db.Model):
    __tablename__ = 'geolocation'

    id = db.Column(db.Integer, primary_key=True)
    geo_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    geo_address = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('ModelUser', backref='geouser')
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    folder = db.relationship('ModelFolder', backref='folder')

    def __init__(self, latitude=None,
                 longitude=None,
                 creator=None,
                 geo_name=None,
                 geo_address=None,
                 folder=None):
        self.latitude = latitude
        self.longitude = longitude
        self.creator = creator
        self.geo_name = geo_name
        self.geo_address = geo_address
        self.folder = folder

    def add_geolocation_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read_from_db(cls, user_id=None,
                     folder_id=None,
                     geo_id=None):
        if user_id:
            return ModelGeolocation.query.filter_by(creator_id=user_id).all()
        if folder_id:
            return ModelGeolocation.query.filter_by(folder_id=folder_id).all()
        if geo_id:
            return ModelGeolocation.query.filter_by(id=geo_id).first()
        return None

    @classmethod
    def delete_from_db(cls, geo_id=None,
                       folder_id=None):
        """Видалення лише однієї геолокації"""
        if geo_id:
            geo_to_delete = ModelGeolocation.read_from_db(geo_id=geo_id)
            if geo_to_delete:
                NoteSubjection.delete_geos_notes(geo_id=geo_to_delete.id)
                db.session.delete(geo_to_delete)
                db.session.commit()
                return 1
            return 0
        """Видалення геолокацій шо містяться в деякій папці"""
        if folder_id:
            list_to_delete = ModelGeolocation.read_from_db(folder_id=folder_id)
            for geo_to_delete in list_to_delete:
                NoteSubjection.delete_geos_notes(geo_id=geo_to_delete.id)
                db.session.delete(geo_to_delete)
                db.session.commit()
            return 1
        return 0

    def edit_db(self, new_geo_name=None, folder_id=None):
        if new_geo_name:
            self.geo_name = new_geo_name
        if folder_id:
            new_folder = ModelFolder.read_from_db(folder_id=folder_id)
            if new_folder:
                self.folder = new_folder
        db.session.commit()
