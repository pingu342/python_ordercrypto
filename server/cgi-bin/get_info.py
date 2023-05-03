#!/usr/bin/env python
import os
import sys
import yaml
import datetime
from os.path import join, dirname
sys.path.append('../')  # TODO: want to fix
from util import save_current_time, calculate_time_diff

DIR = os.environ.get("ENV_ORDERCRYPTO_DATA_DIR")

tor_name = os.environ.get("APP_HIDDEN_SERVICE")
if tor_name == None:
    tor_name = 'not available'

with open(join(DIR, 'config.yaml'), 'r') as f:
    data = yaml.safe_load(f)

new_order = data['settings']['new_order']
interval = data['settings']['interval']

print('Content-type: application/json\r\n')

if new_order:
    remain = int(interval - calculate_time_diff(join(DIR, 'time.txt')))
    td = datetime.timedelta(seconds=remain)
    print('{"new_order": true, "remain": "%s", "tor_name": "%s"}\n' % (td, tor_name))
else:
    print('{"new_order": false, "remain": -1, "tor_name": "%s"}\n' % tor_name)

