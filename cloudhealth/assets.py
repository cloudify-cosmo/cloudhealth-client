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

        total_cost = []

        url = self.client.get_asset(uri=self.ASSESTS_BASE_URI, asset=object_name)
        if object_name == 'AwsInstance':
            for item in url:
                if item['state'] == 'running':
                    total_cost.append(item['price_per_month'][1:].encode('ascii'))
                    print "ID: " + item['instance_id'] + "  Cost: " + item["price_per_month"]
            print sum(map(float,total_cost))
            return url[0]

        elif object_name == 'AwsSecurityGroupRule':
            count = 0
            for item in url:
                if item['is_active'] and item['ip_ranges'] == 'All':
                    count = count + 1
            print "Found {0} SG rules with ALL from ANY".format(count)
            return url[0]
        else:
            return url[0]
