#!/bin/bash
cd `dirname $0`
. ~/virtualenv/bitbankcc/bin/activate
export ENV_ORDERCRYPTO_DATA_DIR=`pwd`/data
python balance.py
deactivate
