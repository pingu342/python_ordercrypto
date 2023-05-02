#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import cgi, sys
from os.path import join, dirname
from dotenv import load_dotenv

PAIR = 'btc_jpy'
DIR = join(dirname(__file__), '../../')

print('Content-type: text/html; charset=UTF-8\r\n')

try:
    form = cgi.FieldStorage()
    purchase = float(form['purchase'].value)
except:
    print('input error')
    sys.exit()

load_dotenv(DIR + '.env')
API_KEY = os.environ.get("ENV_KEY")
API_SECRET = os.environ.get("ENV_SECRET")

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

value = pub.get_depth(pair = PAIR)

# 板から注文価格と購入量を決定
price = int(float(value["bids"][0][0])*0.9999)
amount = round(purchase / price, 6)

print('[bids]', '<br/>')
print('purchase :', purchase, '<br/>')
print('price    :', price, '<br/>')
print('amount   :', amount, '<br/>')

if amount <= 0.00001:
    print('amount too little')
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
    print('Private api error. Bad key and secret')
    sys.exit()

print('order_id :', order_result['order_id'], '<br/>')

# order_idを保存（スポット注文は先頭に '+' を付与）
with open(DIR + 'orders.txt', 'a') as file:
    file.write('+' + str(order_result['order_id']) + '\n')

