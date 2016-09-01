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

from cloudhealth import client, utils


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


@cost.command('list')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='Type of accounts to list [default: AWS-Account]')
@click.option('-r',
              '--resource-type',
              default='accounts',
              help='Resource type to list')
@click.pass_context
def list(ctx, account_type, resource_type):
    """List possible objects for cost function.

    List all accounts, services and dates.
    """
    cost = ctx.obj['client']
    if resource_type == 'accounts':
        print(utils._format_json(cost.list_accounts(account_type)))
    elif resource_type == 'services':
        print(utils._format_json(cost.list_service()))
    elif resource_type == 'dates':
        print(utils._format_json(cost.list_months(account_type)))


@cost.command('current')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-d',
              '--by-days',
              default=False,
              is_flag=True,
              help='Get current cost by days')
@click.option('-S',
              '--by-service',
              default=False,
              is_flag=True,
              help='Get current cost by service')
@click.option('-i',
              '--instance',
              default=False,
              is_flag=True,
              help='Get current cost for instances only')
@click.option('-n',
              '--account-name',
              help='The account to get the cost for')
@click.option('-id',
              '--report_id',
              help='Get current cost of perspective group from a report This only works in 2 dimensions reports')
@click.pass_context
def current_cost(ctx, account_type, by_days, by_service, instance, account_name, report_id):
    """Retrieve current cost for all accounts.

    Using the -S flag will get you a list of current services costs.
    Specifying an account name will get the current cost for that account only.
    Specifying an account type will get the cost to all accounts of that type.
    Omitting both will get the total cost of all accounts.

    Specifying a report id will get you the current cost based on filter and grouping done in web console
    """
    cost = ctx.obj['client']
    if instance:
        print(cost.get_cost_for_instances())[utils._get_yesterdays_date()]
    elif by_days:
        print(cost.get_current_by_days())[utils._get_yesterdays_date()]
    elif by_service:
        print(utils._format_json(cost.get_current_by_services()))
    elif report_id:
        print(utils._format_json(cost.get_custom_report(report_id)))
    elif account_name:
        print(cost.get_current_by_accounts(account_type, account_name)[account_name])
    else:
        print(utils._format_json(cost.get_current_by_accounts(account_type, account_name)))



@cost.command('account-history')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-n',
              '--account-name',
              help='The account to get the cost for')
@click.option('-m',
              '--month',
              # default=utils._get_last_month,
              help='Sum of cost for the last month [default: Last Month]')
@click.pass_context
def account_history(ctx, account_type, account_name, month):
    """Retrieve cost history by account.

    Specifying an account name will get the cost for the previous month.
    Specifying an account type will get the cost to all accounts of that type.
    Omitting both will get the total cost for previous month.
    """
    cost = ctx.obj['client']
    if account_name and month:
        full_history = cost.account_history(account_type)[month]
        print full_history[account_name]
    elif account_name:
        full_history = cost.account_history(account_type)
        for each_month, account in full_history.iteritems():
            print each_month, account[account_name]
    elif month:
        full_history = cost.account_history(account_type)[month]
        for name, amount in full_history.iteritems():
            print name, amount
    else:
        full_history = cost.account_history(account_type)
        print(utils._format_json(full_history))


@cost.command('service-history')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-i',
              '--instance',
              default=False,
              is_flag=True,
              help='Get current cost for instances only')
@click.option('-s',
              '--service',
              help='The service to get the cost for')
@click.option('-m',
              '--month',
              # default=utils._get_last_month,
              help='Sum of cost for the last month [default: Last Month]')
@click.pass_context
def service_history(ctx, account_type, service, month, instance):
    """Retrieve cost history by service.

    Specifying a service will get the cost for the previous month.
    Specifying a service and month will get the cost for the month and service.
    Omitting both will get a dict of services cost for previous month.
    """
    cost = ctx.obj['client']
    if month and service:
        full_history = cost.service_history()[month]
        print service, full_history[service]
    elif service:
        full_history = cost.service_history()
        for each_month, service_cost in full_history.iteritems():
            print each_month, service_cost[service]
    elif month:
        full_history = cost.service_history()[month]
        for each_month, service_cost in full_history.iteritems():
            print each_month, service_cost
    elif instance:
        print(utils._format_json(cost.get_cost_for_instances()))
    else:
        full_history = cost.service_history()
        print(utils._format_json(full_history))



@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def usage(ctx):
    """Retrieve resource usage related information
    """
    ctx.obj['client'] = ctx.obj['client'].usage

@usage.command('list')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.pass_context
def list_services(ctx, account_type):
    """Retrieve list of usage resources
    """
    usage = ctx.obj['client']
    print(utils._format_json(usage.list_services(account_type)))

@usage.command('get')
@click.argument('resource-type')
@click.option('-d',
              '--date',
              default=utils._get_yesterdays_date,
              help='Resource usage per day [defaults to yesterday]')
@click.pass_context
def get_usage(ctx, resource_type, date):
    """Retrieve usage statistics by day and resource type.

    Specifying Date will get you the usage for that day.
    Specifying Resource type will get you the usage for a particular resources by date.
    Omitting date will get you the usage for yesterday.
    """
    usage = ctx.obj['client']
    if date == 'all':
        print(usage.get(resource_type=resource_type, date=date))
    elif date:
        print(usage.get(resource_type=resource_type, date=date)[date])
    else:
        print(usage.get(resource_type=resource_type, date=utils._get_yesterdays_date))


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
@click.argument('object-name')
@click.pass_context
def get_asset(ctx, object_name):
    """Retrieve a specific asset.
    """
    assets = ctx.obj['client']
    # print(utils._format_json(assets.get(object_name)))
    print(utils._format_json(assets.get(object_name)))


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
