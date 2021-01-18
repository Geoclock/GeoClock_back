from Models.ModelNotification import ModelNotification
from Models.ModelGeolocation import ModelGeolocation
from Models.ModelUser import ModelUser
from Database import db
from Models.NoteSubjection import NoteSubjection


class NotificationController(object):

    @classmethod
    def create(cls, not_data=None, user_id=None):
        notification = not_data.get('note')
        geo_id = not_data.get('geo_id')
        radius = not_data.get('radius')
        if geo_id:
            geolocation = ModelGeolocation.read_from_db(geo_id=geo_id)
        if user_id:
            user = ModelUser.read_from_db(user_id=user_id)
        if not notification or not geo_id or not radius:
            return 0
        Notification = ModelNotification(notification=notification,
                                         radius=radius,
                                         creator=user)
        Notification.add_notification_to_db()
        """Незабуваєм оформти зв'язок геолокація - нотифікація"""
        subjection = NoteSubjection(notification=Notification,
                                    geolocation=geolocation)
        subjection.add_to_db()
        return 1

    @classmethod
    def read(cls, not_id=None,
             user_id=None):
        if not_id:
            return ModelNotification.read_from_db(not_id=not_id)
        if user_id:
            return ModelNotification.read_from_db(user_id=user_id)
        return None

    """читаємо геолокацію до якої прив'язана нотифікація"""

    @classmethod
    def read_note_geo_id(cls, not_id=None):
        if not_id:
            subjection = NoteSubjection.query.filter_by(notification_id=not_id).first()
            return subjection.geolocation_id
        return None

    """оформляємо словник для повернення
    за індекс береться айді нотатки, в самій комірці міститься об'єкт зв'язаної геолокації"""

    @classmethod
    def read_notes_geo(cls, note_list=None):
        list = {}
        for note in note_list:
            geo_id = NotificationController.read_note_geo_id(not_id=note.id)
            list[note.id] = ModelGeolocation.read_from_db(geo_id=geo_id)
        return list

    @classmethod
    def delete(cls, not_id=None):
        NoteSubjection.delete_by_notes(not_id=not_id)
        if ModelNotification.delete_from_db(not_id=not_id):
            return 1
        return 0

    @classmethod
    def edit(cls, not_id=None, not_data=None):
        new_notification = not_data.get('note')
        new_radius = not_data.get('radius')
        edit_notification = ModelNotification.read_from_db(not_id=not_id)
        if not edit_notification:
            return 0
        edit_notification.edit_db(new_notification=new_notification, new_radius=new_radius)
        return 1
