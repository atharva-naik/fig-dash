#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::system::mailviewer")
# mail client UI.
import os
import jinja2
from typing import Union
from pathlib import Path
# fig-dash imports.
from fig_dash import FigD
from fig_dash.ui.browser import DebugWebView
# Qt5 imports
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QToolBar, QToolButton, QSizePolicy, QAction, QActionGroup, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect


class MailViewerMenu(QWidget):
    '''mail client menu tab.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MailViewerMenu, self).__init__(parent)


class MailViewerWebView(DebugWebView):
    '''mail client web view: contains list of all emails.'''


class MailViewerWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MailViewerWidget, self).__init__(parent)
# class MailClient(QWidget):
#     '''fig-dash mail client UI.'''
#     def __init__(self, parent: Union[None, QWidget]=None):
#         super(MailClient, self).__init__(parent)
def test_mailviewer():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    mail_client = MailViewerWidget(
        clipboard=app.clipboard(),
        background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        font_color="#fff",
    )
    mail_client.show()
    app.exec()


if __name__ == '__main__':
    test_mailviewer()