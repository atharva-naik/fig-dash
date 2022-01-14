#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mail client UI.
from typing import Union
# qt5 imports.
from PyQt5.QtWidgets import QApplication, QWidget
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.browser import DebugWebView


class MailClientMenu(QWidget):
    '''mail client menu tab.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MailClientMenu, self).__init__(parent)


class MailClientWebView(DebugWebView):
    '''mail client web view: contains list of all emails.'''


class MailClient(QWidget):
    '''fig-dash mail client UI.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(MailClient, self).__init__(parent)


def test_mail_client():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    mail_client = MailClient(
        clipboard=app.clipboard(),
        background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        font_color="#fff",
    )
    mail_client.show()
    app.exec()

if __name__ == '__main__':
    test_mail_client()