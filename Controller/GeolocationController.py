from Models.ModelGeolocation import ModelGeolocation


class GeolocationController(object):
    def __init__(self, model_geolocation=ModelGeolocation()):
        self.model_geolocation = model_geolocation

    def create(self, geo_data=None):
        self.model_geolocation.latitude = geo_data.get('lat')
        self.model_geolocation.longitude = geo_data.get('lon')
        self.model_geolocation.radius = geo_data.get('radius')

        self.model_geolocation.add_geolocation_to_db()

        if self.model_geolocation.latitude != None and self.model_geolocation.longitude != None and self.model_geolocation.radius != None:
            return 1
        else:
            return 0

    def read(self, geo_id=None):
        self.model_geolocation.read_from_db_(geo_id)
        return self.model_geolocation