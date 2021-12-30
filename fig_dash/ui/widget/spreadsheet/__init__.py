#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jinja2
from typing import Union, Dict
# Qt imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QComboBox, QSizePolicy
# fig-dash imports.
from fig_dash.assets import FigD
# widget for handling excel/csv/tsv spreadsheet data, using x-spreadsheet.js and pandas as a backend (saving, formulae etc.)

spreadsheet_style = '''
QWidget#SpreadsheetViewer {
    color: #fff;
    border: 0px;
    background: transparent;
}'''
class SpreadsheetViewer(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(SpreadsheetViewer, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # self.spacing.

        self.webview = QWebEngineView()
        self.webview.setHtml("x-spreadsheet editor not loaded")
        self.setStyleSheet(spreadsheet_style)
        self.setObjectName("SpreadsheetViewer")

    def buildEditor(self, **args):
        from fig_dash.ui.widget.spreadsheet.html import XSpreadsheetHtml
        from fig_dash.ui.widget.spreadsheet.xspreadsheet import XSpreadsheetJS, XSpreadsheetCSS

        self.sources = {
            "DATA": "",
            "XSPREADSHEET_JS": XSpreadsheetJS,
            "XSPREADSHEET_CSS": XSpreadsheetCSS,
        }
        # render the final html.
        self.editor_html = XSpreadsheetHtml.render(**self.sources)
        self.setHtml(self.editor_html)

    def saveEditor(self, path: str):
        with open(path, 'w') as f:
            f.write(self.editor_html)