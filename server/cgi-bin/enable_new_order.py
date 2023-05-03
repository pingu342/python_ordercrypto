#!/usr/bin/env python
import os
import sys
import cgi
import yaml
from os.path import join, dirname

DIR = os.environ.get("ENV_ORDERCRYPTO_DATA_DIR")

with open(join(DIR, 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)

new_order = True

form = cgi.FieldStorage()
if 'disable' in form:
    value = form.getvalue('disable')
    if value == '1':
        new_order = False

config['settings']['new_order'] = new_order

with open(join(DIR, 'config.yaml'), 'w') as f:
    yaml.safe_dump(config, f)

print('Content-type: text/html; charset=UTF-8\r\n')

print('ok')

