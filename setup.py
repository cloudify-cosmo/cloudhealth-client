########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
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

from setuptools import setup

setup(
    name='cloudhealth',
    version='0.1.0',
    author='Nir Cohen',
    author_email='nir36g@gmail.com',
    packages=['cloudhealth'],
    license='LICENSE',
    description='A REST Client for Cloudhealth',
    entry_points={
        'console_scripts': [
            'cloudhealth = cloudhealth.cli:_cloudhealth'
        ]
    },
    install_requires=[
        'click==6.6',
        'requests==2.7.0',
        'click_didyoumean==0.0.3',
    ]
)
