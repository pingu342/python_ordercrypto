#!/usr/bin/env python
import python_bitbankcc
import os, json, time
import yaml
import sys
import json
import math
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
        date = time.strftime("%Y-%m-%d %H:%M", t)
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

# 配列の要素を100個に間引く
# 配列の最初と最後は間引かずに必ず残す
series_max = 100
d = 1
if trade_num > series_max:
    d = series_max / trade_num
_amount_series = []
_purchase_series = []
_price_series = []
_unit_price_series = []
_date_series = []
_profit_series = []
n = -1
for i in range(trade_num):
    m = -2
    if (series_max - 1) == (n + 1):
        if (trade_num - 1) == i:
            m = -1
    else:
        if (i * d - n) >= 1:
            m = i
    if m > -2:
        _amount_series.append(amount_series[m])
        _purchase_series.append(purchase_series[m])
        _price_series.append(price_series[m])
        _unit_price_series.append(unit_price_series[m])
        _date_series.append(date_series[m])
        _profit_series.append(profit_series[m])
        n += 1

resp = {
    "result" : True,
    "date" : _date_series,
    "price" : _price_series,
    "unit_price" : _unit_price_series,
    "amount" : _amount_series,
    "purchase" : _purchase_series,
    "profit" : _profit_series
}

print(json.dumps(resp))

