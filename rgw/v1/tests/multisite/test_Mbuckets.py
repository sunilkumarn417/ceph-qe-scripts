import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../../../..")))
import v1.lib.s3.rgw as rgw_lib
from v1.lib.s3.rgw import Config
import v1.utils.log as log
from v1.lib.s3.rgw import ObjectOps
from v1.utils.test_desc import AddTestInfo
import argparse
import yaml
import simplejson
from v1.lib.io_info import AddIOInfo
from v1.lib.read_io_info import ReadIOInfo


def test_exec(config):

    add_io_info = AddIOInfo()
    add_io_info.initialize()

    read_io_info = ReadIOInfo()

    test_info = AddTestInfo('create m buckets')

    try:

        # test case starts

        test_info.started_info()

        with open('user_details') as fout:
            all_user_details = simplejson.load(fout)

        # write all users details to yaml file.

        for each_user in all_user_details:
            add_io_info.add_user_info(**{'user_id': each_user['user_id'],
                                         'access_key': each_user['access_key'],
                                         'secret_key': each_user['secret_key']})


        for each_user in all_user_details:
            log.info('User credentials: %s' % each_user)
            rgw = ObjectOps(config, each_user)

            assert rgw.create_bucket()

        #read_io_info.verify_io()

        test_info.success_status('test completed')

        sys.exit(0)

    except AssertionError as e:
        log.error(e)
        test_info.failed_status('test failed: %s' % e)
        sys.exit(1)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='RGW Automation')

    parser.add_argument('-c', dest="config",
                        help='RGW Test yaml configuration')

    parser.add_argument('-p', dest="port", default='8080',
                        help='port number where RGW is running')

    args = parser.parse_args()

    yaml_file = args.config
    config = Config()
    config.port = args.port
    if yaml_file is None:
        config.bucket_count = 10
        config.objects_count = 0
        config.objects_size_range = 0
    else:
        with open(yaml_file, 'r') as f:
            doc = yaml.load(f)
        config.bucket_count = doc['config']['bucket_count']
        config.objects_size_range = 0
        config.objects_count = 0

    log.info('bucket_count: %s\n'
             'port: %s\n' % (
                 config.bucket_count, config.port))

    test_exec(config)
