class AccountsClient(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client.get('aws_accounts')
        return response['aws_accounts']
