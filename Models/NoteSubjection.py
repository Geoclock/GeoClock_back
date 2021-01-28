from Database import db
from Models.ModelNotification import ModelNotification

"""
клас, що реалізує зв'язок багато до багатьох між таблицями 
нотифікації і геолокації
кожен зв'язок подається як новий об'єкт в базі даних в даній таблиці, 
з парою айдішок (геолокації і нотифікації відповідно)
"""


class NoteSubjection(db.Model):
    __tablename__ = 'notesubjection'

    id = db.Column(db.Integer, primary_key=True)
    geolocation_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'))
    geolocation = db.relationship('ModelGeolocation', backref='geolocation')
    notification = db.relationship('ModelNotification', backref='notifications')

    def __init__(self, notification=None, geolocation=None):
        self.geolocation = geolocation
        self.notification = notification

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    """
    при видаленні геолокації необхідно видалити усі нотифікації,
    що мали прив'язку до неї і відповідно об'єкту, що зберігає цей зв'язок
    """

    @classmethod
    def delete_geos_notes(cls, geo_id=None):
        list = NoteSubjection.query.filter_by(geolocation_id=geo_id).all()
        for subjection in list:
            NoteSubjection.delete_from_db(subjection=subjection)
            ModelNotification.delete_from_db(not_id=subjection.notification_id)

    """
    при видаленні лише нотифікації потрібно видалити усі зв'язки, 
    які були створенні з нею
    """

    @classmethod
    def delete_by_notes(cls, not_id=None):
        list = NoteSubjection.query.filter_by(notification_id=not_id).all()
        for subjection in list:
            NoteSubjection.delete_from_db(subjection=subjection)

    @classmethod
    def delete_from_db(cls, subjection=None):
        db.session.delete(subjection)
        db.session.commit()
