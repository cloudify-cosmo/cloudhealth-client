from . import date


class UsageClient(object):
    USAGE_URL = 'olap_reports/usage/instance'

    def __init__(self, client):
        self.client = client

    def get_usage(self, day=None):
        response = self.client.get(self.USAGE_URL)

        total_usage = []

        date_client = date.DateClient(self.client)
        list_of_days = date_client.list_days()

        costs = response['data']
        for days_usage in costs:
            total_usage.append(days_usage[0][0])

        usage_for_day = dict(zip(list_of_days, total_usage))

        return usage_for_day

        # if account_name:
        #     return cost_by_account[account_name]
        # else:
        #     return cost_by_account['Total']