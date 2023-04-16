import python_bitbankcc
import os, json, time
from os.path import join, dirname
from dotenv import load_dotenv

PAIR = 'btc_jpy'
DIR = join(dirname(__file__), '')

def matching_order(file_path, order_id):
    order_found = False

    # ファイルの全行を取得
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

if __name__ == '__main__':

    load_dotenv(DIR + '.env')
    API_KEY = os.environ.get("ENV_KEY")
    API_SECRET = os.environ.get("ENV_SECRET")

    pub = python_bitbankcc.public()
    prv = python_bitbankcc.private(API_KEY, API_SECRET)

    value = prv.get_trade_history(PAIR, 1000)

    # print(json.dumps(value))
    # {"trade_id": 3969372, "order_id": 324460818, "pair": "btc_jpy", "side": "buy", "type": "limit", "amount": "0.0050", "price": "2000000", "maker_taker": "maker", "fee_amount_base": "0.00000000", "fee_amount_quote": "0.0000", "executed_at": 1513733421000}

    trade_num = 0
    total_amount = 0.0
    total_price = 0.0

    for trade in value['trades']:
        if matching_order(DIR + 'orders.txt', trade['order_id']):
            amount = float(trade['amount'])
            price = float(trade['price'])
            total_amount += amount
            total_price += (price * amount)
            trade_num += 1
    
    print('number of trades :', trade_num)
    print('total amount     :', round(total_amount, 6))
    print('purchase price   :', round(total_price, 1))
    print('average price    :', round(total_price/total_amount, 1))

    value = pub.get_depth(pair = PAIR)
    current_price = float(value["bids"][0][0])
    print('current price    :', current_price)

    profit = current_price * total_amount - total_price;

    print('profit           :', round(profit, 1), '(' + str(round(profit / total_price * 100, 1)) + '%)')

    active_order = 0
    orders = prv.get_active_orders(PAIR)
    for order in orders['orders']:
        if matching_order(DIR + 'orders.txt', order['order_id']):
            active_order += 1

    print('active order     :', active_order)

    time_str = 'n/a'
    with open(DIR + 'time.txt', 'r') as file:
        time_str = file.read().strip()

    print('last order       :', time_str)
