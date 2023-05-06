#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import cgi, sys, yaml
from os.path import join, dirname
from dotenv import load_dotenv

DIR = os.environ.get("ENV_ORDERCRYPTO_DATA_DIR")

with open(join(DIR, 'config.yaml'), 'r') as f:
    data = yaml.safe_load(f)

PAIR = data['settings']['pair']

print('Content-type: application/json\r\n')

try:
    form = cgi.FieldStorage()
    purchase = float(form['purchase'].value)
except:
    print('{')
    print('"result" : false,')
    print('"error" : "Inpur parameter error."')
    print('}')
    sys.exit()

load_dotenv(join(DIR, '.env'))
API_KEY = os.environ.get("ENV_KEY")
API_SECRET = os.environ.get("ENV_SECRET")

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

value = pub.get_depth(pair = PAIR)

# 板から注文価格と購入量を決定
price = int(float(value["bids"][0][0])*0.9999)
amount = round(purchase / price, 6)

if amount <= 0.0001:
    print('{')
    print('"result" : false,')
    print('"error" : "Inpur parameter error."')
    print('}')
    sys.exit()

try:
    order_result = prv.order( 
            pair = PAIR,
            price = str(price),
            amount = str(amount),
            side = 'buy',
            order_type = 'limit'
            )
except TypeError:
    print('{')
    print('"result" : false,')
    print('"error" : "Bad API key."')
    print('}')
    sys.exit()

print('{')
print('"result" : true,')
print('"purchase" :', purchase, ',')
print('"price" :', price, ',')
print('"amount" :', amount, ',')
print('"order_id" :', order_result['order_id'])
print('}')

# order_idを保存（スポット注文は先頭に '+' を付与）
with open(join(DIR, 'orders.txt'), 'a') as file:
    file.write('+' + str(order_result['order_id']) + '\n')

