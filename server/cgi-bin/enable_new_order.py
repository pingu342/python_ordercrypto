#!/usr/bin/env python
import sys
import cgi
import yaml
from os.path import join, dirname

DIR = join(dirname(__file__), '../../')

with open(DIR + 'config.yaml', 'r') as f:
    config = yaml.safe_load(f)

new_order = True

form = cgi.FieldStorage()
if 'disable' in form:
    value = form.getvalue('disable')
    if value == '1':
        new_order = False

config['settings']['new_order'] = new_order

with open(DIR + 'config.yaml', 'w') as f:
    yaml.safe_dump(config, f)

print('Content-type: text/html; charset=UTF-8\r\n')

print('ok')

