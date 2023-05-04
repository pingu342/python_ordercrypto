# python_ordercrypto

bitbankccの取引所でBitcoinをドルコスト平均法で定期購入する。
　
　
## 1.実行手順

Dockerをインストール。参考：[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

定期購入プログラムが入ったDockerイメージを実行。イメージ：[ghcr.io/pingu342/python_ordercrypto](https://github.com/pingu342/python_ordercrypto/pkgs/container/python_ordercrypto)

    $ docker volume create my_volume
    $ docker run -v my_volume:/home/hoge/data --name test -p 5555:5555 -d ghcr.io/pingu342/python_ordercrypto

`http://<ip_addr>:5555` にアクセス。

初めて使う場合、「APIキー設定」と「定期購入を開始」を行う。

初めてではない場合（実行環境を引っ越しするなど）、以前の環境で「バックアップ」を行い、パスワードと`backup.zip`を保存しておき、新しい環境で「復元」を行うことで、APIキーや購入履歴が復元する。

## 2.その他の実行手順

### 2-1.Dockerイメージを自分でビルド

リポジトリをクローン。

    $ git clone https://github.com/pingu342/python_ordercrypto.git
    $ cd python_ordercrypto

Dokerイメージをビルド。

    $ docker build --tag python_ordercrypto .

Volumeを作成。

    $ docker volume create my_volume

コンテナを作成して実行。（Volumeを/home/hoge/dataにマウント。5555番ポートを開放）

    $ docker run -v my_volume:/home/hoge/data --name my_container -p 5555:5555 -d python_ordercrypto

ブラウザで`http://localhost:5555`にアクセス

### 2-2.Dockerを使わずに実行

#### 2-2-1.インストール

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
    $ deactivate
    
#### 2-2-2.実行

##### 2-2-2-1. order.shを定期的に実行

- Linux : cronを使う

        $ crontab -l | { cat; echo "*/1 * * * * /path/to/python_ordercrypto/order.sh >> /path/to/python_ordercrypto/out 2>&1"; } | crontab -
        $ sudo /etc/init.d/cron restart

    - /path/toは環境に合わせて書き換えること

- macOS : LaunchAgentsを使う

    - [order.c](https://github.com/pingu342/python_ordercrypto/blob/master/order.c)を`gcc order.c`でコンパイルしてa.outを作成
    - a.outをorder.shと同じフォルダに配置
    - a.outを試しに実行してoreder.shが実行されることを確認（プライバシー設定でa.outによるファイルアクセスを許可が必要）
    - a.outをLaunchAgentsで定期実行させるための設定ファイル[order_btc.plist](https://github.com/pingu342/python_ordercrypto/blob/master/macos/order_btc.plist)をダウンロード
    - order_btc.plist内の/path/toを環境に合わせて書き換える
    - order_btc.plistをユーザーの~/Library/LaunchAgentsフォルダに配置
    - order_btc.plistは（macOSの起動時ではなく）ユーザーのログイン時に自動起動
    - 手動で定期実行を開始するとき
    
            $ launchctl load ~/Library/LaunchAgents/order_btc.plist 

    - 手動で定期実行を停止するとき
    
            $ launchctl unload ~/Library/LaunchAgents/order_btc.plist 

##### 2-2-2-2. シェルで購入状況を確認

    $ ./balance.sh
    number of trades : 200
    total amount     : 0.0654
    purchase price   : 249321.3
    average price    : 3812251.5
    current price    : 4059000.0
    profit           : 16137.3 (6.5%)
    active order     : 0
    last order       : 2023-04-16 11:43:27

##### 2-2-2-3. ブラウザで確認

    $ ./start_server.sh
    
`http://<ip_addr>:5555` にアクセス。

シェルからexitしてもサーバを永続実行させるためscreenを使う場合。

    $ sudo apt install screen
    $ screen
    $ cd /path/to/python_ordercrypto
    $ ./start_server.sh
    [ctrl] + a
    d
    $ exit

## 3.その他

### 購入設定

`config.yaml`の以下の変数で設定。デフォルトでは、BTCを2000円✕５回／日で購入する。つまり１日で１万円分のBTCを購入する。

    settings:
        new_order: false # falseの場合、order.shは新規注文しない
        pair: btc_jpy   # ペア
        buy_yen: 2000   # 金額 (円)
        interval: 17280 # 間隔 60*60*24/5 (秒)

### 購入アルゴリズム

- 指値注文
    - `order.sh`は、bitbankccの取引所に「指値」で買い注文を出す。

- 注文時の価格
    - 注文の直前に板のbidsを取得して「ギリギリmakerとして注文できる価格」で指値で注文する。ただし必ずmakerとなる保証はない。

- 定期購入
    - インストール後の最初の`order.sh`の実行（前回注文した時刻を記録したtime.txtが存在しない）か、2回目以降の実行でtime.txtの時刻からintervalが経過していれば、新規注文してtime.txtに時刻を出力し、orders.txtに注文のorder_idを出力する。

- スポット注文（ブラウザ画面）
    - time.txtの時刻とは無関係に注文できる。指定された金額で、上記の「注文時の価格」で購入できるだけの量を注文する。スポット注文のorder_idについてもorders.txtに記録するが、頭に`+`を付与して区別する。スポット注文については下記の「指値価格の調整」は行わない。

- 指値価格の調整
    - `order.sh`は、orders.txtに書かれたorder_idの中で先頭に`+`の付いていない注文の中で、未約定の注文について、もっと約定しやすい価格でかつmakerとして指値で注文し直し可能であれば注文し直し、orders.txtを更新する。

- バックアップと復元
    - 対象は、config.yaml、orders.txt、time.txt、APIキー
    - Dockerで実行時はこれらのファイルをコンテナ外のVolumeに保存することで永続化（docker runオプションに`-v my_volume:/home/hoge/data`を付与）

### 購入状況の確認

`balance.sh`、及び、ブラウザのサマリーや購入状況の画面は、orders.txtに記載されたorder_idの取引結果をbitbankccに問い合わせた結果を出力する。
