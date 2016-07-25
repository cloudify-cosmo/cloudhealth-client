from datetime import date, timedelta

def _get_current_month():
    current = date.today()
    return date(current.year, current.month-1, current.day).strftime('%Y-%m')

class CostClient(object):
    CURRENT_COST_URL = '/olap_reports/cost/current'
    ACCOUNTS_HISTORY_COST_URL = '/olap_reports/custom/893353198679'

    def __init__(self, client):
        self.client = client

    def list_months(self, type):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL)

        list_of_months = []
        months = response['dimensions'][0]["time"]

        for month in months:
            label = month['label']
            list_of_months.append(label.encode('ascii'))

        return list_of_months

    def list_accounts(self, account_type):
        response = self.client.get(self.CURRENT_COST_URL)

        list_of_accounts = []
        accounts_list = response['dimensions'][0][account_type]

        for account in accounts_list:
            label = account['label']
            list_of_accounts.append(label.encode('ascii'))

        return list_of_accounts

    def get_current(self, account_type='AWS-Account', account_name=None):
        response = self.client.get(self.CURRENT_COST_URL)

        accounts_total_cost = []

        list_of_aws_accounts = self.list_accounts(account_type)

        costs = response['data']
        for accounts_total in costs:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        if account_name == 'all':
            return cost_by_account
        elif account_name:
            return cost_by_account[account_name]
        else:
            return cost_by_account['Total']

    def cost_history(self,
                     account_type='AWS-Account',
                     account_name='Total',
                     month=_get_current_month()):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL)

        accounts_cost_by_month = []
        list_of_months = self.list_months(self.ACCOUNTS_HISTORY_COST_URL)
        list_of_aws_accounts = self.list_accounts(account_type)

        costs = response['data']
        for list in costs:
            costs_history_by_month = dict(zip(list_of_aws_accounts, list))
            accounts_cost_by_month.append(costs_history_by_month[account_name][0])

        costs_history_for_account = dict(zip(list_of_months,
                                             accounts_cost_by_month))

        return costs_history_for_account[month]