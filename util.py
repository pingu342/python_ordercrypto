import datetime

def save_current_time(file_path):
    # 現在時刻を取得
    now = datetime.datetime.now()

    # ファイルに書き込む形式の時刻文字列を作成
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # ファイルに書き込む
    with open(file_path, "w") as file:
        file.write(time_str)


def calculate_time_diff(file_path):
    # ファイルから時刻を読み込む
    try:
        with open(file_path, "r") as file:
            time_str = file.read().strip()
    except FileNotFoundError:
        return 60*60*24*365

    # ファイルに保存した時刻文字列をdatetimeオブジェクトに変換
    saved_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    # 現在時刻を取得
    now = datetime.datetime.now()

    # 差分を計算し、秒数を返す
    diff = now - saved_time
    return diff.total_seconds()

