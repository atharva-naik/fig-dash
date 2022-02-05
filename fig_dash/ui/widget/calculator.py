#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Qt5 imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QColor, QKeySequence, QIcon
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize, QPoint, QObject
from PyQt5.QtWidgets import QToolBar, QToolButton, QSplitter, QLabel, QWidget, QAction, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QTextEdit, QPlainTextEdit, QShortcut, QSpacerItem
# fig_dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.effects import WindowHighlightEffect


class DashCalculator(QMainWindow):
    def __init__(self):
        super(DashCalculator, self).__init__()
        self.calculator = self.initCentralWidget()
        self.setCentralWidget(self.calculator)
        self.statusBar().setStyleSheet("background: transparent; color: #fff;")
        self.statusBar().showMessage("message")
        self.statusBar().setFixedHeight(20)
        self.setStyleSheet("""
        QMainWindow {
            background: #292929;
        }""")
        # set window opacity.
        self.setWindowOpacity(0.98)
        # apply background effects.
        ## apply glow effect for the keys.
        background_glow = QGraphicsDropShadowEffect()
        background_glow.setOffset(0,0)
        background_glow.setColor(QColor(252, 94, 3))
        background_glow.setBlurRadius(20)
        self.calculator.setGraphicsEffect(background_glow)
        ## apply highlight effect on the widget.
        highlight_effect = WindowHighlightEffect()
        self.setGraphicsEffect(highlight_effect)

    def initInput(self):
        inp = QTextEdit()
        inp.setAlignment(Qt.AlignRight)
        inp.setPlaceholderText("0")
        inp.setReadOnly(True)
        inp.setFixedHeight(140)
        inp.setStyleSheet("""
        QTextEdit {
            font-size: 65px;
            margin-top: 10px;
            margin-left: 10px;
            margin-right: 10px;
            border: 0px;
            background: #fff;
        }""")

        return inp
    
    def initKeypad(self):
        keypad = QWidget()
        # create and set layout.
        self.keypadLayout = QGridLayout()
        self.keypadLayout.setContentsMargins(0, 10, 0, 10)
        self.keypadLayout.setSpacing(10)
        keypad.setLayout(self.keypadLayout)
        # create spacer grid.
        num_cols = 4
        self.spacers = [(QSpacerItem(5, 50, QSizePolicy.Expanding, QSizePolicy.Fixed), QSpacerItem(5, 50, QSizePolicy.Expanding, QSizePolicy.Fixed)) for i in range(num_cols)]
        # add all the keys to the grid.
        self.keypadLayout.addItem(self.spacers[0][0], 0, 0) 
        self.leftBracket = self.initKey("(")
        self.keypadLayout.addWidget(self.leftBracket, 0, 1)
        self.rightBracket = self.initKey(")")
        self.keypadLayout.addWidget(self.rightBracket, 0, 2)
        self.percentKey = self.initKey("%")
        self.keypadLayout.addWidget(self.percentKey, 0, 3)
        self.clearLetter = self.initKey("CE")
        self.keypadLayout.addWidget(self.clearLetter, 0, 4)
        self.keypadLayout.addItem(self.spacers[0][1], 0, 5)

        return keypad

    def initKey(self, symbol, size=(100,50)):
        key = QToolButton()
        key.setText(symbol)
        key.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding-top: 5px;
            padding-left: 15px;
            padding-right: 15px;
            padding-bottom: 5px;
            border-radius: 5px;
            background: black;
            font-size: 20px;
        }
        QToolButton:hover {
            color: #292929;
            font-weight: bold;
            background: orange;
        }""")
        key.setFixedWidth(size[0])
        key.setFixedHeight(size[1])

        return key

    def initResult(self):
        result = QLineEdit()
        result.setReadOnly(True)
        result.setAlignment(Qt.AlignRight)
        result.setPlaceholderText("0")
        self.historyAction = QAction()
        self.historyAction.setIcon(FigD.Icon("widget/calculator/history.svg"))
        # blank action for formatting.
        self.blank = QAction()
        # self.blank.setIcon(FigD.Icon("widget/calculator/history.svg"))
        result.addAction(self.blank, result.LeadingPosition)
        result.addAction(self.historyAction, result.LeadingPosition)
        result.setStyleSheet("""
        QLineEdit {
            border: 0px;
            margin-left: 10px;
            margin-right: 10px;
            font-size: 35px;
            padding-left: 5px;
            padding-right: 5px;
            background: #fff;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.2 #bbb, stop : 0.6 #aaa, stop: 0.8 #bbb); */
        }""")
        result.setFixedHeight(40)

        return result

    def initCentralWidget(self):
        centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # create widgets.
        self.input = self.initInput()
        self.result = self.initResult()
        self.keypad = self.initKeypad()
        # add widgets to vertical layout.
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.result)
        self.layout.addWidget(self.keypad)
        self.layout.addStretch(1)
        centralWidget.setLayout(self.layout)
        # centralWidget.setStyleSheet("""background: rgba(0, 0, 0, 0.8);""")

        return centralWidget


def test_calculator():
    import sys
    from PyQt5.QtWidgets import QApplication
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    calculator = DashCalculator()
    # calculator.setStyleSheet("background: tranparent; border: 0px;")
    calculator.setGeometry(200, 200, 800, 600)
    calculator.setWindowFlags(Qt.WindowStaysOnTopHint)
    # fileviewer.saveScreenshot("fileviewer.html")
    calculator.show()
    app.exec()


if __name__ == "__main__":
    test_calculator()