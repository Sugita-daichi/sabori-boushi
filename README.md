# sabori-boushi (サボり防止システム) 

iPhoneのオートメーション機能とLINE Messaging API、FastAPIを組み合わせた、自分専用の**研究室サボり防止・強制登校催促システム**です。

毎朝、指定の時間に研究室のWi-Fiに接続していない場合、研究室に到着するまでLINEで容赦なく催促メッセージが届き続けます。

## システム概要

1. **朝のサボり検知 (トリガー)**
   - 毎朝 10:00 にiPhoneのショートカット（オートメーション）が自動起動。
   - 今接続しているWi-FiのSSIDをチェックし、研究室のWi-Fiでなければサーバー（`/sabori-check`）にPOSTリクエストを送信。
2. **LINE無限催促 (ペナルティ)**
   - サーバー側はシグナルを受信すると、バックグラウンド処理で10分おきに「研究室に行け！」とLINEでプッシュ通知を送り続けます。
3. **研究室到着検知 (ストッパー)**
   - 研究室に到着し、iPhoneが自動で研究室のWi-Fiに接続した瞬間、サーバー（`/arrived`）にPOSTリクエストを送信。
   - 催促ループが停止し、「お疲れ様でした」とLINEが届きます。

## 技術スタック

- **Backend:** Python 3.10+ / FastAPI / Uvicorn
- **API/Integration:** LINE Messaging API (line-bot-sdk)
- **Client Trigger:** iOS Shortcuts (Automations)
- **Deployment:** Render (Free Web Service)

## セットアップ

### 1. サーバーサイド (Python)
必要なライブラリをインストールし、サーバーを起動します。

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000