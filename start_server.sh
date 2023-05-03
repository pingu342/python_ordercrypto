#!/bin/sh
cd `dirname $0`
. ~/virtualenv/bitbankcc/bin/activate
export ENV_ORDERCRYPTO_DATA_DIR=`pwd`/data
cd server
python -m http.server 5555 --cgi
