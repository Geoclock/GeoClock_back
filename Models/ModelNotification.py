from Database import db


class ModelNotification(db.Model):
    __tablename__='notification'
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)
    point_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))

    def __init__(self, notification=None, point_id=None):
        self.notification = notification
        self.point_id = point_id

    def add_notification_to_db(self):
        data = ModelNotification(self.notification, self.point_id)
        db.session.add(data)
        db.session.commit()

    def read_from_db_(self, not_id):
        not_ = ModelNotification.query.filter_by(id=not_id).first()
        self.notification = not_.notification
        #self.point_id = not_.point_id
