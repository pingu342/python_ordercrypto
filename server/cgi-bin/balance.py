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

if len(API_KEY) == 0 or len(API_SECRET) == 0:
    print('{')
    print('"result" : false,')
    print('"error" : "APIキーが設定されてません"')
    print('}')
    sys.exit()

pub = python_bitbankcc.public()
prv = python_bitbankcc.private(API_KEY, API_SECRET)

try:
    value = prv.get_trade_history(PAIR, 1000)
except Exception as e:
    print('{')
    print('"result" : false,')
    print('"error" : "', e, '"')
    print('}')
    sys.exit()

# print(json.dumps(value))
# {"trade_id": 3969372, "order_id": 324460818, "pair": "btc_jpy", "side": "buy", "type": "limit", "amount": "0.0050", "price": "2000000", "maker_taker": "maker", "fee_amount_base": "0.00000000", "fee_amount_quote": "0.0000", "executed_at": 1513733421000}

trade_num = 0
total_amount = 0.0
total_price = 0.0

for trade in value['trades']:
    if matching_order(join(DIR, 'orders.txt'), trade['order_id']):
        amount = float(trade['amount'])
        price = float(trade['price'])
        total_amount += amount
        total_price += (price * amount)
        trade_num += 1

print('{')
print('"result" : true', ',')
print('"number_of_trades" :', trade_num, ',')
print('"total_amount" :', round(total_amount, 6), ',')
print('"total_payment" :', round(total_price, 1), ',')
if total_amount > 0:
    print('"unit_price" :', round(total_price/total_amount, 1), ',')

value = pub.get_depth(pair = PAIR)
current_price = float(value["bids"][0][0])
print('"current_price" :', current_price, ',')
print('"market_value" :', round(current_price * total_amount, 1), ',')

profit = current_price * total_amount - total_price;

if total_price > 0:
    print('"profit" :', round(profit, 1), ',')
    print('"profit_rate" :', round(profit / total_price * 100, 1), ',')

active_order = 0
orders = prv.get_active_orders(PAIR)
for order in orders['orders']:
    if matching_order(join(DIR, 'orders.txt'), order['order_id']):
        active_order += 1

print('"active order" :', active_order, ',')

try:
    with open(join(DIR, 'time.txt'), 'r') as file:
        time_str = file.read().strip()
except FileNotFoundError:
    time_str = '-'

print('"last order" :', '"' + time_str + '"')
print('}')
