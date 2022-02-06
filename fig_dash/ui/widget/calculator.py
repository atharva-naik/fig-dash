#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Qt5 imports.
from typing import Tuple
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QTextCursor
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize, QPoint, QObject
from PyQt5.QtWidgets import QToolBar, QToolButton, QSplitter, QLabel, QWidget, QAction, QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QTextEdit, QShortcut, QSpacerItem
# fig_dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.effects import WindowHighlightEffect


class CalculatorKey(QToolButton):
    def __init__(self, symbol: str, tip: str="tip", 
                 size: Tuple[int, int]=(100,50)) -> None:
        super(CalculatorKey, self).__init__()
        self.setText(symbol)
        self.setStyleSheet("""
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
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #292929;
        }""")
        self.setFixedWidth(size[0])
        self.setFixedHeight(size[1])
        self.setStatusTip(tip)
        self.setToolTip(tip)
        self.clicked.connect(self.keyUp)
        self.symbol = symbol

    def connectInput(self, inputField):
        self.input = inputField

    def keyUp(self):
        import pyautogui
        text = self.input.toPlainText().strip()
        if self.symbol == "CE":
            text = text[:-1]
        elif self.symbol == "x!":
            text = text + "!"
        else:
            text = text + self.symbol
        self.input.setText(text)
        pyautogui.hotkey("end")
        # self.input.cursor().movePosition(QTextCursor.End)
        # self.input.setCursorPosition(len(text))
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
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); 
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
        # inp.setReadOnly(True)
        inp.setFixedHeight(140)
        inp.setStyleSheet("""
        QTextEdit {
            font-size: 80px;
            margin-top: 10px;
            margin-left: 10px;
            margin-right: 10px;
            border: 0px;
            background: #fff;
            font-family: 'digital-7';
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
        num_rows = 5
        self.spacers = [(QSpacerItem(5, 50, QSizePolicy.Expanding, QSizePolicy.Fixed), QSpacerItem(5, 50, QSizePolicy.Expanding, QSizePolicy.Fixed)) for i in range(num_rows)]
        # add all the keys to the grid.
        ## first row.
        self.keypadLayout.addItem(self.spacers[0][0], 0, 0) 
        self.radianDegreeToggle = self.initKey("Rad | Deg", size=(250,50))
        self.keypadLayout.addWidget(self.radianDegreeToggle, 0, 1, 1, 2)
        self.factorial = self.initKey("x!", tip="factorial")
        self.keypadLayout.addWidget(self.factorial, 0, 3)
        self.leftBracket = self.initKey("(", tip="left bracket (start expression)")
        self.keypadLayout.addWidget(self.leftBracket, 0, 4)
        self.rightBracket = self.initKey(")", tip="right (end expression)")
        self.keypadLayout.addWidget(self.rightBracket, 0, 5)
        self.percentKey = self.initKey("%", tip="percent")
        self.keypadLayout.addWidget(self.percentKey, 0, 6)
        self.clearLetter = self.initKey("CE", tip="backspace")
        self.keypadLayout.addWidget(self.clearLetter, 0, 7)
        self.keypadLayout.addItem(self.spacers[0][1], 0, 8)
        ## second row.
        self.keypadLayout.addItem(self.spacers[1][0], 1, 0) 
        self.inv = self.initKey("Inv")
        self.keypadLayout.addWidget(self.inv, 1, 1)
        self.sin = self.initKey("sin")
        self.keypadLayout.addWidget(self.sin, 1, 2)
        self.ln = self.initKey("ln")
        self.keypadLayout.addWidget(self.ln, 1, 3)
        self.num7 = self.initKey("7")
        self.keypadLayout.addWidget(self.num7, 1, 4)
        self.num8 = self.initKey("8")
        self.keypadLayout.addWidget(self.num8, 1, 5)
        self.num9 = self.initKey("9")
        self.keypadLayout.addWidget(self.num9, 1, 6)
        self.div = self.initKey("÷")
        self.keypadLayout.addWidget(self.div, 1, 7)
        self.keypadLayout.addItem(self.spacers[1][1], 1, 8)
        ## third row.
        self.keypadLayout.addItem(self.spacers[2][0], 1, 0) 
        self.inv = self.initKey("π")
        self.keypadLayout.addWidget(self.inv, 2, 1)
        self.sin = self.initKey("cos")
        self.keypadLayout.addWidget(self.sin, 2, 2)
        self.ln = self.initKey("log")
        self.keypadLayout.addWidget(self.ln, 2, 3)
        self.num7 = self.initKey("4")
        self.keypadLayout.addWidget(self.num7, 2, 4)
        self.num8 = self.initKey("5")
        self.keypadLayout.addWidget(self.num8, 2, 5)
        self.num9 = self.initKey("6")
        self.keypadLayout.addWidget(self.num9, 2, 6)
        self.div = self.initKey("×")
        self.keypadLayout.addWidget(self.div, 2, 7)
        self.keypadLayout.addItem(self.spacers[2][1], 2, 8)
        ## fourth row.
        self.keypadLayout.addItem(self.spacers[3][0], 1, 0) 
        self.e = self.initKey("e")
        self.keypadLayout.addWidget(self.e, 3, 1)
        self.tan = self.initKey("tan")
        self.keypadLayout.addWidget(self.tan, 3, 2)
        self.root = self.initKey("√")
        self.keypadLayout.addWidget(self.root, 3, 3)
        self.num1 = self.initKey("1")
        self.keypadLayout.addWidget(self.num1, 3, 4)
        self.num2 = self.initKey("2")
        self.keypadLayout.addWidget(self.num2, 3, 5)
        self.num3 = self.initKey("3")
        self.keypadLayout.addWidget(self.num3, 3, 6)
        self.minus = self.initKey("-")
        self.keypadLayout.addWidget(self.minus, 3, 7)
        self.keypadLayout.addItem(self.spacers[3][1], 3, 8)
        ## fifth row.
        self.keypadLayout.addItem(self.spacers[4][0], 4, 0) 
        self.ans = self.initKey("Ans")
        self.keypadLayout.addWidget(self.ans, 4, 1)
        self.exp = self.initKey("EXP")
        self.keypadLayout.addWidget(self.exp, 4, 2)
        self.xpowery = self.initKey("xʸ")
        self.keypadLayout.addWidget(self.xpowery, 4, 3)
        self.num0 = self.initKey("0")
        self.keypadLayout.addWidget(self.num0, 4, 4)
        self.dot = self.initKey(".")
        self.keypadLayout.addWidget(self.dot, 4, 5)
        self.equal = self.initKey("=")
        self.keypadLayout.addWidget(self.equal, 4, 6)
        self.plus = self.initKey("+")
        self.keypadLayout.addWidget(self.plus, 4, 7)
        self.keypadLayout.addItem(self.spacers[4][1], 4, 8)

        return keypad

    def initKey(self, symbol, size=(120,50), tip="tip"):
        key = CalculatorKey(symbol, size=size, tip=tip)
        key.connectInput(self.input)

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
            font-family: 'digital-7';
            padding-left: 5px;
            padding-right: 5px;
            background: #fff;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.2 #bbb, stop : 0.6 #aaa, stop: 0.8 #bbb); */
        }""")
        result.setFixedHeight(40)

        return result

    def updateResult(self):
        math_eqn = self.input.toPlainText()
        result = None
        try:
            math_eqn = math_eqn.replace("[","(").replace("]",")")
            result = eval(math_eqn)
            # print(result)
            self.result.setText(f"{result}")
        except (SyntaxError, TypeError) as e:
            pass

    def initCentralWidget(self):
        centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # create widgets.
        self.input = self.initInput()
        self.result = self.initResult()
        self.keypad = self.initKeypad()
        self.input.textChanged.connect(self.updateResult)
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
    QFontDatabase.addApplicationFont(
        FigD.font("datetime/digital-7.ttf")
    )
    calculator = DashCalculator()
    # calculator.setStyleSheet("background: tranparent; border: 0px;")
    calculator.setGeometry(200, 200, 920, 500)
    calculator.setWindowFlags(Qt.WindowStaysOnTopHint)
    # fileviewer.saveScreenshot("fileviewer.html")
    calculator.show()
    app.exec()


if __name__ == "__main__":
    test_calculator()