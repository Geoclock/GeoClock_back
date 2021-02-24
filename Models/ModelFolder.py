from Database import db
from Models.ModelUser import ModelUser


class ModelFolder(db.Model):
    __tablename__ = 'folder'

    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(50))
    created_by_user = db.Column(db.Boolean)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('ModelUser', backref='user.id')

    def __init__(self, folder_name=None,
                 created_by_user=False,
                 creator=None):
        self.folder_name = folder_name
        self.created_by_user = created_by_user
        self.creator = creator

    def add_folder_to_db(self):
        db.session.add(self)
        db.session.commit()
        user = ModelUser.read_from_db(user_id=self.creator_id)
        if not user.default_folder_id:
            user.default_folder_id = self.id
            user.commit_changes_to_db()

    """Перевірка на те чи дана папка дефолтна"""

    def is_default_folder(self):
        user = ModelUser.read_from_db(user_id=self.creator_id)
        if self.id == user.default_folder_id:
            return True
        return False

    @classmethod
    def read_from_db(cls, folder_id=None,
                     user_id=None):
        if folder_id:
            return ModelFolder.query.filter_by(id=folder_id).first()
        if user_id:
            return ModelFolder.query.filter_by(creator_id=user_id).all()
        return None

    @classmethod
    def delete_from_db(cls, folder_id=None, folder=None):
        folder_to_delete = None
        if folder_id:
            folder_to_delete = ModelFolder.read_from_db(folder_id=folder_id)
        if folder:
            folder_to_delete = folder
        if not folder_to_delete:
            return 0
        db.session.delete(folder_to_delete)
        db.session.commit()
        return 1

    def edit_db(self, new_folder_name=None):
        self.folder_name = new_folder_name
        db.session.commit()
