import json

import config
import utils.log as log
from utils.test_desc import AddTestInfo


class APICrushRuleSet(object):
    def __init__(self, **api_details):
        self.fsid = api_details['fsid']
        self.base_api = 'cluster/'
        self.api = None

    def construct_api(self):
        self.api = self.base_api + self.fsid + '/' + 'crush_rule_set'
        log.debug(self.api)
        return self.api


class APICrushRuleSetOps(APICrushRuleSet):

    def __init__(self, **kwargs):
        self.auth = kwargs['auth']
        super(APICrushRuleSetOps, self).__init__(**kwargs)
        self.json_config = None

    def get_crush_ruleset(self):

        api = self.construct_api()
        response = self.auth.request('GET', api, verify=False)
        response.raise_for_status()
        log.info('\n%s' %response.json())

        pretty_response = json.dumps(response.json(),indent=2)
        log.debug('pretty json response from api %s\n' % pretty_response)


    def put(self):
        pass

    def post(self):
        pass


def exec_test(config_data):

    add_test_info = AddTestInfo(4, 'get crush rule set')
    add_test_info.started_info()

    try:

        api_curshruleset_ops = APICrushRuleSetOps(**config_data)
        api_curshruleset_ops.get_crush_ruleset()
        add_test_info.status('ok')

    except Exception, e:

        log.error('test case error')
        log.info(e)
        add_test_info.status('error')

    add_test_info.completed_info()


if __name__ == '__main__':
    config_data = config.get_config()

    if not config_data['auth']:
        log.error('auth failed')

    else:
        exec_test(config_data)
