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
@click.option('-rid',
              '--report-id',
              help='The report ID to be used')
@click.option('-r',
              '--resource',
              help='Get current cost by resource')
@click.option('-n',
              '--account-name',
              help='The account to get the cost for')
@click.pass_context
def current_cost(ctx,
                 account_type,
                 report_id,
                 resource,
                 account_name):
    """Retrieve current cost for all accounts.

    Specifying an account name will get the current cost for that account only.
    Specifying an account type will get the cost to all accounts of that type.
    Omitting both will get the total cost of all accounts.

    Specifying a report id will get you the current cost
     based on filters and grouping done in web console
    """
    cost = ctx.obj['client']
    if resource:
        if resource == 'by-service':
            print(utils._format_json(cost.get_current_by_services()))
        elif resource == 'instances':
            print(cost.get_cost_for_instances())[utils._get_yesterdays_date()]
        elif resource:
            all_service = cost.get_current_by_services()
            print all_service[resource]
    elif account_name:
        print(cost.get_current_by_accounts(account_type,
                                           account_name)[account_name])
    elif report_id:
        print(utils._format_json(cost.get_custom_report(report_id)))
    else:
        print(utils._format_json(cost.get_current_by_accounts(account_type,
                                                              account_name)))


@cost.command('account-history')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-rid',
              '--report-id',
              required=True,
              help='The report ID to be used')
@click.option('-n',
              '--account-name',
              help='The account to get the cost for')
@click.option('-d',
              '--by-days',
              default=False,
              is_flag=True,
              help='Get current cost by days')
@click.option('-m',
              '--month',
              help='Cost by month [type "last" for previous month]')
@click.pass_context
def account_history(ctx,
                    account_type,
                    report_id,
                    account_name,
                    by_days,
                    month):
    """Retrieve cost history by account.

    Specifying an account name will get the cost for the previous month.
    Specifying a specific month will get the month cost per account.
    Omitting both will get the total cost for previous month.
    Using the --by-days flag will get the total cost per day.

    Specifying a report id will get you the current cost
     based on filter and grouping done in web console.
    """
    cost = ctx.obj['client']
    if account_name and month:
        if month == 'last':
            full_history = cost.account_history(
                    account_type,
                    report_id)[utils._get_last_month()]
            print full_history[account_name]
        else:
            full_history = cost.account_history(
                    account_type,
                    report_id)[month]
            print full_history[account_name]
    elif month:
        if month == 'last':
            full_history = cost.account_history(
                    account_type,
                    report_id)[utils._get_last_month()]
            dict = {}
            for name, amount in full_history.iteritems():
                dict[name] = amount
            print(utils._format_json(dict))
        else:
            full_history = cost.account_history(
                    account_type,
                    report_id)[month]
            dict = {}
            for name, amount in full_history.iteritems():
                dict[name] = amount
            print(utils._format_json(dict))
    elif account_name:
        full_history = cost.account_history(
                account_type,
                report_id)
        for each_month, account in full_history.iteritems():
            print each_month, account[account_name]
    elif by_days:
        print(utils._format_json(cost.get_cost_by_days(report_id)))
    else:
        full_history = cost.account_history(
                account_type,
                report_id)
        print(utils._format_json(full_history))


@cost.command('service-history')
@click.option('-t',
              '--account-type',
              default='AWS-Account',
              help='The type to get the cost for [default: AWS-Account]')
@click.option('-s',
              '--service',
              help='The service to get the cost for')
@click.option('-rid',
              '--report-id',
              required=False,
              help='The report ID to be used')
@click.option('-m',
              '--month',
              help='Cost by month [type "last" for previous month]')
@click.pass_context
def service_history(ctx,
                    account_type,
                    report_id,
                    service,
                    month):
    """Retrieve cost history by service.

    Specifying a service will get the cost for the previous month.
    Specifying a service and month will get the cost for the month and service.
    Omitting both will get a full dict of services cost and months.

    --report-id flag can by ignored because these roprots run against
    default CloudHealth reports
    """
    cost = ctx.obj['client']
    if month and service:
        if month == "last" and service:
            full_history = cost.service_history(
                    account_type,
                    report_id)[utils._get_last_month()]
            print service, full_history[service]
        else:
            full_history = cost.service_history(
                    account_type,
                    report_id)[month]
            print service, full_history[service]
    elif month:
        if month == 'last':
            full_history = cost.service_history(
                    account_type,
                    report_id)[utils._get_last_month()]
            dict = {}
            for service_name, service_cost in full_history.iteritems():
                dict[service_name] = service_cost
            print(utils._format_json(dict))
        else:
            full_history = cost.service_history(
                    account_type,
                    report_id)[month]
            dict = {}
            for service_name, service_cost in full_history.iteritems():
                dict[service_name] = service_cost
            print(utils._format_json(dict))
    elif service:
        full_history = cost.service_history(
                account_type,
                report_id)
        dict = {}
        for month, service_cost in full_history.iteritems():
            dict[month] = service_cost[service]
        print(utils._format_json(dict))
    else:
        full_history = cost.service_history(
                account_type,
                report_id)
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
    """Retrieve the list of resource types
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

    RESOURCE_TYPE The name the resource you want the usage stat for

    Specifying Date will get you the usage for that day.
    Omitting date will get you the usage for yesterday.
    """
    usage = ctx.obj['client']
    if date == 'all':
        print(utils._format_json(usage.get(resource_type=resource_type,
                                           date=date)))
    elif date:
        print(usage.get(resource_type=resource_type,
                        date=date)[date])
    else:
        print(usage.get(resource_type=resource_type,
                        date=utils._get_yesterdays_date))


@_cloudhealth.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=DYMGroup)
@click.pass_context
def reports(ctx):
    """Retrieve report related information
    """
    ctx.obj['client'] = ctx.obj['client'].reports


@reports.command('list')
@click.pass_context
def list_reports(ctx):
    """List all reports
    """
    reports = ctx.obj['client']
    print(utils._format_json(reports.list()))


@reports.command('list-topics')
@click.pass_context
def list_topics(ctx):
    """List all topics
    """
    reports = ctx.obj['client']
    topics_list = reports.topics()
    for topic in topics_list:
        print(topic)


@reports.command('get')
@click.option('-rid',
              '--report-id',
              required=True,
              help='The report ID to be used')
@click.pass_context
def get_report(ctx, report_id):
    """Retrieve a specific report by ID
    Will work on 2-demention reports only
    """
    reports = ctx.obj['client']
    print(utils._format_json(reports.get(report_id)))


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
@click.option('-i',
              '--include',
              default=None,
              help='Asset related ')
@click.pass_context
def get_asset(ctx, object_name, include):
    """Retrieve a specific set of assets.
    Use --include flag to get a referance for the asset.
    """
    assets = ctx.obj['client']
    print(utils._format_json(assets.get(object_name, include)))
