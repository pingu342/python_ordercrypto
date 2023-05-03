#!/usr/bin/env python
import os
import cgi
import pyzipper
from os.path import join, dirname

DIR = os.environ.get("ENV_ORDERCRYPTO_DATA_DIR")

print('Content-type: text/html; charset=UTF-8\r\n')

result = 'error'

form = cgi.FieldStorage()

if 'zipfile' in form:
    uploaded_zip = form['zipfile']
    with pyzipper.AESZipFile(uploaded_zip.file) as zipf:
        zipf.setpassword(form.getvalue('password').encode('UTF-8'))
        for fileinfo in zipf.infolist():
            filename = fileinfo.filename
            with open(join(DIR, filename), 'wb') as f:
                f.write(zipf.read(fileinfo))
        result = 'ok'

print(result)
