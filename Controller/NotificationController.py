from Models.ModelNotification import ModelNotification
from Models.ModelGeolocation import ModelGeolocation
from Database import db


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

    def edit(self, not_id=None, not_data=None):
        curr_notification = ModelNotification.query.filter_by(id=not_id).first()
        new_not = not_data.get('notification')
        if new_not:
            curr_notification.notification = new_not
            db.session.commit()
            return 1
        else:
            return 0
