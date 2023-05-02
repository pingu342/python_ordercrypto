#!/usr/bin/env python
import os
import sys
import cgi
import zipfile
from os.path import join, dirname

DIR = join(dirname(__file__), '../../')

print('Content-Type: application/zip')
print('Content-Disposition: attachment; filename="backup.zip"')
print()

sys.stdout.flush()   # required

with zipfile.ZipFile(sys.stdout.buffer, 'w',
        compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for filename in ['orders.txt', 'time.txt']:
        with open(DIR + filename, 'rb') as f:
            zipf.writestr(filename, f.read())

