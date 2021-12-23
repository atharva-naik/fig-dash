#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# Qt imports.
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash._ui import DashWindow
# Contains all the fig dashboard code.


class DashUI(QApplication):
    def __init__(self, argv, **kwargs):
        FigD(kwargs.get("resources", "resources"))
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            print("high resolution")
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        super(DashUI, self).__init__(argv)
        self.desktop = self.desktop()
        self.window = DashWindow(**kwargs)
        width = self.window.width()
        # self.window.tabs.dropdown.initPos(width=width)
        self.setWindowFlags("frameless", "ontop")
        self.setCursor()

    def setWindowFlags(self, *flags):
        self.window.setFlags(*flags)

    def notify(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            # print("bluring background")
            pass
        if event.type() == QEvent.WindowActivate:
            # print("unbluring background")
            pass
        return super().notify(obj, event)

    def launch(self):
        '''
        launch app ui.
        show QMainWindow and then run QApplication
        '''
        self.window.show()
        sys.exit(self.run())

    def run(self):
        '''execute app ui.'''
        self.exec_()

    def setCursor(self):
        '''setup cursor image.'''
        self.setCursorFlashTime(1000)
        # pixmap = QPixmap(__icon__("cursor.svg")).scaledToWidth(32).scaledToWidth(32)
        # cursor = QCursor(pixmap, 32, 32)