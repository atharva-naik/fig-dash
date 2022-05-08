#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import jinja2
import datetime
from typing import Union
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.titlebar import WindowTitleBar 
# PyQt5 imports
from PyQt5.QtGui import QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QScrollArea, QTabWidget, QToolBar, QLabel, QPushButton, QToolButton, QSizePolicy, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QAction, QCalendarWidget, QGraphicsDropShadowEffect, QApplication, QMainWindow

# Clipboard UI.
class DashClipboardUI(QMainWindow):
    def __init__(self):
        super(DashClipboardUI, self).__init__()
        QApplication.clipboard().dataChanged.connect(
            self.onDataChanged
        )
        self.clipboard_ui = self.initCentralWidget()
        self.setCentralWidget(self.clipboard_ui)
        self.history = []

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setAttribute(Qt.WA_TranslucentBackground)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("""
        QScrollArea {
            background-position: center;
            background: transparent;
            border: 0px;
        }
        QScrollBar:vertical {
            border: 0px solid #999999;
            width: 15px;    
            margin: 0px 0px 0px 0px;
            background-color: rgba(255, 255, 255, 0);
        }
        QScrollBar::handle:vertical {         
            min-height: 0px;
            border: 0px solid red;
            border-radius: 0px;
            background-color: transparent;
        }
        QScrollBar::handle:vertical:hover {         
            background-color: rgba(255, 255, 255, 0.5);
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }""")

        return scrollArea

    def initStack(self):
        stack = QWidget()
        stack.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
        }""")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        stack.setLayout(layout)
        stack.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
        }""")

        return self.wrapInScrollArea(stack)

    def initSearchBar(self):
        searcharea = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        searcharea.setLayout(layout)

        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Search Clipboard!")
        searchbar.setStyleSheet(
        """QLineEdit {
            color: #fff;
            background: #292929;
        }""")
        layout.addWidget(searchbar)

        return searcharea

    def initCentralWidget(self):
        centralWidget = QWidget()
        # layout.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # search bar.
        self.searchbar = self.initSearchBar()
        self.layout.addWidget(self.searchbar)
        # central display stack.
        self.stack = self.initStack()
        self.stackLayout = self.stack.widget().layout()
        print(self.stackLayout)
        self.layout.addWidget(self.stack)
        self.layout.addStretch(1)

        centralWidget.setLayout(self.layout)
        centralWidget.setObjectName("ClipboardViewerWidget")
        centralWidget.setStyleSheet("""
        QWidget#ClipboardViewerWidget {
            border-radius: 20px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 0.98), stop : 0.6 rgba(29, 29, 29, 0.98));
        }""")

        return centralWidget

    def onDataChanged(self):
        # print(i)
        text = QApplication.clipboard().text()
        self.append(text)

    def connectTitlebar(self, titlebar: WindowTitleBar):
        self.titlebar = titlebar
        self.titlebar.connectWindow(self)

    def initClipboardItem(self, text: str):
        item = QTextEdit()
        item.setText(text)
        item.setStyleSheet("""
        QTextEdit {
            color: #fff;
            border: 0px;
            border-radius: 5px;
            background: #484848;
        }""")

        return item

    def append(self, text: str):
        print(f"\x1b[31;1mui.system.clipboard::DashClipboardUI::append\x1b[0m({text})")
        self.history.append(text)
        clipboard_item = self.initClipboardItem(text)
        self.stackLayout.insertWidget(0, clipboard_item)

def test_clipboard_ui():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QToolTip {
        color: #fff;
        border: 0px;
        padding-top: -1px;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: -1px;
        font-size:  17px;
        background: #000;
        font-family: 'Be Vietnam Pro', sans-serif;
    }""")
    screen_rect = app.desktop().screenGeometry()
    w, h = screen_rect.width()//2, screen_rect.height()//2
    # create and reposition clipboard UI.
    clipboard_ui = DashClipboardUI()
    # add the custom window titlebar.
    titlebar = WindowTitleBar(background="purple")
    # titlebar.setStyleSheet("background: #292929; color: #fff;")
    clipboard_ui.layout.insertWidget(0, titlebar)
    clipboard_ui.connectTitlebar(titlebar)
    # set window icon, title and flags.
    clipboard_ui.setWindowIcon(FigD.Icon("system/clipboard/window_icon.png"))
    clipboard_ui.setWindowTitle("Clipboard Viewer")
    clipboard_ui.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    clipboard_ui.setAttribute(Qt.WA_TranslucentBackground)
    # reposition window and show UI.
    clipboard_ui.move(w, h)
    clipboard_ui.show()
    
    app.exec()


if __name__ == "__main__":
    test_clipboard_ui()