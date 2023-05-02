#!/usr/bin/env python
import sys
import yaml
from os.path import join, dirname

DIR = join(dirname(__file__), '../../')

with open(DIR + 'config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print(config)

config['settings']['new_order'] = True

with open(DIR + 'config.yaml', 'w') as f:
    yaml.safe_dump(config, f)

print('Content-type: text/html; charset=UTF-8\r\n')
print()

print('ok')

