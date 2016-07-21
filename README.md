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

```shell
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