import ctypes
import os
import sys

import win32api  # package pywin32
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import threading

from infi.systray import SysTrayIcon

sys.stdout = open('ngrokLauncher_console.log', 'w')

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
    print("stop")
    sys.stdout.close()
    pass

def show(sysTrayIcon):
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    win32gui.ShowWindow(the_program_to_hide, win32con.SW_SHOW)

def hide(sysTrayIcon):
    the_program_to_hide = ctypes.windll.kernel32.GetConsoleWindow()
    win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

try:
    menu_options = (("Startup ngrok", None, startup),
                    ("Show console", None, show),
                    ("Hide console", None, hide),)
    icoPath = os.getcwd().replace("\\","/") + "/resources/ngrok.ico"
    systray = SysTrayIcon(icoPath, "ngrok Launcher", menu_options, on_quit=on_quit_callback)
    systray.start()

except Exception as e:
    print(e)
    sys.stdout.close()

