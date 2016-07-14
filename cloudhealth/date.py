class DateClient(object):
    CURRENT_COST_URL = '/olap_reports/cost/history'
    USAGE_URL = 'olap_reports/usage/instance'

    def __init__(self, client):
        self.client = client

    def list_months(self, type=None):
        response = self.client.get(self.CURRENT_COST_URL)

        list_of_months = []
        months = response['dimensions'][0]["time"]

        for month in months:
            label = month['label']
            list_of_months.append(label.encode('ascii'))

        return list_of_months

    def list_days(self, type=None):
        response = self.client.get(self.USAGE_URL)

        list_of_days = []
        days = response['dimensions'][0]["time"]

        for day in days:
            label = day['label']
            list_of_days.append(label.encode('ascii'))

        return list_of_days
