import re

class UsageClient(object):
    USAGE_URL = 'olap_reports/usage?'

    def __init__(self, client):
        self.client = client

    def list_days(self, uri):
        response = self.client.get(uri)

        list_of_days = []
        days = response['dimensions'][0]["time"]

        for day in days:
            label = day['label']
            list_of_days.append(label.encode('ascii'))

        return list_of_days

    def list_services(self, account_type):
        response = self.client.get(self.USAGE_URL)

        list_pf_services = []

        for items in response['links']:
            list_pf_services.append(re.sub('usage/', '', items))

        return list_pf_services

    def get(self, resource_type, date):
        uri = '{0}{1}{2}{3}'.format(self.USAGE_URL[:-1], '/', resource_type, '?')
        response = self.client.get(uri)

        total_usage = []
        list_of_days = self.list_days(uri)

        costs = response['data']
        for days_usage in costs:
            total_usage.append(days_usage[0][0])

        usage_for_day = dict(zip(list_of_days, total_usage))

        return usage_for_day