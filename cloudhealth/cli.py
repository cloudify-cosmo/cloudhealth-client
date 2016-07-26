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

import click

from click_didyoumean import DYMGroup

from cloudhealth import client


CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower(),
    ignore_unknown_options=True)


@click.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.option('--api-key',
              required=True,
              envvar='CLOUDHEALTH_API_KEY',
              help='The API key to your Cloudhealth Account')
@click.pass_context
def _cloudhealth(ctx, api_key):
    """A CloudHealth Command Line Interface

    You can set the `CLOUDHEALTH_API_KEY` environment variable instead
    of using the `--api-key` everytime.
    """
    # TODO: Expose `--api-key` to all commands.
    ctx.obj = {}
    ctx.obj['client'] = client.CloudHealth(api_key)


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def cost(ctx):
    """Retrieve cost related information
    """
    ctx.obj['client'] = ctx.obj['client'].cost


@cost.command('current')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-n',
              '--account-name',
              help='The account to get the cost for')
@click.pass_context
def current_cost(ctx, account_type, account_name):
    """Retrieve current cost.

    Specifying an account name will get the current cost for that account only
    Specifying an account type will get the cost to all accounts of that type.
    Omitting both will get the total cost of all accounts.
    """
    cost = ctx.obj['client']
    print(cost.get_current(account_type, account_name))


@cost.command('history')
@click.option('--history-report-id',
              # required=True,
              envvar='CLOUDHEALTH_HISTORY_REPORT_ID',
              help='Cloudhealth history reports ID Number')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-n',
              '--account-name',
              default='Total'.encode('ascii'),
              help='The account to get the cost for')
@click.option('-s',
              '--service',
              default='Total'.encode('ascii'),
              help='The service cost')
@click.option('-m',
              '--month',
              help='Sum of cost for the last month [default: Last Month]')
@click.pass_context
def cost_history(ctx, history_report_id, account_type, account_name, service, month):
    """Retrieve Cost History.

    You must create a report to reflect your various accounts.
    In "Cost History", change the category from "Service Item" to "Accounts".
    Save the report and use the ID from the url as `--history_report_id`

    You can set the `CLOUDHEALTH_HISTORY_REPORT_ID` environment variable instead
    of using the `--history-report-id` everytime.

    Specifying an account name will get the cost history for that account only for previous month.
    Specifying an account name and month will get the cost history for month and account.
    Specifying an account type will get the cost to all accounts of that type.
    Omitting all will get the cost history of all accounts for previous month.
    """
    cost = ctx.obj['client']
    if month:
        print(cost.cost_history(history_report_id,
                                account_type,
                                account_name=account_name,
                                service=service,
                                month=month))
    else:
        print(cost.cost_history(history_report_id,
                                account_type,
                                account_name=account_name,
                                service=service))


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def usage(ctx):
    """Retrieve resource usage related information
    """
    ctx.obj['client'] = ctx.obj['client'].usage


@usage.command('get')
@click.argument('resource-type')
@click.option('-d',
              '--date',
              help='Resource usage per day [defaults to yesterday]')
@click.pass_context
def get_usage(ctx, resource_type, date):
    """Retrieve usage statistics by day and resource type.

    Specifying Date will get you the usage for that day.
    Specifying Resource type will get you the usage for a particular resources
    by date.
    Omitting date will get you the usage for yesterday.
    """
    usage = ctx.obj['client']
    if date and resource_type:
        print(usage.get(resource_type=resource_type, date=date))
    elif resource_type:
        print(usage.get(resource_type=resource_type))
    elif date:
        print(usage.get(date=date))
    else:
        print(usage.get())


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def reports(ctx):
    """Retrieve report related information
    """
    ctx.obj['client'] = ctx.obj['client'].reports


@reports.command('list')
@click.option('-t',
              '--topic',
              help='The topic to get the reports for')
@click.pass_context
def list_reports(ctx, topic):
    """List all reports

    Specifying a topic will get the reports only for that topic.
    """
    reports = ctx.obj['client']
    reports_list = reports.list(topic)
    for report in reports_list:
        print(report)


@reports.command('list-topics')
@click.pass_context
def list_topics(ctx):
    """List all topics
    """
    reports = ctx.obj['client']
    topics_list = reports.topics()
    for topic in topics_list:
        print(topic)


@reports.command(name='get')
@click.option('-i',
              '--id',
              default=None,
              help='The ID of the report')
@click.option('-t',
              '--topic',
              default=None,
              help='The topic of the report')
@click.option('-n',
              '--report-name',
              default=None,
              help='The name of the report')
@click.pass_context
def get_report(ctx, id, topic, report_name):
    """Retrieve a specific report
    """
    reports = ctx.obj['client']
    print(reports.get(id, topic, report_name))


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def assets(ctx):
    """Retrieve assets related information
    """
    ctx.obj['client'] = ctx.obj['client'].assets


@assets.command(name='list')
@click.pass_context
def list_assets(ctx):
    """List all assets
    """
    assets = ctx.obj['client']
    assets_list = assets.list()
    for asset in assets_list:
        print(asset)


@assets.command(name='get')
@click.argument('asset-name')
@click.pass_context
def get_asset(ctx, object_name):
    """Retrieve a specific asset.
    """
    assets = ctx.obj['client']
    print(assets.get(object_name))


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def accounts(ctx):
    """Retrieve accounts related information
    """
    ctx.obj['client'] = ctx.obj['client'].accounts


@accounts.command(name='list')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.pass_context
def list_accounts(ctx, account_type):
    accounts = ctx.obj['client']
    accounts_list = accounts.list(account_type)
    for account in accounts_list:
        print(account)
