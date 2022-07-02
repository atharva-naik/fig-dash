#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
# set QT DEBUGGING PORT.
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '0.0.0.0:5000'
import sys
import jinja2
from typing import *
# Qt imports.
from PyQt5.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QComboBox, QSizePolicy
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.webview import DebugWebView
from fig_dash.ui import FigDAppContainer, wrapFigDWindow, styleContextMenu, DashWidgetGroup
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap, FigDSystemAppIconMap

def blank(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)
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
        self.setCurrentIndex(21)
        # self.setFixedWidth(300)
    def changeTheme(self, i):
        theme = self.themes[i]
        code = f'''selectThemeByIndex({i})'''
        self.webview.page().runJavaScript(code)
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
        version_info = sys.version
        self.py_version_text = "Python "+version_info.split("\n")[0].split()[0].strip()
        self.gcc_version_text = version_info.split("\n")[1].strip()[1:-1]
        self.py_version = self.initBtn(
            icon="python.png",
            text=" "+self.py_version_text
        )
        self.gcc_version = self.initBtn(
            icon="c.png",
            text=" "+self.gcc_version_text
        )
        # add widgets.
        self.layout.addStretch(1)
        self.layout.addWidget(self.py_version)
        self.layout.addWidget(self.gcc_version)
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
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QLabel {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
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
        btn.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QToolButton:hover {
            border: 0px;
            background: rgba(0, 0, 0, 0.5);
        }''')

        return btn


class CodeMirrorViewToolbar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 themes: Dict[str, str]={}, 
                 webview: Union[str, QWebEngineView]=None):
        super(CodeMirrorViewToolbar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = webview
        self.formatBtn = CodeMirrorBtn(
            self, icon="format_code.svg", size=(27,27),
            tip="format code according to language specification (if formatter is available)"
        )
        self.wordWrapBtn = CodeMirrorBtn(
            self, icon="word_wrap.svg",
            tip="wrap lines"
        )
        self.diffBtn = CodeMirrorBtn(
            self, icon="diff.svg",
            tip="toggle differences"
        )
        self.diffBtn.clicked.connect(self.toggleDifferences)
        self.themeDropdown = CodeMirrorThemeDropdown(themes=themes, webview=webview)
        self.themeDropdown.setStyleSheet("background: #292929; color: #eb5f34; font-size: 15px;")
        self.themeDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.themeDropdown)
        self.layout.addWidget(self.formatBtn)
        self.layout.addWidget(self.wordWrapBtn)
        self.layout.addWidget(self.diffBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def toggleDifferences(self):
        self.webview.page().runJavaScript("toggleDifferences()")


class CodeMirrorCodeToolbar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 modes: Dict[str, str]={}, 
                 webview: Union[str, QWebEngineView]=None):
        super(CodeMirrorCodeToolbar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = webview
        self.debugBtn = CodeMirrorBtn(
            self, icon="debug.svg",
            tip="debug code"
        )
        self.modeDropdown = CodeMirrorModeDropdown(modes=modes, webview=webview)
        self.modeDropdown.setStyleSheet("background: #292929; color: #eb5f34; font-size: 15px;")
        self.modeDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.webview.devToolsBtn)
        self.layout.addWidget(self.modeDropdown)
        self.layout.addWidget(self.debugBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def toggleDifferences(self):
        self.webview.page().runJavaScript("toggleDifferences()")


class CodeMirrorMenu(DashWidgetGroup):
    def __init__(self, webview, parent: Union[QWidget, None]=None):
        from fig_dash.ui.widget.codemirror.theme import CMTheme
        from fig_dash.ui.widget.codemirror.mode import CMMimeTypeToLang

        self.modes = CMMimeTypeToLang
        super(CodeMirrorMenu, self).__init__(parent=parent, name="View")
        self.viewtoolbar = CodeMirrorViewToolbar(
            themes=CMTheme, 
            webview=webview
        )
        self.codetoolbar = CodeMirrorCodeToolbar(
            modes=self.modes, 
            webview=webview
        )
        self.viewtoolbar.setMaximumHeight(30)
        self.codetoolbar.setMaximumHeight(30)
        self.addWidget(self.viewtoolbar)
        self.addWidget(self.codetoolbar)

    def toggle(self):
        if self.isVisible(): 
            self.hide()
        else: self.show()


class CodeMirrorWebView(DebugWebView):
    def __init__(self, *args, accent_color: str="red", **kwargs):
        super(CodeMirrorWebView, self).__init__(*args, **kwargs)
        self.accent_color = accent_color
        self.action_shortcut_map = {
            "Undo": QKeySequence.Undo,
            "Redo": QKeySequence("Ctrl+Y"),
            "Cut": QKeySequence.Cut,
            "Copy": QKeySequence.Copy,
            "Paste": QKeySequence.Paste,
            "Select all": QKeySequence.SelectAll,
            "Inspect": QKeySequence("Ctrl+Shift+I"),
        }
        self.action_icon_map = {
            "Undo": "widget/spreadsheet/undo.svg",
            "Redo": "widget/spreadsheet/redo.svg",
            "Cut": "browser/cut.svg",
            "Copy": "browser/copy.svg",
            "Paste": "browser/paste.svg",
            "Select all": "browser/select_all.png",
            "Inspect": "titlebar/dev_tools.svg",
        }

    def contextMenuEvent(self, event):
        self.contextMenu = self.page().createStandardContextMenu()
        for action in self.contextMenu.actions():
            shortcut_keyseq = self.action_shortcut_map.get(action.text())
            action_icon = self.action_icon_map.get(action.text())
            if shortcut_keyseq:
                action.setShortcut(shortcut_keyseq)
            if action_icon:
                action.setIcon(FigD.Icon(action_icon))
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu.popup(event.globalPos())


class CodeMirrorEditor(QWidget):
    '''codemirror code editor.'''
    def __init__(self, parent: Union[None, QWidget]=None,
                 zoom_factor: float=1.35, accent_color="red"):
        super(CodeMirrorEditor, self).__init__(parent)
        from fig_dash.ui.widget.codemirror.theme import CMTheme
        from fig_dash.ui.widget.codemirror.mode import CMMimeTypeToLang

        self.zoom_factor = zoom_factor
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.mimetype_to_lang = CMMimeTypeToLang
        self.webview = CodeMirrorWebView(accent_color=accent_color)
        self.webview.setHtml("CM Editor not loaded")
        self.modes = CMMimeTypeToLang
        self.statusbar = CodeMirrorStatus(self.webview)
        self.statusbar.setMaximumHeight(30)
        self.themes = CMTheme
        self.menu = CodeMirrorMenu(webview=self.webview)
        self.menu.setFixedHeight(120)
        self.menu.hide()
        # view and codet toolbars.
        self.codetoolbar = self.menu.codetoolbar
        self.viewtoolbar = self.menu.viewtoolbar
        # self.layout.addWidget(self.viewtoolbar)
        # self.layout.addWidget(self.codetoolbar)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.webview.splitter)
        self.layout.addWidget(self.statusbar)
        # self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setObjectName("CMEditor")
        self.setStyleSheet(code_mirror_style)
        self.webview.urlChanged.connect(self.onUrlChange)
        # self.webview.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    def onUrlChange(self):
        self.webview.setZoomFactor(self.zoom_factor)
        self.webview.loadFinished.connect(self.webview.loadDevTools)
    
    def setZoomFactor(self, zoom_factor: float=1):
        self.zoom_factor = zoom_factor

    def buildEditor(self, **args):
        from fig_dash.ui.widget.codemirror.js import QWebChannelJS
        from fig_dash.ui.widget.codemirror.html import CMHtml, CMMergeHtml
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
        # hint addon.
        from fig_dash.ui.widget.codemirror.addon.hint.anyword_hint import CMAnywordHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.css_hint import CMCSSHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.html_hint import CMHTMLHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.javascript_hint import CMJavascriptHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.show_hint import CMShowHintCSS, CMShowHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.sql_hint import CMSQLHintJS
        from fig_dash.ui.widget.codemirror.addon.hint.xml_hint import CMXMLHintJS
        # lint addon.
        from fig_dash.ui.widget.codemirror.addon.lint.lint import CMLintJS, CMLintCSS
        from fig_dash.ui.widget.codemirror.addon.lint.json_lint import CMJSONLintJS
        from fig_dash.ui.widget.codemirror.addon.lint.css_lint import CMCSSLintJS
        from fig_dash.ui.widget.codemirror.addon.lint.html_lint import CMHTMLLintJS
        from fig_dash.ui.widget.codemirror.addon.lint.javascript_lint import CMJavascriptLintJS
        from fig_dash.ui.widget.codemirror.addon.lint.yaml_lint import CMYAMLLintJS
        from fig_dash.ui.widget.codemirror.addon.lint.coffeescript_lint import CMCoffeescriptLintJS
        # merge addon.
        from fig_dash.ui.widget.codemirror.addon.merge.merge import CMMergeJS, CMMergeCSS
        from fig_dash.ui.widget.codemirror.addon.merge.ui_funcs import CMMergeUIFuncs
        from fig_dash.ui.widget.codemirror.addon.merge.diff_match_patch import GoogleDiffMatchPatchJS
        # wrap addon.
        from fig_dash.ui.widget.codemirror.addon.wrap.hardwrap import CMHardwrapJS
        # default mode is python.
        from fig_dash.ui.widget.codemirror.mode.python import PYTHONJS
        # self.keymap = {}
        merge_mode = args.get('merge_mode', False)
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
            "ANYWORD_HINT_JS": CMAnywordHintJS,
            "CSS_HINT_JS": CMCSSHintJS,
            "HTML_HINT_JS": CMHTMLHintJS,
            "JAVASCRIPT_HINT_JS": CMJavascriptHintJS,
            "SHOW_HINT_CSS": CMShowHintCSS,
            "SHOW_HINT_JS": CMShowHintJS,
            "SQL_HINT_JS": CMSQLHintJS,
            "XML_HINT_JS": CMXMLHintJS,
            "COFFEESCRIPT_LINT_JS": CMCoffeescriptLintJS,
            "CSS_LINT.JS": CMCSSLintJS,
            "HTML_LINT_JS": CMHTMLLintJS,
            "JAVASCRIPT_LINT_JS": CMJavascriptHintJS,
            "JSON_LINT_JS": CMJSONLintJS,
            "LINT_CSS": CMLintCSS,
            "LINT_JS": CMLintJS,
            "YAML_LINT_JS": CMYAMLLintJS,
            "MERGE_JS": CMMergeJS,
            "MERGE_CSS": CMMergeCSS,
            "MATCH_PATCH_JS": GoogleDiffMatchPatchJS,
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
        params["EDITOR_BACKGROUND_COLOR"] = "#292929"
        if merge_mode:
            params["THEME"] = "gruvbox-dark"
            self.editor_html = CMMergeHtml.render(params)
        else:
            self.editor_html = CMHtml.render(params)
        url = FigD.createTempUrl(self.editor_html)
        self.webview.load(url)
        # print(url)
    def saveEditor(self, path: str):
        with open(path, "w") as f:
            f.write(self.editor_html)

    def setMode(self, mimetype: str="text"):
        lang = self.mimetype_to_lang[mimetype]
        exec(f"from fig_dash.ui.widget.codemirror.mode.{lang} import {lang.upper()}JS")
# def test_code_mirror():
#     import sys
#     import time
#     FigD("/home/atharva/GUI/fig-dash/resources")
#     app = QApplication(sys.argv)
#     cm = CodeMirrorEditor()
#     cm.show()
#     s = time.time()
#     cm.buildEditor(merge_mode=False)
#     print(f"built code-mirror editor in {time.time()-s}s")
#     cm.saveEditor("cm-editor.html")
#     app.exec()
def test_codemirror():
    import sys
    import time
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    # accent color and css grad color.
    icon = FigDSystemAppIconMap["codeeditor"]
    accent_color = FigDAccentColorMap["codeeditor"]
    cm = CodeMirrorEditor(accent_color=accent_color)
    # cm.show()
    window = wrapFigDWindow(cm, title="Code Editor", icon=icon, where="back",
                            accent_color=accent_color, titlebar_callbacks={
                                "autoSave": blank(),
                            })
    window.show()
    s = time.time()
    cm.buildEditor(merge_mode=False)
    print(f"built code-mirror editor in {time.time()-s}s")
    # cm.saveEditor("cm-editor.html")
    app.exec()

def launch_codemirror(app):
    # accent color and css grad color.
    icon = FigDSystemAppIconMap["codeeditor"]
    accent_color = FigDAccentColorMap["codeeditor"]
    cm = CodeMirrorEditor(accent_color=accent_color)
    cm.buildEditor(merge_mode=False)
    window = wrapFigDWindow(cm, title="Code Editor", icon=icon, where="back",
                            accent_color=accent_color, titlebar_callbacks={
                                "autoSave": blank(),
                            })
    window.show()


if __name__ == "__main__":
    test_codemirror()