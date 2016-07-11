class AccountsClient(object):
    CURRENT_COST_URL = '/olap_reports/cost/current'

    def __init__(self, client):
        self.client = client

    def list(self, type=None):
        response = self.client.get(self.CURRENT_COST_URL)

        list_of_accounts = []
        accounts_list = response['dimensions'][0]["AWS-Account"]

        for account in accounts_list:
            label = account['label']
            list_of_accounts.append(label.encode('ascii'))

        return list_of_accounts