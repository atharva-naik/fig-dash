#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2
from typing import Union
# Qt5 imports.
from PyQt5.QtGui import QIcon, QColor, QMovie
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtWidgets import QSizePolicy, QWidget, QToolBar, QToolButton, QLabel, QAction, QApplication, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QLineEdit, QTextEdit
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.widget.richtexteditor import RichTextEditor, richtexteditor_style
# from fig_dash.ui.browser import Browser
ideas_widget_style = '''
QWidget {
    color: #fff;
    border: 0px;
    background: #1B161C;
}
QLabel {
    margin-top: 5px;
    margin-left: 10px;
    font-size: 20px;
    font-weight: bold;
}'''
# class IdeasTextArea(Browser):
#     def __init__(self, parent: Union[None, QWidget]=None, zoomFactor: float = 1):
#         super(IdeasTextArea, self).__init__(parent, zoomFactor)
#         self.webview = Browser(self, zoomFactor=1)
#         self.setObjectName("IdeasTextArea")
#         # self.webview.setHtml('''<h1>Loading quill<h1>''')
#         self.loadStarted.connect(self.afterLoad)
#         self.loadFinished.connect(self.beforeLoad)

#     def afterLoad(self):
#         print("loaded")
#         self.setFixedWidth(320)

#     def beforeLoad(self):
#         print("before loading")
#         self.setFixedWidth(300)
class IdeasWidget(QWidget):
    '''A do-dat to store the freshest of your ideas.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(IdeasWidget, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # create widgets.
        self.motif = QWidget()
        self.motifLayout = QVBoxLayout()
        self.motifLayout.setContentsMargins(0, 0, 0, 0)
        self.motif.setLayout(self.motifLayout)
        # populate motif widget.
        self.logo = QLabel()
        self.logo.setStyleSheet('''
        QLabel {
            border: 0px;
            background: #1B161C;
        }''')
        self.movie = QMovie(FigD.icon("widget/ideas/ideas.gif"))
        self.logo.setMovie(self.movie)
        self.movie.start()
        # self.logo.setIconSize(QSize(150,150))
        self.label = QLabel("Bottle your ideas!")
        self.label.setAlignment(Qt.AlignCenter)
        # motif.
        self.motifLayout.addWidget(self.label)
        self.motifLayout.addWidget(self.logo)
        self.motifLayout.addStretch(1)
        # search for/filter ideas.
        self.list = QWidget()
        self.listLayout = QVBoxLayout()
        self.listLayout.setContentsMargins(0, 0, 0, 0)
        self.list.setLayout(self.listLayout)
        self.list.setStyleSheet('''
        QLineEdit {
            color: #292929;
            width: 200px;
            background: #eb5f34;
            border-radius: 10px;
        }''')
        self.search = QLineEdit()
        self.search.setPlaceholderText("search in your ideas")
        self.searchAction = QAction(parent=self.list)
        self.searchAction.setIcon(FigD.Icon("widget/ideas/search.svg"))
        self.search.addAction(
            self.searchAction,
            self.search.LeadingPosition
        )
        # list view of ideas.
        self.listLayout.addWidget(self.blank())
        self.listLayout.addWidget(self.search)
        self.listLayout.addStretch(1)
        # self.scroll = 
        # populate edit area.
        self.edit = QWidget()
        self.editLayout = QVBoxLayout()
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        self.edit.setLayout(self.editLayout)
        
        # self.textarea = QTextEdit() 
        # self.textarea.setPlaceholderText("Jot down your ideas here!")
        # self.textarea.setStyleSheet('''font-size: 16px;''')
        self.textarea = RichTextEditor(self)
        self.textarea.setMaximumWidth(400)
        self.textarea.edit_tb.setMovable(False)
        self.textarea.file_tb.setMovable(False)
        self.textarea.font_tb.setMovable(False)
        self.textarea.format_tb.setMovable(False)
        self.textarea.edit_tb.hide()
        self.textarea.comboFont.setMaximumWidth(120)
        self.textarea.comboStyle.setMaximumWidth(120)
        self.textarea.statusBar().clearMessage()
        self.textarea.setMaximumHeight(240)
        # self.textarea = IdeasTextArea(self)
        # self.textarea.load(QUrl.fromLocalFile("/home/atharva/GUI/fig-dash/resources/static/ideas.html"))

        # editing area.
        self.editLayout.addWidget(self.blank(2))
        self.editLayout.addWidget(self.textarea)
        # populate widgets.
        self.layout.addWidget(self.motif)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.edit)
        # wrapper widget.
        wrapperWidget = QWidget()
        wrapperWidget.setLayout(self.layout)
        wrapperLayout = QVBoxLayout()
        wrapperLayout.setContentsMargins(0, 0, 0, 0)
        wrapperLayout.addWidget(wrapperWidget)
        # set layout.
        self.setLayout(wrapperLayout)
        self.setStyleSheet(ideas_widget_style)
        # apply glow effect.
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        self.setGraphicsEffect(glow_effect)
        # self.movie.stop()

    def toogle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def blank(self, height: int=5):
        blank = QWidget()
        blank.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        blank.setFixedHeight(height)

        return blank


def test_ideas():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    ideas = IdeasWidget()
    ideas.show()
    app.exec()
    # floatmenu.setAttribute(Qt.WA_TranslucentBackground)

if __name__ == '__main__':
    test_ideas()