#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cProfile import label
import os
from typing import Union, Tuple
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QPoint
from PyQt5.QtWidgets import QMenu, QLabel, QWidget, QAction, QMainWindow, QApplication, QVBoxLayout, QGraphicsBlurEffect
# fig dash imports.
from fig_dash.assets import FigD


class BlurLabel(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, text: str=""):
        super(BlurLabel, self).__init__(parent)
        # self.setAttribute(Qt.WA_StyledBackground)
        self.widget = QWidget()
        effect = QGraphicsBlurEffect(blurRadius=10)
        self.widget.setGraphicsEffect(effect)

        self._label = QLabel(text)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.widget)
        self.label.setParent(self)
        self.move(self.width()//2, self.height()//2)
        self.setAttribute(Qt.WA_TranslucentBackground)

    @property
    def label(self):
        return self._label

    def sizeHint(self):
        return self._label.sizeHint()

    def resizeEvent(self, event):
        self._label.resize(self.size())
        self._label.raise_()
        self.move(self.width()//2, self.height()//2)
        return super().resizeEvent(event)

    def setStyleSheet(self, stylesheet):
        self.widget.setStyleSheet(stylesheet)


class BlurMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(BlurMenu, self).__init__(parent)
        self.widget = QWidget()
        blur_effect = QGraphicsBlurEffect(blurRadius=5)
        self.widget.setGraphicsEffect(blur_effect)

        self._menu = QMenu(parent=self)
        self.menu.setStyleSheet(""" background-color : transparent; color : black""")
        self.menu.setContentsMargins(0, 0, 0, 0)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    @property
    def menu(self):
        return self._menu

    def sizeHint(self):
        return self._menu.sizeHint()

    def resizeEvent(self, event):
        self._menu.resize(self.size())
        self._menu.raise_()
        return super().resizeEvent(event)


class TestWindow(QMainWindow):
    def contextMenuEvent(self, event):
        self.menu = BlurMenu(self)
        self.menu.widget.setStyleSheet("""
        QWidget { 
            background: rgba(0,0,0,0.9); 
            color: #fff;
        }""")
        self.menu.addAction(QAction("Test 1"))
        self.menu.addAction(QAction("Test 2"))
        print("context menu event")
        self.menu.menu.popup(event.globalPos())


def test_blurmenu():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec()

def test_blurlabel():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    label = BlurLabel(text="For the record, I think the widget does have a transparent background, but it's obviously sitting on something else that doesn't")
    label.setStyleSheet("background: rgba(29,29,29,0.9); color: #fff;")
    label.show()
    app.exec()


if __name__ == "__main__":
    # test_blurmenu()
    test_blurlabel()