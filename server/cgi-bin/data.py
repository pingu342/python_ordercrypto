#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import yaml
import sys
import json
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

trade_num = 0
total_amount = 0
total_purchase = 0
amount_series = []
purchase_series = []
price_series = []
unit_price_series = []
date_series = []
profit_series = []

trades = value['trades']
trades.reverse()
for trade in trades:
    if matching_order(join(DIR, 'orders.txt'), trade['order_id']):
        amount = float(trade['amount'])
        price = float(trade['price'])
        t = time.localtime(int(trade['executed_at'])/1000 + 60*60*9)
        date = time.strftime("%Y-%m-%d %H:%M:%S", t)
        total_amount += amount
        total_purchase += (price * amount)
        profit = price * total_amount - total_purchase
        trade_num += 1
        amount_series.append(total_amount)
        purchase_series.append(total_purchase)
        price_series.append(price)
        unit_price_series.append(total_purchase/total_amount)
        date_series.append(date)
        profit_series.append(profit)

resp = {
    "result" : True,
    "trade" : trade_num,
    "date" : date_series,
    "price" : price_series,
    "unit_price" : unit_price_series,
    "amount" : amount_series,
    "purchase" : purchase_series,
    "profit" : profit_series
}

print(json.dumps(resp))

