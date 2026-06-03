import asyncio
import os
from fastapi import FastAPI, BackgroundTasks
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = FastAPI()

# LINEの環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("YOUR_LINE_USER_ID")  

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

is_saboring = False


async def send_reminders_until_arrival():
    """研究室に到着するまで、定期的にLINE催促を送り続けるバックグラウンドタスク"""
    global is_saboring

    interval_seconds = 600

    print("サボり監視アラートを開始しました。")

    while is_saboring:
        try:
            line_bot_api.push_message(
                USER_ID, TextSendMessage(text="研究室に行け！！\n（到着したらLINEのリンク、またはショートカットから報告してください）")
            )
            print("催促メッセージを送信しました。")
        except Exception as e:
            print(f"LINE送信エラー: {e}")

        await asyncio.sleep(interval_seconds)


@app.post("/sabori-check")
def sabori_check(background_tasks: BackgroundTasks):
    """iPhoneの朝9:00オートメーションから叩かれるエンドポイント"""
    global is_saboring

    if is_saboring:
        return {"status": "already_monitoring"}

    is_saboring = True
    background_tasks.add_task(send_reminders_until_arrival)

    return {"status": "sabori_detected_start_monitoring"}


@app.post("/arrived")
def arrived():
    """研究室に到着した（Wi-Fiに繋がった）時に叩く、または手動で止めるエンドポイント"""
    global is_saboring

    if is_saboring:
        is_saboring = False  

        try:
            line_bot_api.push_message(
                USER_ID, TextSendMessage(text="研究室への到着を確認しました！今日も研究頑張りましょう！")
            )
        except Exception as e:
            print(f"LINE送信エラー: {e}")

        return {"status": "stopped_monitoring", "message": "お疲れ様でした！"}

    return {"status": "not_monitoring", "message": "現在サボり監視は動いていません。"}