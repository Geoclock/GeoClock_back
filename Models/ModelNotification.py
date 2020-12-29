from Database import db
from Models.ModelGeolocation import ModelGeolocation


class ModelNotification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    # id of point this notification belongs to
    point_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))
    point = db.relationship('ModelGeolocation', backref='geolocation', uselist=False)

    def __init__(self, notification=None, point=None, radius=None):
        self.notification = notification
        self.point = point
        self.radius = radius

    def add_notification_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read_from_db(cls, not_id=None):
        return ModelNotification.query.filter_by(id=not_id).first()

    @classmethod
    def read_list_by_point_from_db(cls, point_id=None):
        return ModelNotification.query.filter_by(point_id=point_id).all()

    @classmethod
    def delete_from_db(cls, not_id=None):
        cls = ModelNotification.read_from_db(not_id=not_id)
        if not cls:
            return 0
        db.session.delete(cls)
        db.session.commit()
        return 1

    def edit_db(self, new_notification=None):
        self.notification = new_notification
        db.session.commit()
