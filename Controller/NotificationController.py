from Models.ModelNotification import ModelNotification
from Models.ModelGeolocation import ModelGeolocation


class NotificationController(object):

    def create(self, not_data=None):
        notification = not_data.get('not')
        point = ModelGeolocation.query.filter_by(id=not_data.get('geo_id')).first()
        if not notification or not point:
            return 0
        Notification = ModelNotification(notification=notification, point=point)
        Notification.add_notification_to_db()
        return 1

    def read(self, not_id=None):
        notification = ModelNotification.query.filter_by(id=not_id).first()
        notification.read_from_db_(not_id)
        return notification
    
    def delete(self, not_id=None):
        notification = ModelNotification.query.filter_by(id=not_id).first()
        if not notification:
            return 0
        notification.delete_from_db_()
        return 1