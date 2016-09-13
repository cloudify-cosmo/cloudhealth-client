from . import exceptions

class AssetsClient(object):
    ASSETS_BASE_URI = 'api/search.json?name={0}&include={1}&'

    def __init__(self, client):
        self.client = client

    def list(self):
        assets = []

        uri = '/api.json?'
        assets = self.client.get(uri)
        return assets

    def get(self, object_name, include):

        if object_name not in self.list():
            raise exceptions.CloudHealthError(
            'Object {0} does not exist'.format(object_name))

        response = self.client.get(uri=self.ASSETS_BASE_URI.format(object_name, include))


        return response