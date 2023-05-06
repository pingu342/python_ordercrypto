#!/bin/sh
cd `dirname $0`
. ~/virtualenv/bitbankcc/bin/activate
if [ -z "${ENV_ORDERCRYPTO_DATA_DIR}" ]; then
	export ENV_ORDERCRYPTO_DATA_DIR=`pwd`/data
fi
cd server
python -m http.server 7777 --cgi
