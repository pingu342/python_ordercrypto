#!/usr/bin/env python
import os
import sys
import cgi
import pyzipper, secrets, string
from os.path import join, dirname

def make_password(length):
    pass_chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return password

DIR = join(dirname(__file__), '../../')

form = cgi.FieldStorage()

if 'password' in form:
    password = form.getvalue('password')
    print('Content-Type: application/zip')
    print('Content-Disposition: attachment; filename="backup.zip"')
    print()
    sys.stdout.flush()   # required
    with pyzipper.AESZipFile(sys.stdout.buffer, 'w',
            compression=pyzipper.ZIP_LZMA) as zipf:
        zipf.setencryption(pyzipper.WZ_AES, nbits=128)
        zipf.setpassword(password.encode('UTF-8'))
        for filename in ['orders.txt', 'time.txt', '.env', 'config.yaml']:
            with open(DIR + filename, 'rb') as f:
                zipf.writestr(filename, f.read())
else:
    password = make_password(32)
    print('Content-Type: text/html; charset=utf-8')
    print()
    print('Your password is: ', password, '<br/>')
    print('<a href="/cgi-bin/backup.py?password=%s">download</a>' % password)

