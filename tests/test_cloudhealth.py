from mock import patch
from cloudhealth import client, utils


class TestingUtils():
    def test_time_day_format(self):
        assert type(utils._get_yesterdays_date()) is str

    def test_time_month_format(self):
        assert type(utils._get_last_month()) is str


class Testing_Cost_Client():
    ch = client.CloudHealth('')

    FULL_JSON = {'data': [[[200]]],
                 'dimensions': [{
                     'AWS-Account': [{'label': 'test-account'}]},
                                {'AWS-Service-Category': [{
                                    'label': 'EC2 - Compute'}]}]}

    MONTH_LIST = {'dimensions': [{'time': [{'label': '2016-03'}]}]}

    mock_get = patch('cloudhealth.client.HTTPClient.get',
                     return_value=FULL_JSON)
    mock_list_month = patch('cloudhealth.cost.CostClient.list_months',
                            return_value=MONTH_LIST)

    @mock_get
    def test_cost_current(self, FULL_JSON):
        assert self.ch.cost.get_current_by_accounts()['test-account'] == 200

    @mock_get
    @mock_list_month
    def test_cost_account_history(self, FULL_JSON, MONTH_LIST):

        assert self.ch.cost.account_history(
                'AWS-Account', 'b')['dimensions']['test-account'] == 200

    @mock_get
    @mock_list_month
    def test_cost_service_history(self, FULL_JSON, MONTH_LIST):
        assert self.ch.cost.service_history(
                'AWS-Account', 'b')['dimensions']['EC2 - Compute'] == 200
