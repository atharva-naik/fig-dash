#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jinja2
from typing import Union, Dict
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '0.0.0.0:5000'
# Qt imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QSplitter, QComboBox, QSizePolicy
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.webview import DebugWebView
# widget for handling excel/csv/tsv spreadsheet data, using x-spreadsheet.js and pandas as a backend (saving, formulae etc.)

spreadsheet_style = '''
QWidget#SpreadsheetViewer {
    color: #fff;
    border: 0px;
    background: transparent;
}'''
class SpreadsheetViewer(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.45):
        super(SpreadsheetViewer, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.zoom_factor = zoom_factor
        # self.spacing.
        self.webview = DebugWebView()
        self.webview.setHtml("x-spreadsheet editor not loaded")
        # add widgets to layout.
        self.layout.addWidget(self.webview.devToolsBtn)
        self.layout.addWidget(self.webview.splitter)
        # set layout.width
        self.setLayout(self.layout)
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
        self.editor_html = jinja2.Template(
            XSpreadsheetHtml.render(**self.sources)
        ).render(
            ICON_PACK_URL=FigD.icon("widget/spreadsheet/spreadsheet_icons.svg")
        )
        self.webview.load(FigD.createTempUrl(self.editor_html))
        self.webview.urlChanged.connect(self.onUrlChange)

    def onUrlChange(self):
        self.webview.setZoomFactor(self.zoom_factor)
        self.webview.loadFinished.connect(self.webview.loadDevTools)

    def setZoomFactor(self, zoom_factor: float=1):
        self.zoom_factor = zoom_factor

    def saveEditor(self, path: str):
        with open(path, 'w') as f:
            f.write(self.editor_html)


def test_spreadsheet():
    import sys
    import time
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    excel = SpreadsheetViewer()
    excel.show()
    s = time.time()
    excel.buildEditor(merge_mode=True)
    print(f"built code-mirror editor in {time.time()-s}s")
    excel.saveEditor("excel-editor.html")
    app.exec()


if __name__ == "__main__":
    test_spreadsheet()