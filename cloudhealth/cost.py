class CostClient(object):
    CURRENT_COST_URL = 'olap_reports/cost/current?'
    INSTANCE_COST_URL = 'olap_reports/cost/current/instance?'
    HISTORY_COST_URL = 'olap_reports/cost/history?'
    CUSTOM_REPORT_URL = 'olap_reports/custom/{0}?'
    DATE_NAME = 'time'

    def __init__(self, client):
        self.client = client

    def _list_object(self, url, requested_object):
        """List function to support the get functions.

         This function helps build the lists to be used by other functions.
         It should be use internally only.

        """
        response = self.client.get(url)

        list_of_objects = []

        try:
            list_object = response['dimensions'][0][requested_object]
        except KeyError:
            list_object = response['dimensions'][1][requested_object]

        for instance in list_object:
            object = instance['label']
            list_of_objects.append(object)

        return list_of_objects

    def get_current_by_accounts(self,
                                account_type='AWS-Account',
                                account_name=None):
        """Fetch data on current cost from start of month by accounts

        Returns dictionary of account:cost

        """
        response = self.client.get(self.CURRENT_COST_URL)

        accounts_total_cost = []
        list_of_aws_accounts = self._list_object(self.CURRENT_COST_URL,
                                                 account_type)

        cost_response = response['data']
        for accounts_total in cost_response:
            accounts_total_cost.append(accounts_total[0][0])

        cost_by_account = dict(zip(list_of_aws_accounts, accounts_total_cost))

        return cost_by_account

    def get_current_by_services(self, account_type='AWS-Account',
                                service_type='AWS-Service-Category'):
        """Fetch data on current cost from start of month by service type

        Returns dictionary of service:cost

        """
        response = self.client.get(self.CURRENT_COST_URL)

        services_total_cost = []
        list_of_services = self._list_object(self.CURRENT_COST_URL,
                                             service_type)

        cost_response = response['data'][0]
        for services_total in cost_response:
            services_total_cost.append(services_total[0])

        cost_by_service = dict(zip(list_of_services, services_total_cost))

        return cost_by_service

    def get_cost_by_days(self, report_id,
                         account_type='AWS-Account',
                         account_name=None):
        """Fetch data of cost per day for all accounts and services

        Returns dictionary of day_date:cost

        """
        response = self.client.get(self.CUSTOM_REPORT_URL.format(report_id))

        days_total_cost = []
        list_of_days = self._list_object(
                self.CUSTOM_REPORT_URL.format(report_id), self.DATE_NAME)

        cost_response = response['data'][0]
        for days_cost in cost_response:
            days_total_cost.append(days_cost[0])

        cost_by_days = dict(zip(list_of_days, days_total_cost))

        return cost_by_days

    def get_cost_for_instances(self):
        """Fetch data of cost per day for instances on all accounts

        Returns dictionary of day_date:cost_for_instances

        """
        response = self.client.get(self.INSTANCE_COST_URL)

        instace_total_cost = []
        list_of_days = self._list_object(self.INSTANCE_COST_URL,
                                         self.DATE_NAME)

        cost_response = response['data']
        for instance_cost in cost_response:
            instace_total_cost.append(instance_cost[0][0])

        cost_by_day = dict(zip(list_of_days, instace_total_cost))

        return cost_by_day

    def get_account_history(self, account_type, report_id):
        """Fetch the cost history for account

        For best results save a report that uses "Accounts" as Category
         the interval should be by month
        Returns a dictionary of months with a dictionary of accounts:cost

        """
        response = self.client.get(self.CUSTOM_REPORT_URL.format(report_id))

        list_of_months = self._list_object(
                self.CUSTOM_REPORT_URL.format(report_id), self.DATE_NAME)
        list_of_accounts = self._list_object(self.CURRENT_COST_URL,
                                             account_type)

        accounts_history = {}

        cost_response = response['data']
        for month_cost, each_month in zip(cost_response, list_of_months):
            accounts_cost_history_by_month = dict(zip(list_of_accounts,
                                                      sum(month_cost, [])))
            months_total = {each_month: accounts_cost_history_by_month}
            for key, value in months_total.iteritems():
                accounts_history[key] = value

        return accounts_history

    def get_service_history(self, account_type, report_id,
                        service_type='AWS-Service-Category'):
        """Fetch the cost history for service type

        Returns a dictionary of months with a dictionary of service:cost
        Using report_id will limit the results to only desired services
         and history of

        """
        if report_id:
            response = self.client.get(
                    self.CUSTOM_REPORT_URL.format(report_id))
            fetch_services = self._list_object(
                    self.CUSTOM_REPORT_URL.format(report_id), service_type)
        else:
            response = self.client.get(self.HISTORY_COST_URL)
            fetch_services = self._list_object(self.CURRENT_COST_URL,
                                               service_type)

        list_of_months = self._list_object(self.HISTORY_COST_URL,
                                           self.DATE_NAME)

        service_cost_by_month = {}

        cost_response = response['data']
        for month_cost, each_month in zip(cost_response, list_of_months):
            service_cost_history_by_month = dict(zip(fetch_services,
                                                     sum(month_cost,
                                                         [])))
            months_total = {each_month: service_cost_history_by_month}
            for key, value in months_total.iteritems():
                service_cost_by_month[key] = value

        return service_cost_by_month

    def get_custom_report(self, report_id):
        """Fetch data on current cost from start of month by custom grouping

       Returns dictionary of service\account\group:cost
       This will work with 2 dimensions reports only!

       """
        response = self.client.get(self.CUSTOM_REPORT_URL.format(report_id))

        for key in response['dimensions'][0].iterkeys():
            group_name = key

        groups_cost = []
        groups_names = self._list_object(
                self.CUSTOM_REPORT_URL.format(report_id), group_name)

        cost_response = response['data']
        for group_total in cost_response:
            groups_cost.append(group_total[0])

        cost_by_group = dict(zip(groups_names, groups_cost))

        return cost_by_group
