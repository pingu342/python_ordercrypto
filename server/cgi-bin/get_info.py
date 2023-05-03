#!/usr/bin/env python
import os
import sys
import yaml
import datetime
from os.path import join, dirname
sys.path.append('../')  # TODO: want to fix
from util import save_current_time, calculate_time_diff

DIR = join(dirname(__file__), '../../')

hostname = os.environ.get("APP_HIDDEN_SERVICE")
if hostname == None:
    hostname = ''

with open(DIR + 'config.yaml', 'r') as f:
    data = yaml.safe_load(f)

new_order = data['settings']['new_order']
interval = data['settings']['interval']

print('Content-type: application/json\r\n')

if new_order:
    remain = int(interval - calculate_time_diff(DIR + 'time.txt'))
    td = datetime.timedelta(seconds=remain)
    print('{"new_order": true, "remain": "%s", "hostname": "%s"}\n' % (td, hostname))
else:
    print('{"new_order": false, "remain": -1, "hostname": "%s"}\n' % hostname)

