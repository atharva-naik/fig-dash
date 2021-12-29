#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union, Dict
# Qt imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QComboBox, QSizePolicy
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


class CodeMirrorModeDropdown(QComboBox):
    def __init__(self, modes: Dict[str, str], webview: Union[QWebEngineView, None]=None):
        super(CodeMirrorModeDropdown, self).__init__()
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.modes = list(modes.keys())
        self.webview = webview
        self.setEditable(True)
        # ignored if combobox is non editable for Gtk
        self.setMaxVisibleItems(5)
        for lang in modes:
            self.addItem(lang)
        self.currentIndexChanged.connect(self.changeMode)

    def changeMode(self, i):
        lang = self.modes[i]
        print(i, lang)


class CodeMirrorThemeDropdown(QComboBox):
    def __init__(self, themes: Dict[str, str], webview: Union[QWebEngineView, None]=None):
        super(CodeMirrorThemeDropdown, self).__init__()
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
class CodeMirrorStatus(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                webview: Union[QWebEngineView, None]=None):
        super(CodeMirrorStatus, self).__init__(parent)    
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = webview
        self.layout.setSpacing(20)    
        self.num_warnings = self.initBtn(icon="warnings.png", text=" 0") 
        self.num_errors = self.initBtn(icon="errors.png", text=" 0") 
        self.permissions = self.initBtn(icon="pen.svg", text="[RW]")
        self.cursor_pos = QLabel("Ln 0, Col 0")
        self.enc_type = QLabel("UTF-8")
        self.eol_seq = QLabel("LF") 
        self.indent_type = self.initBtn(text="Spaces: 4")
        self.mimetype = QLabel("text/x-python") 
        # add widgets.
        self.layout.addStretch(1)
        self.layout.addWidget(self.num_warnings)
        self.layout.addWidget(self.num_errors)
        self.layout.addWidget(self.permissions)
        self.layout.addStretch(1)
        self.layout.addWidget(self.cursor_pos)
        self.layout.addWidget(self.indent_type)
        self.layout.addWidget(self.enc_type)
        self.layout.addWidget(self.mimetype)
        self.layout.addWidget(self.eol_seq)
        self.layout.addStretch(1)
        # set layout and style
        self.setLayout(self.layout)
        self.setObjectName("CodeMirrorStatus")
        self.setStyleSheet('''
        QWidget#CodeMirrorStatus {
            color: #fff;
            border: 0px;
            background: transparent;
        }
        QLabel {
            color: #fff;
            border: 0px;
            background: transparent;
        }''')
    def initBtn(self, icon=None, text=None):
        btn = QToolButton(self)
        if icon: 
            icon = os.path.join("widget/codemirror", icon)
            btn.setIcon(FigD.Icon(icon))
        if text: btn.setText(text)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setStyleSheet("background: #292929; color: #fff;")

        return btn


class CodeMirrorMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 themes: Dict[str, str]={}, 
                 modes: Dict[str, str]={}, 
                 webview: Union[str, QWebEngineView]=None):
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
        self.modeDropdown = CodeMirrorModeDropdown(modes=modes, webview=webview)
        self.themeDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.formatBtn)
        self.layout.addWidget(self.themeDropdown)
        self.layout.addWidget(self.modeDropdown)
        self.layout.addWidget(self.debugBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class CodeMirrorEditor(QWidget):
    '''codemirror code editor.'''
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.45):
        super(CodeMirrorEditor, self).__init__(parent)
        from fig_dash.ui.widget.codemirror.mode import CMMimeTypeToLang
        from fig_dash.ui.widget.codemirror.theme import CMTheme

        self.zoom_factor = zoom_factor
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.mimetype_to_lang = CMMimeTypeToLang
        self.webview = QWebEngineView()
        self.webview.setHtml("CM Editor not loaded")
        self.modes = CMMimeTypeToLang
        self.menubar = CodeMirrorMenu(
            themes=CMTheme, 
            modes=self.modes, 
            webview=self.webview
        )
        self.statusbar = CodeMirrorStatus(self.webview)
        self.statusbar.setMaximumHeight(30)
        self.themes = CMTheme
        self.layout.addWidget(self.menubar)
        self.menubar.setMaximumHeight(30)
        self.layout.addWidget(self.webview)
        self.layout.addWidget(self.statusbar)
        # self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setObjectName("CMEditor")
        self.setStyleSheet(code_mirror_style)
        self.webview.urlChanged.connect(self.onUrlChange)
        # self.webview.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    def onUrlChange(self):
        self.webview.setZoomFactor(self.zoom_factor)
    
    def setZoomFactor(self, zoom_factor: float=1):
        self.zoom_factor = zoom_factor

    def buildEditor(self, **args):
        from fig_dash.ui.widget.codemirror.js import QWebChannelJS
        from fig_dash.ui.widget.codemirror.html import CMHtml
        from fig_dash.ui.widget.codemirror.lib.codemirror import CMCodeMirrorCSS, CMCodeMirrorJS
        # editor keymaps
        from fig_dash.ui.widget.codemirror.keymap.sublime import CMSublimeJS
        # comment addon.
        from fig_dash.ui.widget.codemirror.addon.comment.comment import CMCommentJS
        from fig_dash.ui.widget.codemirror.addon.comment.continuecomment import CMContinueCommentJS
        # dialog addon.
        from fig_dash.ui.widget.codemirror.addon.dialog.dialog import CMDialogCSS, CMDialogJS
        # display addon.
        from fig_dash.ui.widget.codemirror.addon.display.autorefresh import CMAutoRefreshJS
        from fig_dash.ui.widget.codemirror.addon.display.fullscreen import CMFullscreenJS, CMFullscreenCSS
        from fig_dash.ui.widget.codemirror.addon.display.panel import CMPanelJS
        from fig_dash.ui.widget.codemirror.addon.display.placeholder import CMPlaceholderJS
        from fig_dash.ui.widget.codemirror.addon.display.ruler import CMRulerJS
        # edit addon.
        from fig_dash.ui.widget.codemirror.addon.edit.closebrackets import CMCloseBracketJS
        from fig_dash.ui.widget.codemirror.addon.edit.closetag import CMCloseTagJS
        from fig_dash.ui.widget.codemirror.addon.edit.continuelist import CMContinueListJS
        from fig_dash.ui.widget.codemirror.addon.edit.matchbrackets import CMMatchBracketsJS
        from fig_dash.ui.widget.codemirror.addon.edit.matchtags import CMMatchTagsJS
        from fig_dash.ui.widget.codemirror.addon.edit.trailingspace import CMTrailingSpaceJS
        # fold addon: for codefolding.
        from fig_dash.ui.widget.codemirror.addon.fold.brace_fold import CMBraceFoldJS
        from fig_dash.ui.widget.codemirror.addon.fold.comment_fold import CMCommentFoldJS
        from fig_dash.ui.widget.codemirror.addon.fold.foldcode import CMFoldCodeJS
        from fig_dash.ui.widget.codemirror.addon.fold.foldgutter import CMFoldGutterJS, CMFoldGutterCSS
        from fig_dash.ui.widget.codemirror.addon.fold.indent_fold import CMIndentFoldJS
        from fig_dash.ui.widget.codemirror.addon.fold.markdown_fold import CMMarkdownJS
        from fig_dash.ui.widget.codemirror.addon.fold.xml_fold import CMXMLFoldJS
        # wrap addon.
        from fig_dash.ui.widget.codemirror.addon.wrap.hardwrap import CMHardwrapJS
        # default mode is python.
        from fig_dash.ui.widget.codemirror.mode.python import PYTHONJS
        # self.keymap = {}
        self.addon = {
            "COMMENT_JS": CMCommentJS,
            "CONTINUECOMMENT_JS": CMContinueCommentJS,
            "DIALOG_CSS": CMDialogCSS,
            "DIALOG_JS": CMDialogJS,
            "AUTOREFRESH_JS": CMAutoRefreshJS,
            "FULLSCREEN_JS": CMFullscreenJS,
            "FULLSCREEN_CSS": CMFullscreenCSS,
            "PANEL_JS": CMPanelJS,
            "PLACEHOLDER_JS": CMPlaceholderJS,
            "RULER_JS": CMRulerJS,
            "KEYMAP_JS": CMSublimeJS,
            "HARDWRAP_JS": CMHardwrapJS,
            "THEMES_CSS": "\n".join(self.themes.values()),
            "DEFAULT_MODE_JS": PYTHONJS,
            "CLOSEBRACKETS_JS": CMCloseBracketJS,
            "CLOSETAG_JS": CMCloseTagJS,
            "CONTINUELIST_JS": CMContinueListJS,
            "MATCHBRACKETS_JS": CMMatchBracketsJS,
            "MATCHTAGS_JS": CMMatchTagsJS,
            "TRAILINGSPACE_JS": CMTrailingSpaceJS,
            "BRACE_FOLD_JS": CMBraceFoldJS,
            "COMMENT_FOLD_JS":CMCommentFoldJS,
            "FOLDCODE_JS": CMFoldCodeJS,
            "FOLDGUTTER_JS": CMFoldGutterJS,
            "FOLDGUTTER_CSS": CMFoldGutterCSS,
            "INDENT_FOLD_JS": CMIndentFoldJS,
            "MARKDOWN_FOLD_JS": CMMarkdownJS,
            "XML_FOLD_JS": CMXMLFoldJS,
        }
        # self.mode = {}
        self.lib = {
            "CODEMIRROR_JS": CMCodeMirrorJS,
            "CODEMIRROR_CSS": CMCodeMirrorCSS,
        }
        params = {
            "TITLE": args.get("TITLE", "CodeMirror for Qt"),
            "LANG_MODE": "text/x-python",
            "QWEBCHANNEL_JS": QWebChannelJS
        }
        params.update(args)
        params.update(self.lib)
        params.update(self.addon)
        self.editor_html = CMHtml.render(params)
        self.webview.setHtml(self.editor_html)

    def saveEditor(self, path: str):
        with open(path, "w") as f:
            f.write(self.editor_html)

    def setMode(self, mimetype: str="text"):
        lang = self.mimetype_to_lang[mimetype]
        exec(f"from fig_dash.ui.widget.codemirror.mode.{lang} import {lang.upper()}JS")

    def setTheme(self, theme: str=""):
        pass
        # self.webview.page().runJavaScript()


def test_code_mirror():
    import sys
    import time
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    cm = CodeMirrorEditor()
    cm.show()
    s = time.time()
    cm.buildEditor()
    print(f"built code-mirror editor in {time.time()-s}s")
    cm.saveEditor("cm-editor.html")
    app.exec()


if __name__ == "__main__":
    test_code_mirror()