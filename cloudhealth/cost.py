# https://chapi.cloudhealthtech.com/olap_reports?api_key=<your api key>


class CostsClient(object):
    def __init__(self, client):
        self.client = client

    def get_current(self, account_name=None):
        uri = '/olap_reports/cost/current'

        report = self.client.get(uri)

        # if account_name return cost for specific account
        # else return cost for all accounts

        return data

    def get_by_month(self, account_name, last=False, filter=None):
        uri = '/olap_reports/cost/history'

        report = self.client.get(uri)

        # same for account_name as above
        # if last is true, return for last month
        # if filter, return according to filter

        return data
