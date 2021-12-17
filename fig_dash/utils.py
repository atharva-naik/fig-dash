import os
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import Qt, QT_VERSION_STR


def collapseuser(path: str):
    return path.replace(os.path.expanduser("~"), "~")

def description():
    pass