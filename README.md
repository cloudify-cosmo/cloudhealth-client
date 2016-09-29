Cloudhealth REST Client
=======================

[![Build Status](https://travis-ci.org/cloudify-cosmo/cloudhealth-client.svg?branch=master)](https://travis-ci.org/cloudify-cosmo/cloudhealth-client)
[![PyPI](http://img.shields.io/pypi/dm/cloudhealth-client.svg)](http://img.shields.io/pypi/dm/cloudhealth-client.svg)
[![PypI](http://img.shields.io/pypi/v/cloudhealth-client.svg)](http://img.shields.io/pypi/v/cloudhealth-client.svg)

[WIP!]

This is a Python REST Client for the wonderful Cloudhealth service which also provides a CLI to easily retrieve information.

## Installation

```shell
pip install cloudhealth

# latest development version
pip install http://github.com/cloudify-cosmo/cloudhealth-client/archive/master.tar.gz
```


## CLI Usage

Note that currently, you can only pass the `--api-key` after the main function.
i.e. `cloudhealth --api-key ... SUBCOMMANDS [ARGUMENT] [OPTIONS]

Prior to using most of the reports (cost and usage) you'll need to create some personal reports.
One to get cost per account per month (for `account-history`) and can be past using `--report-id` or CLOUDHEALTH_ACCOUNTS_HISTORY_REPORT system var
The other for service history and days usage, passed using `--report-id` of CLOUDHEALTH_DAYS_COST_REPORT system var


```shell
# Exploring the main function
$ cloudhealth
Usage: cloudhealth [OPTIONS] COMMAND [ARGS]...

  A CloudHealth Command Line Interface

  You can set the `CLOUDHEALTH_API_KEY` environment variable instead of
  using the `--api-key` everytime.

Options:
  --api-key TEXT  The API key to your Cloudhealth Account  [required]
  -h, --help      Show this message and exit.

Commands:
  accounts  Retrieve accounts related information
  assets    Retrieve assets related information
  cost      Retrieve cost related information
  reports   Retrieve report related information
  usage     Retrieve resource usage related information

# Geting the current costs for all AWS account
$ cloudhealth cost current
  {
      "Blended": null, 
      "Total": $$$$$, 
      "ec2training": $$$$
  }
  
# Get costs per account for a specific month
$ cloudhealth cost account-history -m 2016-03
  {
      "Blended": null, 
      "Total": $$$$, 
      "ec2training": $$$$
  }

# Get the cost for all services in AWS for a specific month
$ cloudhealth cost service-history -m 2016-03
  {
      "APN Annual Program Fee": null, 
      "EBS - I/O": 32.67424689999989, 
      "S3 - Storage": 131.25546249, 
      "S3 - Transfer": 72.95783235000017
  }

# Fetch AWS Instance assets and include info about parent accounts
$ cloudhealth assets get AwsInstance -i account
  {
          "account": {
              "access_enabled": null, 
              "account_type": "Linked", 
              "amazon_name": null, 
              "auth_type": 0, 
              "aws_config_bucket_name": null, 
              "aws_config_prefix": null, 
              "base_state": "Unknown", 
              "cloudtrail_bucket_name": "cloudify-production-event", 
              "cloudtrail_prefix": null, 
              "cloudwatch_runtime": 24, 
              "cluster_name": "<NAME>"
          }, 
          "architecture": "x86_64", 
          "attached_ebs": 8,  
          "vpc_id": "vpc-#####"
      }
```

## Python API Example

Check out the code for all available API calls until full docs are ready.

```python
from cloudhealth import client

ch = client.CloudHealth(api_key='Ali23melAS$E#@$Im3lsim1!')

# Get AWS instance usage for yesterday (currently only AWS is supported)
ch.usage.get(resource_type='instance')
...

79.79166666666666

# Get current cost of all service in all AWS-Accounts
ch.cost.get_current(account_type='AWS-Account')
...

9676.619999999908

```


## Testing

Currently, there aren't any... but soon.. there will be...
...
..

## Contributions..

..are always welcome.