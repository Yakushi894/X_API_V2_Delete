import json
import re
import time
from requests_oauthlib import OAuth1Session

# --- 設定エリア ---
CK = 'APIキー'
CS = 'APIシークレット'
AT = 'アクセストークン'
ATS = 'アクセストークンシークレット'

FILE_PATH = '{ここにtweets.jsのパスを入力・GoogleColabで稼働確認}'  # tweets.jsのパス
# ----------------

# 1. tweets.js からツイートIDを抽出
def get_tweet_ids(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 冒頭のJavaScript変数代入部分を削除して純粋なJSONにする
        json_text = re.sub(r'^window\.YTD\.tweets\.part\d+\s*=\s*', '', content)
        data = json.loads(json_text)
        
        # tweet.id または tweet.id_str を取得
        return [item['tweet']['id'] for item in data]

# 2. 削除の実行
def delete_tweets():
    ids = get_tweet_ids(FILE_PATH)
    print(f"{len(ids)} 件のツイートが見つかりました。削除を開始します。")
    
    twitter = OAuth1Session(CK, CS, AT, ATS)
    
    for i, tweet_id in enumerate(ids):
        url = f"https://api.x.com/2/tweets/{tweet_id}"
        response = twitter.delete(url)
        
        if response.status_code == 200:
            print(f"[{i+1}/{len(ids)}] 成功: {tweet_id}")
        elif response.status_code == 429:
            print("レート制限に達しました。しばらく待ちます...")
            time.sleep(900)  # 15分待機
        else:
            print(f"[{i+1}/{len(ids)}] 失敗: {tweet_id} (Status: {response.status_code})")
        
        # 連続リクエストで止められないよう少し間隔を空ける
        time.sleep(1)

if __name__ == "__main__":
    delete_tweets()
