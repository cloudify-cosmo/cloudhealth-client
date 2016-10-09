import re

from cloudhealth import exceptions


class ReportsClient(object):
    BASE_REPORT_URL = '/olap_reports/custom/?'

    def __init__(self, client):
        self.client = client

    def list(self, topic=None):
        reports = []
        reports_name = []
        links_list = []

        uri = self.BASE_REPORT_URL
        if topic:
            uri = uri + '/{0}'.format(topic)
        response = self.client.get(uri)
        report_links = response['links']
        for _, link_item in report_links.items():
            reports_name.append(_.encode('ascii'))
            reports.append(link_item['href'])

        for i in reports:
            links_list.append(re.findall(
                    'report_id=(.*?)$', i.encode('ascii'), re.DOTALL))
        links_list = sum(links_list, [])
        reports_and_ids = dict(zip(links_list, reports_name))

        return reports_and_ids

    def list_groups(self, uri):
        response = self.client.get(uri)

        list_of_groups = []
        for group_name in response['dimensions'][0]:
            pass
        group_list = response['dimensions'][0][group_name]

        for service in group_list:
            label = service['label']
            list_of_groups.append(label.encode('ascii'))

        return list_of_groups

    def topics(self):
        topics = []

        reports = self.list()
        for report in reports:
            topic = report.split('/')[-1]
            topics.append(topic)

        return topics

    def get(self, id=None, topic=None, report_name=None):
        if id:
            uri = '/olap_reports/custom/{0}?'.format(id)
        elif topic and report_name:
            uri = '/olap_reports/{0}/{1}?'.format(topic, report_name)
        else:
            raise exceptions.CloudHealthError(
                'Must either provide a report id or a topic and report-name')

        report = self.client.get(uri)

        groups_cost = []
        groups_names = self.list_groups(uri)

        cost_response = report['data']
        for group_total in cost_response:
            groups_cost.append(group_total[0])

        cost_by_group = dict(zip(groups_names, groups_cost))

        return cost_by_group
