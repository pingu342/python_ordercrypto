# python_ordercrypto

bitbankccでbtc_jpyペアをドルコスト平均法で定期購入する。

- Dockerコンテナで実行
- Dockeを使わずに実行

## Dockerコンテナで実行

クローン

    $ git clone https://github.com/pingu342/python_ordercrypto.git
    $ cd python_ordercrypto

Dokerイメージを作成

    $ docker build --tag python_ordercrypto .

コンテナを作成して実行（5555番ポートを開放）

    $ docker run --name my_container -p 5555:5555 -d python_ordercrypto

ブラウザで`http://localhost:5555`にアクセス

初めて使う場合、「APIキー設定」と「定期購入を開始」を行う。

初めてではない場合（実行環境を引っ越しするなど）、以前の環境で「バックアップ」を行い、パスワードと`backup.zip`を保存しておき、新しい環境で「復元」を行うことで、APIキーや取引履歴が復元する。

## Dockerを使わずに実行

raspi4で動作確認

### インストール

    $ cd ~
    $ mkdir virtualenv
    $ cd virtualenv
    $ python3 -m venv bitbankcc
    $ cd ~
    $ git clone https://github.com/pingu342/python_ordercrypto.git
    $ cd python_ordercrypto
    $ . ~/virtualenv/bitbankcc/bin/activate
    $ pip install git+https://github.com/bitbankinc/python-bitbankcc@fba9f83\#egg=python-bitbankcc
    $ pip install requests
    $ pip install python-dotenv
    $ pip install pyyaml
    $ pip install pyzipper
    $ echo "ENV_KEY=XXX" > .env
    $ echo "ENV_SECRET=XXX" >> .env
    $ deactivate
    

### 実行

`order.sh`を定期的に実行する。

crontabを使う場合：

    $ crontab -e
    
    */1 * * * * /path/to/python_ordercrypto/order.sh >> /path/to/python_ordercrypto/out 2>&1  の行を追加
    
    $ sudo /etc/init.d/cron restart

購入の設定は`config.yaml`の以下の変数で。デフォルトでは、BTCを2000円✕５回／日で購入する。つまり１日で１万円分のBTCを購入する。

    settings:
        new_order: false # falseの場合、order.shは新規注文しない
        pair: btc_jpy   # ペア
        buy_yen: 2000   # 金額 (円)
        interval: 17280 # 間隔 60*60*24/5 (秒)

注文では板のbidsを取得してギリギリmakerとして注文できる価格で指値で注文する。

実行時、time.txtが存在しない（初回注文）か、time.txtに書かれた時刻からINTERVALが経過していれば新規注文してtime.txtに時刻を出力し、orders.txtに注文のorder_idを出力する。INTERVALが経過してなければ新規注文しない。

実行時、orders.txtが存在するなら、orders.txtに書かれた過去のorder_idの注文の中で、未約定の注文についてはもっと約定しやすい価格に変更が可能であれば注文しなおしてorders.txtを更新する。


### 購入状況確認

    $ ./balance.sh
    number of trades : 200
    total amount     : 0.0654
    purchase price   : 249321.3
    average price    : 3812251.5
    current price    : 4059000.0
    profit           : 16137.3 (6.5%)
    active order     : 0
    last order       : 2023-04-16 11:43:27

orders.txtを参照してbitbankccに問い合わせして上記を出力する。

購入状況をブラウザで確認したいとき

    $ ./start_server.sh
    
`http://<ip_addr>:5555` にアクセス

シェルからexitしてもサーバを永続実行させるためscreenを使う場合

    $ sudo apt install screen
    $ screen
    $ cd /path/to/python_ordercrypto
    $ ./start_server.sh
    [ctrl] + a
    d
    $ exit
    
