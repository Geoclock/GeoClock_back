from Models.ModelNotification import ModelNotification
from Models.ModelGeolocation import ModelGeolocation
from Database import db


class NotificationController(object):

    @classmethod
    def create(cls, not_data=None):
        notification = not_data.get('not')
        geo_id=not_data.get('geo_id')
        point = ModelGeolocation.read_from_db(geo_id=geo_id)
        if not notification or not point:
            return 0
        Notification = ModelNotification(notification=notification, point=point)
        Notification.add_notification_to_db()
        return 1


    @classmethod
    def read(cls, not_id=None):
        read_notification = ModelNotification.read_from_db(not_id=not_id)
        if read_notification:
            return read_notification
        return None

    @classmethod
    def delete(cls, not_id=None):
        if ModelNotification.delete_from_db(not_id=not_id):
            return 1
        return 0

    @classmethod
    def edit(cls, not_id=None, not_data=None):
        new_notification = not_data.get('notification')
        edit_notification = ModelNotification.read_from_db(not_id=not_id)
        if not edit_notification:
            return 0
        edit_notification.edit_db(new_notification=new_notification)
        return 1
