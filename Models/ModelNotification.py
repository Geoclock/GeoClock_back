from Models.ModelUser import db


class ModelNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)

    def __init__(self, notification=None):
        self.notification = notification

    def add_notification_to_db(self):
        data = ModelNotification(self.notification)
        db.session.add(data)
        db.session.commit()

    def read_from_db_(self, not_id):
        not_ = ModelNotification.query.filter_by(id=not_id).first()
        self.notification = not_.notification