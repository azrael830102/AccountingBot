import os
import threading

from infi.systray import SysTrayIcon

IsStart = False

def fire():
    target = os.getcwd().replace("\\","/") + "/resources/ngrok.exe"
    cmd = f'"{target}" http 9527'
    print(cmd)
    retValue = os.system(cmd)
    print(retValue)

def startup(systray):
    global IsStart
    if not IsStart:
        IsStart = True
        threading.Thread(target=fire).start()
        
def on_quit_callback(systray):
    from win32api import GenerateConsoleCtrlEvent
    CTRL_C_EVENT = 0
    GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)
    pass

menu_options = (("Startup ngrok", None, startup),)
icoPath = os.getcwd().replace("\\","/") + "/resources/ngrok.ico"
systray = SysTrayIcon(icoPath, "ngrok Launcher", menu_options, on_quit=on_quit_callback)
systray.start()