from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from MessageHandler import MessageHandler
import configparser

msgHandler = None
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    message = TextSendMessage(text=event.message.text).text
    resultMsg = msgHandler.handleMsg(message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resultMsg))

if __name__ == "__main__":
    msgHandler = MessageHandler()
    port = int(os.environ.get('PORT', 9527))
    app.run(port=port)
    pass