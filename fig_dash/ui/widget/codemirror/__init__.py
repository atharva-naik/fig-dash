#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union, Dict
# Qt imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QComboBox
# fig-dash imports.
from fig_dash.assets import FigD


class CodeMirrorBtn(QToolButton): 
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(CodeMirrorBtn, self).__init__(parent)
        icon = kwargs.get("icon")
        if icon:
            self.inactive_icon = os.path.join("widget/codemirror", icon)
            stem, ext = os.path.splitext(icon)
            self.active_icon = os.path.join("widget/codemirror", stem+"_active"+ext)
            self.setIcon(FigD.Icon(self.inactive_icon))
        tip = kwargs.get("tip", "a tip")
        size = kwargs.get("size", (23,23))
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(CodeMirrorBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(CodeMirrorBtn, self).leaveEvent(event)



class CodeMirrorTextBtn(QToolButton): 
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(CodeMirrorTextBtn, self).__init__(parent)
        text = kwargs.get("text")
        self.setText(text)
        tip = kwargs.get("tip", "a tip")
        size = kwargs.get("size", (23,23))
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 16px;
            background: transparent;
        }
        QToolButton:hover {
            color: #eb5f34;
        }''')


class CodeMirrorThemeDropdown(QComboBox):
    def __init__(self, themes: Dict[str, str], webview: Union[QWebEngineView, None]=None):
        super(CodeMirrorThemeDropdown, self).__init__()
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setMaximumHeight(100)
        self.theme_map = themes
        self.themes = list(themes.keys()) 
        self.webview = webview
        self.setEditable(True)
        # ignored if combobox is non editable for Gtk
        self.setMaxVisibleItems(8)
        for theme in themes:
            self.addItem(theme)
        self.currentIndexChanged.connect(self.changeTheme)
        # self.setFixedWidth(300)
    def changeTheme(self, i):
        theme = self.themes[i]
        # print(i, theme)
        # self.webview.setTheme(theme)
code_mirror_style = '''
QWidget#CMEditor {
    color: #fff;
    border: 0px;
    background: #292929;
}'''
class CodeMirrorMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 themes: Dict[str, str]={}, webview: Union[str, QWebEngineView]=None):
        super(CodeMirrorMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.debugBtn = CodeMirrorBtn(
            self, icon="debug.svg",
            tip="debug code"
        )
        self.formatBtn = CodeMirrorTextBtn(
            self, text="format",
            tip="format code according to language specification (if formatter is available)"
        )
        # self.mergeBtn = GitUIBtn(
        #     self, icon="merge.svg",
        #     tip="merge branch",
        # )
        # self.newBranchBtn = GitUIBtn(
        #     self, icon="new_branch.svg",
        #     tip="create new branch",
        # )
        # self.delBranchBtn = GitUIBtn(
        #     self, icon="delete_branch.svg",
        #     tip="delete branch",
        # )
        self.themeDropdown = CodeMirrorThemeDropdown(themes=themes, webview=webview)
        self.themeDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.formatBtn)
        self.layout.addWidget(self.themeDropdown)
        self.layout.addWidget(self.debugBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class CodeMirrorEditor(QWidget):
    '''codemirror code editor.'''
    def __init__(self, parent: Union[None, QWidget]=None):
        super(CodeMirrorEditor, self).__init__(parent)
        from fig_dash.ui.widget.codemirror.addon.comment.comment import CMCommentJS
        from fig_dash.ui.widget.codemirror.addon.comment.continuecomment import CMContinueCommentJS
        from fig_dash.ui.widget.codemirror.addon.dialog.dialog import CMDialogCSS, CMDialogJS
        from fig_dash.ui.widget.codemirror.lib.codemirror import CMCodeMirrorCSS, CMCodeMirrorJS
        from fig_dash.ui.widget.codemirror.mode import CMMimeTypeToLang
        from fig_dash.ui.widget.codemirror.theme import CMTheme

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.keymap = {}
        self.addon = {
            "comment/comment.js": CMCommentJS,
            "comment/continuecomment.js": CMContinueCommentJS,
            "dialog/dialog.css": CMDialogCSS,
            "dialog/dialog.js": CMDialogJS,
        }
        self.mode = {}
        self.theme = {}
        self.lib = {
            "codemirror.css": CMCodeMirrorCSS,
            "codemirror.js": CMCodeMirrorJS,
        }
        self.mimetype_to_lang = CMMimeTypeToLang
        self.webview = QWebEngineView()
        self.webview.setHtml("CM Editor")
        self.menubar = CodeMirrorMenu(themes=CMTheme, webview=self.webview)
        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)
        self.setObjectName("CMEditor")
        self.setStyleSheet(code_mirror_style)
        # self.a = {
        # }
    def setMode(self, mimetype: str="text"):
        lang = self.mimetype_to_lang[mimetype]
        exec(f"from fig_dash.ui.widget.codemirror.mode.{lang} import {lang.upper()}JS")

    def setTheme(self, theme: str=""):
        pass
        # self.webview.page().runJavaScript()


def test_code_mirror():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    cm = CodeMirrorEditor()
    cm.show()
    app.exec()


if __name__ == "__main__":
    test_code_mirror()