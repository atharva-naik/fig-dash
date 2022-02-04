import os
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QT_VERSION_STR


def collapseuser(path: str):
    return path.replace(os.path.expanduser("~"), "~")

def pyqtSleep(time: int=1000):
    '''
    A pyqt5 friendly version of time.sleep.
    time to wait in millis
    '''
    loop = QEventLoop()
    QTimer.singleShot(time, loop.quit)
    loop.exec_()

def truncStr(string):
    if len(string) > 20:
        return string[:10]+"..."+string[-6:]
    else:
        return string

def notify(msg=None, icon=None, title="Fig Dashboard", critical=False):
    import getpass
    import platform
    if msg is None: 
        msg = f"Hello {getpass.getuser()}!"
    # /home/atharva/GUI/fig-dash/resources/icons/logo.svg
    if platform.system() == "Linux":
        # use notify send for Linux.
        code = f'''notify-send "Fig Dashboard" "{msg}"'''
        if icon: code += f" -i {icon}" 
        if critical: code += f" -u critical"
        print("\x1b[34;1mcode:\x1b[0m", code)
        os.system(code)

def secs_to_hms(secs):
    hrs = secs // 3600
    mins = (secs % 3600) // 60
    
    return (hrs, mins, secs)

def QFetchIcon(url: str, is_svg=True) -> QIcon:
    import requests
    import tempfile

    content = requests.get(url)
    if is_svg: 
        path = "/tmp/lol1_2hjalx_ffl2c.svg"
        with open(path, "w") as f:
            f.write(content.text)
    else: 
        path = "/tmp/lol1_2hjalx_ffl2c.png"
        with open(path, "wb") as f:
            f.write(content.content)
    icon = QIcon(path)
    # os.remove(path)
    return icon
