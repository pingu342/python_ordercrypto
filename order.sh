#!/bin/bash
cd `dirname $0`
. ~/virtualenv/bitbankcc/bin/activate
if [ -z "${ENV_ORDERCRYPTO_DATA_DIR}" ]; then
	export ENV_ORDERCRYPTO_DATA_DIR=`pwd`/data
fi
python order.py
deactivate
