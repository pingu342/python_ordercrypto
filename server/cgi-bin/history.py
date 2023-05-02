#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import yaml
import sys
from os.path import join, dirname
from dotenv import load_dotenv

DIR = join(dirname(__file__), '../../')
with open(DIR + 'config.yaml', 'r') as f:
    data = yaml.safe_load(f)

PAIR = data['settings']['pair']

def matching_order(file_path, order_id):
    order_found = False

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return False

    for line in lines:
        if line.strip() == str(order_id):
            order_found = True

        # スポット注文
        spot_order_id = '+' + str(order_id)
        if line.strip() == spot_order_id:
            order_found = True

    return order_found

load_dotenv(DIR + '.env')
API_KEY = os.environ.get("ENV_KEY")
API_SECRET = os.environ.get("ENV_SECRET")

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

print('Content-type: text/html; charset=UTF-8\r\n')

try:
    orders = prv.get_active_orders(PAIR)
except TypeError:
    print('Private api error. Bad key and secret')
    sys.exit()

print('active order', '<br/>')
for order in orders['orders']:
    if matching_order(DIR + 'orders.txt', order['order_id']):
        a = order['start_amount']
        p = order['price']
        r = int(float(a) * float(p))
        t = time.localtime(int(order['ordered_at'])/1000 + 60*60*9)
        print(order['order_id'], ',',
                time.strftime("%Y-%m-%d %H:%M:%S", t), ',',
                a, ',', p, ',', r, '<br/>')

try:
    value = prv.get_trade_history(PAIR, 1000)
except TypeError:
    print('Private api error. Bad key and secret')
    sys.exit()

# print(json.dumps(value))
# {"trade_id": 3969372, "order_id": 324460818, "pair": "btc_jpy", "side": "buy", "type": "limit", "amount": "0.0050", "price": "2000000", "maker_taker": "maker", "fee_amount_base": "0.00000000", "fee_amount_quote": "0.0000", "executed_at": 1513733421000}

print('history', '<br/>')
for trade in value['trades']:
    if matching_order(DIR + 'orders.txt', trade['order_id']):
        a = trade['amount']
        p = trade['price']
        r = int(float(a) * float(p))
        t = time.localtime(int(trade['executed_at'])/1000 + 60*60*9)
        print(trade['order_id'], ',',
                time.strftime("%Y-%m-%d %H:%M:%S", t), ',',
                a, ',', p, ',', r, '<br/>')

