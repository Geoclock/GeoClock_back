from Database import db
from Models.ModelUser import ModelUser


class ModelNotification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(200), nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('ModelUser', backref='user')

    def __init__(self, notification=None,
                 creator=None,
                 radius=None):
        self.notification = notification
        self.creator = creator
        self.radius = radius

    def add_notification_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read_from_db(cls, not_id=None,
                     user_id=None):
        if not_id:
            return ModelNotification.query.filter_by(id=not_id).first()
        if user_id:
            return ModelNotification.query.filter_by(creator_id=user_id).all()
        return None

    @classmethod
    def delete_from_db(cls, not_id=None):
        if not_id:
            note_to_delete = ModelNotification.read_from_db(not_id=not_id)
            if note_to_delete:
                db.session.delete(note_to_delete)
                db.session.commit()
        return 1

    def edit_db(self, new_notification=None, new_radius=None):
        if new_notification:
            self.notification = new_notification
        if new_radius:
            self.radius = new_radius
        db.session.commit()
