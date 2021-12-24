#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# Qt imports.
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QGraphicsBlurEffect
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
        QFontDatabase.addApplicationFont(
            FigD.font("datetime/digital-7.ttf")
        )
        self.desktop = self.desktop()
        self.window = DashWindow(**kwargs)
        width = self.window.width()
        # actions for tray icon context menu.
        self.showAction = QAction("Show")
        self.quitAction = QAction("Quit")
        self.logsAction = QAction("Get logs")
        self.supportAction = QAction("Collect support files")
        # connect functions to actions.
        self.quitAction.triggered.connect(self.quit)
        # tray icon menu.
        self.trayMenu = QMenu()
        self.trayMenu.addAction(self.logsAction)
        self.trayMenu.addAction(self.showAction)
        self.trayMenu.addAction(self.quitAction)
        self.trayMenu.addAction(self.supportAction)
        # tray icon button.
        self.trayIcon = QSystemTrayIcon(QIcon(kwargs.get("icon")), self)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()
        # self.window.tabs.dropdown.initPos(width=width)
        self.setWindowFlags("frameless", "ontop")
        self.setCursor()
        # self.window.setWindowIcon(QIcon(kwargs.get("icon")))
    def setWindowFlags(self, *flags):
        self.window.setFlags(*flags)

    def notify(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            currentWidget = self.window.tabs.currentWidget()
            currentWidget.setGraphicsEffect(QGraphicsBlurEffect(blurRadius=10))
            # print("bluring background")
        if event.type() == QEvent.WindowActivate:
            currentWidget = self.window.tabs.currentWidget()
            currentWidget.setGraphicsEffect(None)
            # print("unbluring background")
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