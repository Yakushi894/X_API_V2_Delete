# X (Twitter) Tweet Mass Deleter

Twitterからダウンロードしたアーカイブデータ（`tweets.js`）を解析し、記載されているすべてのツイートを X API v2 を利用して一括削除するPythonスクリプトです。

## 📋 概要
このスクリプトは、手動で消すのが困難な大量の過去ツイートを、APIを通じて自動で削除します。
Google Colab または ローカルの Python 環境で動作します。

## 🛠 事前準備

1. **X API の取得と設定**
   - [X Developer Portal](https://x.com) で App を作成します。
   - **重要**: `User authentication settings` で App permissions を **「Read and Write」** に変更してください（デフォルトの Read-only では削除できません）。
   - 設定変更後、`Access Token` と `Access Token Secret` を再生成（Regenerate）してください。

2. **アーカイブデータの準備**
   - Xの「設定とプライバシー」からアーカイブをリクエストし、ダウンロードします。
   - 解凍したフォルダの中にある `data/tweets.js` を用意します。

## 🚀 使い方

### 1. ライブラリのインストール
```bash
pip install requests_oauthlib
```

### 2. スクリプトの準備
以下のコードを `delete_tweets.py` として保存し、各種キーと `tweets.js` のパスを入力します。

```python
import json
import re
import time
from requests_oauthlib import OAuth1Session

# --- 設定エリア ---
CK = 'APIキー'
CS = 'APIシークレット'
AT = 'アクセストークン'
ATS = 'アクセストークンシークレット'

FILE_PATH = 'tweets.js'  # tweets.jsのパスを指定
# ----------------

def get_tweet_ids(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        json_text = re.sub(r'^window\.YTD\.tweets\.part\d+\s*=\s*', '', content)
        data = json.loads(json_text)
        return [item['tweet']['id'] for item in data]

def delete_tweets():
    ids = get_tweet_ids(FILE_PATH)
    print(f"{len(ids)} 件のツイートが見つかりました。")
    
    twitter = OAuth1Session(CK, CS, AT, ATS)
    
    for i, tweet_id in enumerate(ids):
        url = f"https://x.com{tweet_id}"
        response = twitter.delete(url)
        
        if response.status_code == 200:
            print(f"[{i+1}/{len(ids)}] 成功: {tweet_id}")
        elif response.status_code == 429:
            print("レート制限に達しました。15分待機します...")
            time.sleep(900)
        else:
            print(f"[{i+1}/{len(ids)}] 失敗: {tweet_id} (Status: {response.status_code})")
        
        time.sleep(1)

if __name__ == "__main__":
    delete_tweets()
```

### 3. 実行
```bash
python delete_tweets.py
```

## ⚠️ 注意事項
- **削除制限**: X API の Free プランでは、1ヶ月に削除できるツイート数に制限があります。
- **復旧不可**: 一度削除したツイートは元に戻せません。
- **免責事項**: 本スクリプトの利用により生じた損害について、一切の責任を負いません。
