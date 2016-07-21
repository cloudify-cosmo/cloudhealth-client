from . import accounts


class CostClient(object):
    CURRENT_COST_URL = '/olap_reports/cost/current'
    HISTORY_COST_URL = '/olap_reports/cost/history'

    def __init__(self, client):
        self.client = client

    def list_months(self, type=None):
        response = self.client.get(self.HISTORY_COST_URL)

        list_of_months = []
        months = response['dimensions'][0]["time"]

        for month in months:
            label = month['label']
            list_of_months.append(label.encode('ascii'))

        return list_of_months

    def get_current(self, account_name=None, account_type='AWS-Account'):
        response = self.client.get(self.CURRENT_COST_URL)

        accounts_total_cost = []

        accounts_client = accounts.AccountsClient(self.client)
        list_of_aws_accounts = accounts_client.list(account_type)

        costs = response['data']
        for accounts_total in costs:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        if account_name:
            return cost_by_account[account_name]
        else:
            return cost_by_account['Total']
