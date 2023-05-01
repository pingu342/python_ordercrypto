#!/usr/bin/env python
import os
import cgi, sys
from os.path import join, dirname

DIR = join(dirname(__file__), '../../')

print('Content-type: text/html; charset=UTF-8\r\n')

try:
    form = cgi.FieldStorage()
    key = form['key'].value
    secret = form['secret'].value
except:
    print('input error')
    sys.exit()

try:
    with open(DIR + '.env', 'w') as file:
        file.write('ENV_KEY=' + key + '\n')
        file.write('ENV_SECRET=' + secret + '\n')
except:
    print('write error')
    sys.exit()

print('ok')
