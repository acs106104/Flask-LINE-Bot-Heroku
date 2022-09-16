import os
from datetime import datetime
import json

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, BeaconEvent, FlexSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"Echo: {get_message}")
    line_bot_api.reply_message(event.reply_token, reply)

@handler.add(BeaconEvent)
def handle_beacon(event):   
    hwid = event.beacon.hwid
    # reply = TextSendMessage(text=f"Beacon 新通知！\nGot beacon event. hwid= {hwid}")
    reply = FlexSendMessage(
    alt_text='Beacon 通知！',
    contents={
        "type": "bubble",
        "direction": "ltr",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "Beacon 通知",
                "weight": "bold",
                "color": "#000000FF",
                "align": "center",
                "gravity": "center",
                "contents": []
            }
            ]
        },
         "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "接收到的 hwid: " + str(hwid),
                "align": "center",
                "contents": []
            }
            ]
        }
    }
    
)
    line_bot_api.reply_message(event.reply_token, reply)

    # "hero": {
    #         "type": "image",
    #         "url": "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/3e7653db-f3c4-40c9-9f32-c31d7447f7de/sketch-1531214280539.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45/20220916/us-west-2/s3/aws4_request&X-Amz-Date=20220916T132633Z&X-Amz-Expires=86400&X-Amz-Signature=6cc6f8d8b9e9208c3b4725681d0c9e9c3825799afd813718c352abc4dd757674&X-Amz-SignedHeaders=host&response-content-disposition=filename =\"sketch-1531214280539.png\"&x-id=GetObject",
    #         "size": "full",
    #         "aspectRatio": "1.51:1",
    #         "aspectMode": "fit"
    #     },
        # "body": {
        # "type": "box",
        # "layout": "vertical",
        # "contents": [
        # {
        #     "type": "text",
        #     "text": "接收到的 hwid: " + str(hwid),
        #     "align": "center",
        #     "contents": []
        # }
        # ]
        # }