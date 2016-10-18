# import os
# import time
import json
# import shlex
# import base64
# import shutil
# import external_module
import pytest

from mock import mock, patch, MagicMock
from cloudhealth import client, utils

# import click.testing as clicktest


ch = client.CloudHealth('')


def test_time_format():
    assert type(utils._get_yesterdays_date()) is str

@pytest.fixture
def FULL_JSON():
    return {'data': [[[200]]],
            'dimensions': [{'AWS-Account': [{'label': 'test-account'}]},
                           {'AWS-Service-Category': [{'label': 'EC2 - Compute'}]}]}

@pytest.fixture
def MONTH_LIST():
    return {'dimensions': [{'time': [{'label': '2016-03'}]}]}

@patch('cloudhealth.client.HTTPClient.get', return_value=FULL_JSON())
def test_cost_current(FULL_JSON):

    assert ch.cost.get_current_by_accounts()['test-account'] == 200

@patch('cloudhealth.client.HTTPClient.get', return_value=FULL_JSON())
@patch('cloudhealth.cost.CostClient.list_months', return_value=MONTH_LIST())
def test_cost_account_history(FULL_JSON, MONTH_LIST):

    assert ch.cost.account_history('AWS-Account', 'b')

@patch('cloudhealth.client.HTTPClient.get', return_value=FULL_JSON())
@patch('cloudhealth.cost.CostClient.list_months', return_value=MONTH_LIST())
def test_cost_service_history(FULL_JSON, MONTH_LIST):

    assert ch.cost.service_history('AWS-Account', 'b')