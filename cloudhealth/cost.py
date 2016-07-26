from . import utils

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

        cost_response = response['data']
        for accounts_total in cost_response:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        if account_name == 'all':
            return cost_by_account
        elif account_name:
            return cost_by_account[account_name]
        else:
            return cost_by_account['Total']

    def history(self,
                     account_type='AWS-Account',
                     account_name='Total',
                     month=utils._get_last_month()):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL)

        accounts_cost_by_month = []
        list_of_months = self.list_months(self.ACCOUNTS_HISTORY_COST_URL)
        list_of_aws_accounts = self.list_accounts(account_type)

        cost_response = response['data']
        for list in cost_response:
            costs_history_by_month = dict(zip(list_of_aws_accounts, list))
            accounts_cost_by_month.append(costs_history_by_month[account_name][0])

        cost_history_for_account = dict(zip(list_of_months,
                                             accounts_cost_by_month))

        return cost_history_for_account
        # if month == 'all':
        #     return costs_history_for_account
        # else:
        #     return costs_history_for_account[month]