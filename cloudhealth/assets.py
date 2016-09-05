from . import exceptions

class AssetsClient(object):
    ASSESTS_BASE_URI = '/api/search.json'


    def __init__(self, client):
        self.client = client

    def list(self):
        assets = []

        uri = '/api.json'
        assets = self.client.get(uri)
        return assets

    def get(self, object_name):

        if object_name not in self.list():
            raise exceptions.CloudHealthError(
            'Object {0} does not exist'.format(object_name))

        url = self.client.get_asset(uri=self.ASSESTS_BASE_URI, asset=object_name)
        return url