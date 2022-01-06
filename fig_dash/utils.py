import os
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QT_VERSION_STR


def collapseuser(path: str):
    return path.replace(os.path.expanduser("~"), "~")

def description():
    pass

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
