from datetime import date, timedelta


def _get_yesterdays_date():
    return (date.today() - timedelta(1)).strftime('%Y-%m-%d')


class UsageClient(object):
    USAGE_URL = 'olap_reports/usage'

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

    def get(self, resource_type, date=_get_yesterdays_date()):
        uri = self.USAGE_URL + '/' + resource_type
        response = self.client.get(uri)

        total_usage = []

        list_of_days = self.list_days(uri)

        costs = response['data']
        for days_usage in costs:
            total_usage.append(days_usage[0][0])

        usage_for_day = dict(zip(list_of_days, total_usage))

        return usage_for_day[date]