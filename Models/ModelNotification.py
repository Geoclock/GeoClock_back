from Database import db
from Models.ModelGeolocation import ModelGeolocation


class ModelNotification(db.Model):

    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)
    # id of point this notification belongs to
    point_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))
    point = db.relationship('ModelGeolocation', backref='geolocation', uselist=False)

    def __init__(self, notification=None, point=None):
        self.notification = notification
        self.point = point

    def add_notification_to_db(self):
        db.session.add(self)
        db.session.commit()

    def read_from_db_(self, not_id):
        read_notification = ModelNotification.query.filter_by(id=not_id).first()
        self.notification = read_notification.notification
    
    def delete_from_db_(self):
        db.session.delete(self)
        db.session.commit()

    def edit_db(self, geo_id=None):
        edit_geo = ModelGeolocation.query.filter_by(id=geo_id).first()
        self.radius = edit_geo.new_radius
        db.session.commit()