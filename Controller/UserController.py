from Models.ModelUser import ModelUser

class UserController(object):

    def __init__(self, model_user=ModelUser()):
        self.model_user = model_user

    def create(self, user_data=None):
        self.model_user.user_login = user_data.get('login')
        self.model_user.user_password = user_data.get('password')
        self.model_user.add_users_to_db()
        if self.model_user.user_login != None and self.model_user.user_password != None:
            return 1
        else:
            return 0

    def read(self, user_id=None):
        self.model_user.read_from_db_(user_id)
        return self.model_user