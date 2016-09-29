class CostClient(object):
    CURRENT_COST_URL = 'olap_reports/cost/current?'
    INSTANCE_COST_URL = 'olap_reports/cost/current/instance?'
    HISTORY_COST_URL = 'olap_reports/cost/history?'
    CUSTOM_REPORT_URL = 'olap_reports/custom/{0}?'
    ACCOUNTS_HISTORY_COST_URL = 'olap_reports/custom/{0}?'
    DAYS_COST_URL = 'olap_reports/custom/{0}?'

    def __init__(self, client):
        self.client = client

    def __work_on_data(self, data, list_name, depth):
        orig_data =  data[list_name]
        for item in orig_data:
            print item[depth]

    def list_days(self, url):
        response = self.client.get(url)

        list_of_days = []
        # ADD handle to different responses
        # something is broken here since I made the change to move the report ID
        # I need to check all the function to confirm it all works
        if url == self.DAYS_COST_URL:
            days = response['dimensions'][1]["time"]
        else:
            days = response['dimensions'][1]["time"]

        for day in days:
            label = day['label']
            list_of_days.append(label)

        return list_of_days

    def list_months(self, uri, report_id):
        response = self.client.get(uri.format(report_id))

        list_of_months = []
        months = response['dimensions'][0]["time"]

        for month in months:
            label = month['label']
            list_of_months.append(label.encode('ascii'))

        return list_of_months

    def list_accounts(self, account_type):
        response = self.client.get(self.CURRENT_COST_URL)

        list_of_accounts = []
        accounts_list = response['dimensions'][0][account_type]

        for account in accounts_list:
            label = account['label']
            list_of_accounts.append(label.encode('ascii'))

        return list_of_accounts

    def list_service(self, account_type='AWS-Service-Category'):

        response = self.client.get(self.HISTORY_COST_URL)

        list_of_services = []
        service_list = response['dimensions'][1][account_type]

        for service in service_list:
            label = service['label']
            list_of_services.append(label.encode('ascii'))

        return list_of_services

    def list_groups(self, report_id):

        response = self.client.get(self.CUSTOM_REPORT_URL.format(report_id))

        list_of_groups = []
        for group_name in response['dimensions'][0]:
            pass
        group_list = response['dimensions'][0][group_name]

        for service in group_list:
            label = service['label']
            list_of_groups.append(label.encode('ascii'))


        return list_of_groups

    def get_current_by_accounts(self, account_type='AWS-Account', account_name=None):
        response = self.client.get(self.CURRENT_COST_URL)

        accounts_total_cost = []

        list_of_aws_accounts = self.list_accounts(account_type)

        cost_response = response['data']
        # This part is replicated several times starting from here, Should I create a function to handle it?
        # I started something but it's not an easy task (at least at first glance)
        # cost_response = self.__work_on_data(response, 'data', 0)
        for accounts_total in cost_response:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        return cost_by_account

    def get_current_by_services(self, account_type='AWS-Account'):
        response = self.client.get(self.CURRENT_COST_URL)

        services_total_cost = []

        list_of_services = self.list_service(account_type)

        cost_response = response['data']
        for services_total in cost_response[0]:
            services_total_cost.append(services_total[0])

        cost_by_service = dict(zip(list_of_services, services_total_cost))

        return cost_by_service

    def get_cost_by_days(self, report_id, account_type='AWS-Account', account_name=None):
        response = self.client.get(self.DAYS_COST_URL.format(report_id))

        days_total_cost = []

        list_of_days = self.list_days(self.DAYS_COST_URL.format(report_id))

        cost_response = response['data'][0]
        for days_cost in cost_response:
            days_total_cost.append(days_cost[0])

        cost_by_days = dict(zip(list_of_days, days_total_cost))

        return cost_by_days

    def get_cost_for_instances(self):
        response = self.client.get(self.INSTANCE_COST_URL)

        instace_total_cost = []

        list_of_days = self.list_days(self.INSTANCE_COST_URL)

        cost_response = response['data']
        for instance_cost in cost_response:
            instace_total_cost.append(instance_cost[0][0])

        cost_by_day = dict(zip(list_of_days, instace_total_cost))

        return cost_by_day

    def account_history(self, account_type, report_id):
        response = self.client.get(self.ACCOUNTS_HISTORY_COST_URL.format(report_id))

        list_of_months = self.list_months(self.ACCOUNTS_HISTORY_COST_URL.format(report_id), report_id)
        list_of_accounts = self.list_accounts(account_type)

        accounts_history = {}

        cost_response = response['data']
        for month_cost, each_month in zip(cost_response, list_of_months):
            accounts_cost_history_by_month = dict(zip(list_of_accounts, sum(month_cost, [])))
            months_total = {each_month: accounts_cost_history_by_month}
            for key, value in months_total.iteritems():
                accounts_history[key] = value

        return accounts_history

    def service_history(self, account_type, report_id):
        response = self.client.get(self.HISTORY_COST_URL)

        list_of_months = self.list_months(self.HISTORY_COST_URL, report_id)

        service_cost_by_month = {}
        fetch_services = self.list_service()

        cost_response = response['data']
        for month_cost, each_month in zip(cost_response, list_of_months):
            service_cost_history_by_month = dict(zip(fetch_services, sum(month_cost, [])))
            months_total = {each_month: service_cost_history_by_month}
            for key, value in months_total.iteritems():
                service_cost_by_month[key] = value

        return service_cost_by_month

    def get_custom_report(self, report_id):
        response = self.client.get(self.CUSTOM_REPORT_URL.format(report_id))

        groups_cost = []
        groups_names = self.list_groups(report_id)

        cost_response = response['data']
        for group_total in cost_response:
            groups_cost.append(group_total[0])

        cost_by_group = dict(zip(groups_names, groups_cost))

        return cost_by_group