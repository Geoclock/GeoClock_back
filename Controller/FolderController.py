from Models.ModelFolder import ModelFolder
from Models.ModelUser import ModelUser
from Controller.GeolocationController import GeolocationController


class FolderController(object):

    @classmethod
    def create(cls, folder_data=None, user_id=None):
        folder_name = folder_data.get('name')
        if user_id:
            user = ModelUser.read_from_db(user_id=user_id)
        else:
            return 0
        if not user:
            return 0
        created_by_user = False
        if folder_data.get('created_by_user'):
            created_by_user = True
        Folder = ModelFolder(folder_name=folder_name,
                             created_by_user=created_by_user,
                             creator=user)
        Folder.add_folder_to_db()
        return 1

    @classmethod
    def read(cls, read_data=None, user_id=None):
        try:
            return ModelFolder.read_from_db(folder_id=read_data.get('folder_id'))
        except:
            if user_id:
                return ModelFolder.read_from_db(user_id=user_id)
        return None

    """оформляємо словник для повернення
        за індекс береться айді папки, в самій комірці міститься об'єкт зв'язаної геолокації"""

    @classmethod
    def read_folders_geo(cls, folder_list=None):
        list = {}
        for folder in folder_list:
            list[folder.id] = GeolocationController.read(folder_id=folder.id)
        return list

    @classmethod
    def delete(cls, folder_id=None):
        folder_to_delete = ModelFolder.read_from_db(folder_id=folder_id)
        if folder_to_delete:
            folder_id = folder_to_delete.id
            # delete included geolocation
            geo_list = GeolocationController.read(folder_id=folder_id)
            for geo in geo_list:
                GeolocationController.delete(geo_id=geo.id)
            ModelFolder.delete_from_db(folder=folder_to_delete)
            return 1
        return 0

    @classmethod
    def edit(cls, folder_id=None, folder_data=None):
        new_folder_name = folder_data.get('name')
        edit_folder = ModelFolder.read_from_db(folder_id=folder_id)
        if not edit_folder:
            return 0
        edit_folder.edit_db(new_folder_name=new_folder_name)
        return 1
