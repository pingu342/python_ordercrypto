#!/usr/bin/env python
import os
import cgi
import zipfile
from os.path import join, dirname

DIR = join(dirname(__file__), '../../')

print('Content-type: text/html; charset=UTF-8\r\n')

result = 'error'

form = cgi.FieldStorage()

if 'zipfile' in form:
    uploaded_zip = form['zipfile']
    with zipfile.ZipFile(uploaded_zip.file) as zipf:
        for fileinfo in zipf.infolist():
            filename = fileinfo.filename
            with open(DIR + filename, 'wb') as f:
                f.write(zipf.read(fileinfo))
        result = 'ok'

print(result)
