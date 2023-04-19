#!/usr/bin/env python
import python_bitbankcc
import os, json, time
from os.path import join, dirname
from dotenv import load_dotenv

PAIR = 'btc_jpy'
DIR = join(dirname(__file__), '../../')

def matching_order(file_path, order_id):
    order_found = False

    with open(file_path, 'r') as file:
        lines = file.readlines()

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

#orders = prv.get_active_orders(PAIR)
#for order in orders['orders']:
#    if matching_order(DIR + 'orders.txt', order['order_id']):

value = prv.get_trade_history(PAIR, 1000)

# print(json.dumps(value))
# {"trade_id": 3969372, "order_id": 324460818, "pair": "btc_jpy", "side": "buy", "type": "limit", "amount": "0.0050", "price": "2000000", "maker_taker": "maker", "fee_amount_base": "0.00000000", "fee_amount_quote": "0.0000", "executed_at": 1513733421000}

for trade in value['trades']:
    if matching_order(DIR + 'orders.txt', trade['order_id']):
        a = trade['amount']
        p = trade['price']
        r = int(float(a) * float(p))
        t = time.localtime(int(trade['executed_at'])/1000)
        print(trade['order_id'], ',',
                time.strftime("%Y/%m/%d %H:%M:%S", t), ',',
                a, ',', p, ',', r, '<br/>')

