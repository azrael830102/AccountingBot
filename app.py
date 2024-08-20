from __future__ import unicode_literals

import ctypes
import os
import sys
import threading

import win32api  # package pywin32
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

from flask import Flask, abort, request
from infi.systray import SysTrayIcon
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from MessageHandler import MessageHandler

app = Flask(__name__)

channel_access_token = "j0+juQAPLM/TpiLYueU4aTQc8VtNVj5jSVRNrskQj4htLE//AcTcrdZ2LIPmOqYvq4M5v42IZ4L0Y0EBgtemwKMeslujWBPcVt2vmlCfFIU6lgyEgINju5rhmgPlDevafwwVPzAS0oIGeuVoKqw5ZAdB04t89/1O/w1cDnyilFU="
channel_secret = "ed44100c7733509cad6fd66a5a1c2776"

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
    msgHandler = MessageHandler()
    message = TextSendMessage(text=event.message.text).text
    resultMsg = msgHandler.handleMsg(message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resultMsg))


IsStart = False
IsStart_ngrok = False
IsShow = True
sys.stdout = open('AccountingBot_console.log', 'w')

def fire():
    port = int(os.environ.get('PORT', 9527))
    app.run(port=port,debug=True, use_reloader=False)
    

def startup(systray):
    global IsStart
    if not IsStart:
        threading.Thread(target=fire, daemon=True).start()

def fire_ngrok():
    target = os.getcwd().replace("\\","/") + "/resources/ngrok.exe"
    cmd = f'"{target}" http 9527'
    print(cmd)
    retValue = os.system(cmd)
    print(retValue)

def startup_ngrok(systray):
    global IsStart_ngrok
    if not IsStart_ngrok:
        IsStart_ngrok = True
        threading.Thread(target=fire_ngrok).start()


def on_quit_callback(systray):
    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    print("stop")
    sys.stdout.close()
    pass

def ShowOrHide(sysTrayIcon):
    global IsShow
    if(IsShow):
        IsShow = False
        hide(sysTrayIcon)
    else:
        IsShow = True
        show(sysTrayIcon)

def show(sysTrayIcon):
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    win32gui.ShowWindow(the_program_to_hide, win32con.SW_SHOW)

def hide(sysTrayIcon):
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

if __name__ == "__main__":
    menu_options = (("Startup accounting bot", None, startup),
                    ("Startup ngrok", None, startup_ngrok),
                    ("Show/Hide console", None, ShowOrHide),)
    icoPath = os.getcwd().replace("\\","/") + "/resources/AccountingBot.ico"
    systray = SysTrayIcon(icoPath, "Accounting bot Launcher", menu_options, on_quit=on_quit_callback)
    systray.start()
    pass