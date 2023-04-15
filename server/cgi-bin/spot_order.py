#!/usr/bin/env python
import python_bitbankcc
import os, json, time
from os.path import join, dirname
from dotenv import load_dotenv

PAIR = 'btc_jpy'
DIR = join(dirname(__file__), '../../')

load_dotenv(DIR + '.env')
API_KEY = os.environ.get("ENV_KEY")
API_SECRET = os.environ.get("ENV_SECRET")

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

value = pub.get_depth(pair = PAIR)

# 板から注文価格と購入量を決定
price = int(float(value["bids"][0][0])*0.9999)
amount = round(1000.0 / price, 6)

print('Content-type: text/html; charset=UTF-8\r\n')
print('[bids]', '<br/>')
print('price :', price, '<br/>')
print('amount :', amount, '<br/>')

order_result = prv.order( 
        pair = PAIR,
        price = str(price),
        amount = str(amount),
        side = 'buy',
        order_type = 'limit'
        )

print('order_id :', order_result['order_id'], '<br/>')

# order_idを保存（スポット注文は先頭に '+' を付与）
with open(DIR + 'orders.txt', 'a') as file:
    file.write('+' + str(order_result['order_id']) + '\n')

