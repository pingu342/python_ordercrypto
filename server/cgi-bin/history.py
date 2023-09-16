#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import yaml
import sys
from os.path import join, dirname
from dotenv import load_dotenv

DIR = os.environ.get("ENV_ORDERCRYPTO_DATA_DIR")

with open(join(DIR, 'config.yaml'), 'r') as f:
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

load_dotenv(join(DIR, '.env'))
API_KEY = os.environ.get("ENV_KEY")
API_SECRET = os.environ.get("ENV_SECRET")

print('Content-type: application/json\r\n')

if not API_KEY or not API_SECRET:
    print('APIキーが設定されてません')
    sys.exit()

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

try:
    orders = prv.get_active_orders(PAIR)
except Exception as e:
    print(e)
    sys.exit()

series = []

for order in orders['orders']:
    if matching_order(join(DIR, 'orders.txt'), order['order_id']):
        a = order['start_amount']
        p = order['price']
        t = time.localtime(int(order['ordered_at'])/1000 + 60*60*9)
        t = time.strftime("%Y-%m-%d %H:%M:%S", t)
        d = {
            "order_id" : order['order_id'],
            "status" : '注文中',
            "amount" : a,
            "price" : p,
            "purchase" : int(float(a) * float(p)),
            "date" : t,
        }
        series.append(d)

count = 1000
truncate_trade_id = 0
since_unix_time = None

while True:
    try:
        value = prv.get_trade_history(pair=PAIR, order_count=count, since=since_unix_time, order='asc')
    except Exception as e:
        print(e)
        sys.exit()

    # print(json.dumps(value))
    # {"trade_id": 3969372, "order_id": 324460818, "pair": "btc_jpy", "side": "buy", "type": "limit", "amount": "0.0050", "price": "2000000", "maker_taker": "maker", "fee_amount_base": "0.00000000", "fee_amount_quote": "0.0000", "executed_at": 1513733421000}

    no_value = True
    for trade in value['trades']:
        if trade['trade_id'] > truncate_trade_id:
            no_value = False
            if matching_order(join(DIR, 'orders.txt'), trade['order_id']):
                a = trade['amount']
                p = trade['price']
                t = time.localtime(int(trade['executed_at'])/1000 + 60*60*9)
                t = time.strftime("%Y-%m-%d %H:%M:%S", t)
                d = {
                    "order_id" : trade['order_id'],
                    "status" : '約定',
                    "amount" : a,
                    "price" : p,
                    "purchase" : int(float(a) * float(p)),
                    "date" : t,
                }
                series.append(d)

    if len(value['trades']) < count or no_value:
        break

    truncate_trade_id = value['trades'][-1]['trade_id']
    since_unix_time = value['trades'][-1]['executed_at']

resp = {
    "result" : True,
    "orders" : series
}

print(json.dumps(resp))

