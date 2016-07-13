class AssetsClient(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        assets = []

        uri = '/api.json'
        assets = self.client.get(uri)
        return assets

    def get(self, object_name):

        uri = '/api/{0}.json'.format(object_name)
        # if object_name not in self.list():
        #     raise exceptions.CloudHealthError(
        #         'Object {0} does not exist'.format(object_name))

        asset = self.client.get(uri)
        return asset
