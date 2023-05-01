import python_bitbankcc
import os, json, time
import yaml
from os.path import join, dirname
from dotenv import load_dotenv
from util import save_current_time, calculate_time_diff

with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)

BUY_YEN = data['settings']['buy_yen']
INTERVAL = data['settings']['interval']
PAIR = data['settings']['pair']
NEW_ORDER = data['settings']['new_order']
#print('BUY_YEN   :', BUY_YEN)
#print('INTERVAL  :', INTERVAL)
#print('PAIR      :', PAIR)
#print('NEW_ORDER :', NEW_ORDER)

DIR = join(dirname(__file__), '')

# ファイルにorder_idと一致する行があればその行を削除してTrueを、無ければFalseを返す
def delete_matching_order(file_path, order_id):
    order_found = False

    # ファイルの全行を取得
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return False

    # 一致しない行のみファイルに書き戻す (スポット注文は一致せずに書き戻す)
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() == str(order_id):
                order_found = True
            else:
                file.write(line)

    return order_found

if __name__ == '__main__':

    load_dotenv(DIR + '.env')
    API_KEY = os.environ.get("ENV_KEY")
    API_SECRET = os.environ.get("ENV_SECRET")

    pub = python_bitbankcc.public()
    prv = python_bitbankcc.private(API_KEY, API_SECRET)

    value = pub.get_depth(pair = PAIR)

    # 板から注文価格と購入量を決定
    price = int(float(value["bids"][0][0])*0.9999)
    amount = BUY_YEN / price

    print('[bids]')
    print('price', price)
    print('amount', amount)

    new_order = re_order = 0
    
    # 未約定の定期購入の注文はキャンセルして再注文
    orders = prv.get_active_orders(PAIR)
    for order in orders['orders']:
        if int(order['price']) < price:
            if delete_matching_order(DIR + 'orders.txt', order['order_id']):
                print('[cancel order]')
                value = prv.cancel_order(PAIR, order['order_id'])
                print(json.dumps(value))

                # 再注文のカウントアップ
                re_order += 1
    
    # 前回の定期購入の新規注文からの一定時間が経っていたら新規注文
    time_diff = calculate_time_diff(DIR + 'time.txt')
    #print('time_diff', time_diff)
    if time_diff >= INTERVAL and NEW_ORDER:
        new_order = 1
        save_current_time(DIR + 'time.txt')

    # 定期購入の新規/再注文のカウントだけ指値注文
    for i in range(new_order + re_order):
        print('[new order]')
        order_result = prv.order( 
                                 pair = PAIR,
                                 price = str(price),
                                 amount = str(amount),
                                 side = 'buy',
                                 order_type = 'limit'
                                 )

        print(json.dumps(order_result))

        # order_idを保存
        with open(DIR + 'orders.txt', 'a') as file:
            file.write(str(order_result['order_id']) + '\n')

