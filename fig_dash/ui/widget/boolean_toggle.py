#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.api.browser.url.parse import UrlOrQuery
# qtwidgets import.
from qtwidgets import AnimatedToggle
# PyQt5 imports
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QPoint, QUrl, QEvent, QStringListModel, QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QWidget, QAction, QMainWindow, QToolButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication


class BooleanToggleBtn(QWidget):
    def __init__(self, parent=None,
                 checked_color="#FFB000", 
                 pulse_checked_color="#44FFB000", 
                 width=65, **kwargs) -> None:
        super(BooleanToggleBtn, self).__init__(parent)
        self.toggleBtn = AnimatedToggle(
            checked_color=checked_color, 
            pulse_checked_color=pulse_checked_color, 
        )
        text = kwargs.get("text")
        orient = kwargs.get("orient", "vertical")
        if orient == "vertical":
            self.layout = QVBoxLayout()
        elif orient == "horizontal":
            self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.toggleBtn, 0, Qt.AlignCenter)
        if text:
            self.label = QLabel(text)
            self.layout.addWidget(self.label, 0, Qt.AlignCenter)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setWordWrap(True)
            self.label.setStyleSheet("background: red; padding: 0px;")
        self.layout.addStretch(1)
        self.toggleBtn.setFixedWidth(width)
        self.setLayout(self.layout)
        self.setStyleSheet("background: yellow;")
        # self.setStyleSheet("")
        # print(vars(self))
class BooleanToggleTestWindow(QMainWindow):
    def __init__(self):
        super(BooleanToggleTestWindow, self).__init__()
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.boolean_btn = BooleanToggleBtn(self, text="window mode")
        self.layout.addWidget(self.boolean_btn)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)


def test_boolean_toggle():
    import sys
    import platform
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    window = BooleanToggleTestWindow()
    # QFontDatabase.addApplicationFont(
    #     FigD.font("BeVietnamPro-Regular.ttf")
    # )
    window.setGeometry(200, 200, 160, 120)
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    app.setWindowIcon(FigD.Icon("system/fileviewer/logo.svg"))
    window.show()
    app.exec()


if __name__ == "__main__":
    test_boolean_toggle()