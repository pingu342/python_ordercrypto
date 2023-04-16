#!/bin/bash
cd `dirname $0`
. ~/virtualenv/bitbankcc/bin/activate
python balance.py
deactivate
