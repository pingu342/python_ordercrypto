# python_ordercrypto

bitbankccでbtc_jpyペアをドルコスト平均法で定期購入する。

## 環境構築
    $ cd ~
    $ mkdir virtualenv
    $ cd virtualenv
    $ python3 -m venv bitbankcc
    $ cd ~
    $ git pull <this repository>
    $ . ~/virtualenv/bitbankcc/bin/activate
    $ pip install git+https://github.com/bitbankinc/python-bitbankcc@fba9f83\#egg=python-bitbankcc
    $ pip install requests
    $ pip install python-dotenv
    $ cd python_ordercrypto
    $ echo "ENV_KEY=XXX" > .env
    $ echo "ENV_SECRET=XXX" >> .env
    $ deactivate
    
## 定期購入

    $ ./order.sh

order.shを定期的に実行する。

crontabを使う場合

    $ crontab -e
    
    */1 * * * * /path/to/python_ordercrypto/a.out >> /path/to/python_ordercrypto/out  の行を追加
    
    $ sudo /etc/init.d/cron restart

購入の設定はorder.pyの以下の変数で。デフォルトでは、BTCを2000円✕５回／日で購入する。つまり１日で１万円分のBTCを購入する。

    PAIR = 'btc_jpy'
    BUY_YEN = 2000
    INTERVAL = 60*60*24/5

注文では板のbidsを取得してギリギリmakerとして注文できる価格で指値で注文する。

実行時、time.txtが存在しない（初回注文）か、time.txtに書かれた時刻からINTERVALが経過していれば新規注文してtime.txtに時刻を出力し、orders.txtに注文のorder_idを出力する。INTERVALが経過してなければ新規注文しない。

実行時、orders.txtが存在するなら、orders.txtに書かれた過去のorder_idの注文の中で、未約定の注文についてはもっと約定しやすい価格に変更が可能であれば注文しなおしてorders.txtを更新する。


## 購入状況確認

    $ ./balance.sh
    number of trades : 190
    total amount     : 0.0626
    purchase price   : 237919.9
    average price    : 3800637.7
    current price    : 4076978.0
    profit           : 17298.9
    last order       : 2023-04-15 06:45:59

orders.txtを参照してbitbankccに問い合わせして上記を出力する。

購入状況をブラウザで確認したいとき

    $ sudo apt install screen
    $ screen
    $ cd /path/to/python_ordercrypto
    $ ./start_server.sh
    [ctrl] + a
    d

`http://<ip_addr>:5555/cgi-bin/balance.py` にアクセス
