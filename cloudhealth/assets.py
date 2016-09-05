from . import exceptions

class AssetsClient(object):
    ASSESTS_BASE_URI = '/api/search.json'


    def __init__(self, client):
        self.client = client


    def _instance_assets(self, url):
        total_cost = []
        stopped_count = 0

        for item in url:
            if item['state'] == 'running':
                total_cost.append(item['price_per_month'][1:].encode('ascii'))
                print "ID: " + item['instance_id'] + "  Cost: " + item["price_per_month"]
            elif item['state'] == 'stopped':
                stopped_count = stopped_count + 1

        return "There are {0} stopped Instances in all AWS accounts".format(stopped_count), "The Total projected cost per month for all Instances is: ${0}".format(sum(map(float,total_cost)))

    def _security_assets(self, url):
        count = 0

        for item in url:
            if item['is_active'] and item['ip_ranges'] == 'All':
                count = count + 1

        return "Found {0} SG rules with ALL from ANY".format(count)

    def _elastic_ip_assets(self, url):
        count = 0
        active_count = 0

        for item in url:
            count = count + 1
            if item['private_ip_address']:
                active_count = active_count +1

        return "There are {0} Active EIPs out of {1}".format(active_count,count)

    def list(self):

        uri = '/api.json'
        assets = self.client.get(uri)
        return assets

    def get(self, object_name):

        if object_name not in self.list():
            raise exceptions.CloudHealthError(
            'Object {0} does not exist'.format(object_name))

        url = self.client.get_asset(uri=self.ASSESTS_BASE_URI, asset=object_name)
        if object_name == 'AwsInstance':
            return self._instance_assets(url)

        elif object_name == 'AwsSecurityGroupRule':
            return self._security_assets(url)

        elif object_name == 'AwsElasticIp':
            return self._security_assets(url)

        else:
            return url[0]
