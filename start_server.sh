#!/bin/sh
. ~/virtualenv/bitbankcc/bin/activate
cd server
python -m http.server 5555 --cgi
