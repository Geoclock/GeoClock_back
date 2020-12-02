from Models.ModelNotification import ModelNotification


class NotificationController(object):
    def __init__(self, model_notification=ModelNotification()):
        self.model_notification = model_notification

    def create(self, not_data=None):
        self.model_notification.notification = not_data.get('not')

        self.model_notification.add_notification_to_db()

        if self.model_notification.notification != None:
            return 1
        else:
            return 0

    def read(self, not_id=None):
        self.model_notification.read_from_db_(not_id)
        return self.model_notification