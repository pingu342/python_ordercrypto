import python_bitbankcc
import os, json, time
from os.path import join, dirname
from dotenv import load_dotenv
from util import save_current_time, calculate_time_diff

BUY_YEN = 2000
INTERVAL = 60*60*24/5
PAIR = 'btc_jpy'
DIR = join(dirname(__file__), '')

# $B%U%!%$%k$K(Border_id$B$H0lCW$9$k9T$,$"$l$P$=$N9T$r:o=|$7$F(BTrue$B$r!"L5$1$l$P(BFalse$B$rJV$9(B
def delete_matching_order(file_path, order_id):
    order_found = False

    # $B%U%!%$%k$NA49T$r<hF@(B
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # $B0lCW$7$J$$9T$N$_%U%!%$%k$K=q$-La$9(B
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

    # $BHD$+$iCmJ82A3J$H9XF~NL$r7hDj(B
    price = int(float(value["bids"][0][0])*0.9999)
    amount = BUY_YEN / price

    print('[bids]')
    print('price', price)
    print('amount', amount)

    new_order = re_order = 0
    
    # $BL$LsDj$NCmJ8$O%-%c%s%;%k$7$F:FCmJ8(B
    orders = prv.get_active_orders(PAIR)
    for order in orders['orders']:
        if int(order['price']) < price:
            if delete_matching_order(DIR + 'orders.txt', order['order_id']):
                print('[cancel order]')
                value = prv.cancel_order(PAIR, order['order_id'])
                print(json.dumps(value))

                # $B:FCmJ8$N%+%&%s%H%"%C%W(B
                re_order += 1
    
    # $BA02s$N?75,CmJ8$+$i$N0lDj;~4V$,7P$C$F$$$?$i?75,CmJ8(B
    time_diff = calculate_time_diff(DIR + 'time.txt')
    if time_diff >= INTERVAL:
        new_order = 1
        save_current_time(DIR + 'time.txt')

    # $B?75,(B/$B:FCmJ8$N%+%&%s%H$@$1;XCMCmJ8(B
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

        # order_id$B$rJ]B8(B
        with open(DIR + 'orders.txt', 'a') as file:
            file.write(str(order_result['order_id']) + '\n')

