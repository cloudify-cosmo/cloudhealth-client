########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import requests
from requests.packages import urllib3

from .cost import CostClient
from .usage import UsageClient
from .assets import AssetsClient
from .reports import ReportsClient


DEFAULT_CLOUDHEALTH_API_URL = 'https://chapi.cloudhealthtech.com/'

urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)


class HTTPClient(object):
    def __init__(self,
                 endpoint,
                 api_key,
                 headers=None,
                 query_params=None,
                 cert=None,
                 trust_all=False):
        self.endpoint = endpoint
        self.api_key = api_key
        self.headers = headers.copy() if headers else {}
        if not self.headers.get('Content-type'):
            self.headers['Content-type'] = 'application/json'

    def get(self,
            uri,
            data=None,
            params=None,
            headers=None,
            _include=None,
            expected_status_code=200,
            stream=False):
        url = '{0}{1}api_key={2}'.format(self.endpoint, uri, self.api_key)
        response = requests.get(url,
                                data=data,
                                params=params,
                                headers=headers,
                                stream=stream)
        if response.status_code != 200:
            raise RuntimeError(
                'Request to {0} failed! (HTTP Error Code: {1})'.format(
                    url, response.status_code))
        return response.json()


class CloudHealth(object):
    def __init__(self, api_key, endpoint=DEFAULT_CLOUDHEALTH_API_URL):
        self._client = HTTPClient(endpoint, api_key)
        self.reports = ReportsClient(self._client)
        self.assets = AssetsClient(self._client)
        self.cost = CostClient(self._client)
        self.usage = UsageClient(self._client)
