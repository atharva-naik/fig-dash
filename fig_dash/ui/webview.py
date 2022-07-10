#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::browser")
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
import sys
import jinja2
import socket
import getpass
import pathlib
import argparse
import subprocess
from typing import *
from functools import partial
from requests.exceptions import MissingSchema, InvalidSchema
# Qt5 imports.
from PyQt5.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog
from PyQt5.QtWebEngineCore import QWebEngineFindTextResult
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings, QWebEngineContextMenuData
from PyQt5.QtGui import QColor, QFont, QPalette, QKeySequence, QIcon, QMovie, QPixmap, QGradient, QLinearGradient, QPainterPath, QRegion
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize, QPoint, QPointF, QRectF, QObject, QBuffer, QIODevice
from PyQt5.QtWidgets import QTabBar, QToolBar, QToolButton, QSplitter, QLabel, QMenu, QWidget, QAction, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QTextEdit, QPlainTextEdit, QShortcut, QMessageBox, QFrame
# fig_dash
from fig_dash.assets import FigD
from fig_dash.utils import collapseuser
# from fig_dash.api.browser.extensions import ExtensionManager
from fig_dash.ui import DashWidgetGroup, styleContextMenu, styleTextEditMenuIcons

ON_POSIX = 'posix' in sys.builtin_module_names
WEBPAGE_TERMINAL_JS = '''
var FigWebPageTerminal = document.getElementById("term-output");
class FigWebPageTerminalHandler {
	constructor(name, age) {
    	this.cwd=`'''+collapseuser(os.getcwd())+'''`;
        this.user=`'''+getpass.getuser()+'''`;
        this.hostname=`'''+socket.gethostname()+'''`;
    }
    chdir(cwd) {
        this.cwd = cwd;
    }
    clear() {
        FigWebPageTerminal.innerHTML = `<span style="font-weight: bold; color: #8ae234;">${this.user}@${this.hostname}</span>:<span style="font-weight: bold; color: #729fcf;">${this.cwd}</span> <br>`;
    }
    writeLine(cmd, line) {
        FigWebPageTerminal.innerHTML = FigWebPageTerminal.innerHTML + `<span style="font-weight: bold; color: #8ae234;">${this.user}@${this.hostname}</span>:<span style="font-weight: bold; color: #729fcf;">${this.cwd}</span> ${cmd} <br> ${line} <br>`
    }
    /* writeLs(cmd, lsArray) {
        var line = '';
        for (int i=0; i<lsArray.length, i++) {
            line += '';
        }
        FigWebPageTerminal.innerHTML = FigWebPageTerminal.innerHTML + `<span style="font-weight: bold; color: #8ae234;">${this.user}@${this.hostname}</span>:<span style="font-weight: bold; color: #729fcf;">${this.cwd}</span> ${cmd} <br> ${line} <br>`
    } */
    write(cmd, line) {
        FigWebPageTerminal.innerHTML = FigWebPageTerminal.innerHTML + `<span style="font-weight: bold; color: #8ae234;">${this.user}@${this.hostname}</span>:<span style="font-weight: bold; color: #729fcf;">${this.cwd}</span> ${cmd} <br>`
    }
    writeErrorLine(cmd, line) {
        FigWebPageTerminal.innerHTML = FigWebPageTerminal.innerHTML + `<span style="font-weight: bold; color: #8ae234;">${this.user}@${this.hostname}</span>:<span style="font-weight: bold; color: #729fcf;">${this.cwd}</span> ${cmd} <br> <span style="color: red;">${line}</span> <br>`
    }
}
var FigTerminal = new FigWebPageTerminalHandler()
// welcome user and give guidelines on how to use!
FigTerminal.writeLine("welcome", "Welcome '''+getpass.getuser()+'''!, type a command in the navigation bar to execute quick terminal commands");
'''
WEBPAGE_ANNOT_JS = '''
function getSafeRanges(dangerous) {
    var a = dangerous.commonAncestorContainer;
    // Starts -- Work inward from the start, selecting the largest safe range
    var s = new Array(0), rs = new Array(0);
    if (dangerous.startContainer != a)
        for(var i = dangerous.startContainer; i != a; i = i.parentNode)
            s.push(i)
    ;
    if (0 < s.length) for(var i = 0; i < s.length; i++) {
        var xs = document.createRange();
        if (i) {
            xs.setStartAfter(s[i-1]);
            xs.setEndAfter(s[i].lastChild);
        }
        else {
            xs.setStart(s[i], dangerous.startOffset);
            xs.setEndAfter(
                (s[i].nodeType == Node.TEXT_NODE)
                ? s[i] : s[i].lastChild
            );
        }
        rs.push(xs);
    }

    // Ends -- basically the same code reversed
    var e = new Array(0), re = new Array(0);
    if (dangerous.endContainer != a)
        for(var i = dangerous.endContainer; i != a; i = i.parentNode)
            e.push(i)
    ;
    if (0 < e.length) for(var i = 0; i < e.length; i++) {
        var xe = document.createRange();
        if (i) {
            xe.setStartBefore(e[i].firstChild);
            xe.setEndBefore(e[i-1]);
        }
        else {
            xe.setStartBefore(
                (e[i].nodeType == Node.TEXT_NODE)
                ? e[i] : e[i].firstChild
            );
            xe.setEnd(e[i], dangerous.endOffset);
        }
        re.unshift(xe);
    }

    // Middle -- the uncaptured middle
    if ((0 < s.length) && (0 < e.length)) {
        var xm = document.createRange();
        xm.setStartAfter(s[s.length - 1]);
        xm.setEndBefore(e[e.length - 1]);
    }
    else {
        return [dangerous];
    }

    // Concat
    rs.push(xm);
    response = rs.concat(re);    

    // Send to Console
    return response;
}

// add style for annotation_context_menu
const style = document.createElement("style");
style.textContent = `
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro&display=swap');
#fig_webpage_annotation_context_menu {
    color: #fff;
    font-size: 14px;
    font-family: 'Be Vietnam Pro', sans-serif;
    background-color: rgba(29, 29, 29, 0.9);
    backdrop-filter: blur(5px);
}
.fig_webpage_annotation_menu_item {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 4px;
    padding-bottom: 4px;
    margin: 0;
}
.fig_webpage_annotation_menu_item:hover {
    color: #292929;
    background-color: orange;
}`
function figWebAnnotationClear() {
    console.log(selectedWebAnnotation);
    selectedWebAnnotation.outerHTML = selectedWebAnnotation.innerHTML
    // selectedWebAnnotation
}
document.head.appendChild(style);
var selectedWebAnnotation = "";
let annotation_context_menu = document.createElement("div");
annotation_context_menu.id = "fig_webpage_annotation_context_menu";
annotation_context_menu.innerHTML = `
<p class="fig_webpage_annotation_menu_item">Change highlight color</p>
<p class="fig_webpage_annotation_menu_item" onclick="figWebAnnotationClear(this)">Clear highlight</p>
<p class="fig_webpage_annotation_menu_item">Add a note</p>
<p class="fig_webpage_annotation_menu_item" onclick='alert("Thank you!")'>Upvote</p>`;
annotation_context_menu.style.position = "absolute";
annotation_context_menu.style.display = 'none'
document.body.appendChild(annotation_context_menu);
annotation_context_menu.onmouseleave = () => annotation_context_menu.style.display = 'none'

function highlightContextMenu(event) {
    event.preventDefault();
    annotation_context_menu.style.top = `${event.pageY+10}px`;
    annotation_context_menu.style.left = `${event.pageX+10}px`;
    console.log(event.pageY, event.pageX);
    annotation_context_menu.style.display = '';
    selectedWebAnnotation = event.path[0];
}

function highlightRange(range) {
    var newNode = document.createElement("div");
    newNode.classList.add("fig_webpage_annotation");
    newNode.setAttribute(
       "style",
       "background-color: yellow; display: inline;"
    );
    range.surroundContents(newNode);
}

function highlightSelection() {
    var userSelection = window.getSelection().getRangeAt(0);
    var safeRanges = getSafeRanges(userSelection);
    for (var i = 0; i < safeRanges.length; i++) {
        highlightRange(safeRanges[i]);
    }
    document.querySelectorAll('.fig_webpage_annotation').forEach(item => {
        item.addEventListener('contextmenu', highlightContextMenu);
    })
}
'''
contextMenuHtml = '''
<menu type="context" id="highlightMenu">
	<menuitem label="Refresh Post" onclick="window.location.reload();" icon="/images/refresh-icon.png"></menuitem>
	<menuitem label="Skip to Comments" onclick="window.location='#comments';" icon="/images/comment_icon.gif"></menuitem>
	<menu label="Share on..." icon="/images/share_icon.gif">
		<menuitem label="Twitter" icon="/images/twitter_icon.gif" onclick="goTo('//twitter.com/intent/tweet?text=' + document.title + ':  ' + window.location.href);"></menuitem>
		<menuitem label="Facebook" icon="/images/facebook_icon16x16.gif" onclick="goTo('//facebook.com/sharer/sharer.php?u=' + window.location.href);"></menuitem>
	</menu>
</menu>'''
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-features=-webengine-proprietary-codecs --blink-settings=darkMode=4,darkModeImagePolicy=2"
os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = FigD.locale("qtwebengine_dictionaries")
# "--blink-settings=darkMode=4,darkModeImagePolicy=2"
# HOME_URL = "file:///tmp/fig_dash.rendered.content.html"

TermViewerJS = """  """
TermViewerCSS = r"""
body {
    color: #fff;
    background: #000;
    font-family: 'Monospace';
}
"""
TermViewerHtml = jinja2.Template(r"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Terminal</title>
        <style>{{ TERM_VIEWER_CSS }}</style>
    </head>
    <body>
        <div id="term-output" class="fig-html-web-terminal"></div>
        <script>{{ TERM_VIEWER_JS }}</script>
    </body>
</html>""")


class TerminalProcessWorker(QObject):
    def run(self):
        pass

class DevToolsBtn(QToolButton): 
    def __init__(self, parent: Union[None, QWidget]=None, 
                size: Tuple[int, int]=(23,23)):
        super(DevToolsBtn, self).__init__(parent)
        self.inactive_icon = "browser/dev_tools.svg"
        self.active_icon = "browser/dev_tools_active.svg"
        self.setIcon(FigD.Icon(self.inactive_icon))
        self.setIconSize(QSize(*size))
        self.setToolTip("open devtools (inspect)")
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 12px;
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(DevToolsBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(DevToolsBtn, self).leaveEvent(event)
# class PyDevToolsBtn(QToolButton):
#     def __init__(self, parent: Union[None, QWidget]=None, 
#                 size: Tuple[int, int]=(23,23)):
#         super(PyDevToolsBtn, self).__init__(parent)
#         self.inactive_icon = "browser/dev_tools.svg"
#         self.active_icon = "browser/dev_tools_active.svg"
#         self.setIcon(FigD.Icon(self.inactive_icon))
#         self.setIconSize(QSize(*size))
#         self.setToolTip("open python devtools")
#         self.setStyleSheet('''
#         QToolButton {
#             border: 0px;
#             background: transparent;
#         }''')
# class PyDevToolsView(QWidget):
#     def __init__(self):
#         super(PyDevToolsView, self).__init__()
#         self.layout = QVBoxLayout()
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         self.layout.setSpacing(0)
        
#         self.execBtn = QToolButton()
#         self.execBtn.setText("run")
#         self.layout.addWidget(self.execBtn)

#         self.input = QPlainTextEdit()
#         self.input.setPlainText("input")
#         self.output = QTextEdit()
#         self.output.setText("output")
#         self.output.setReadOnly(True)
#         # bind events.
#         self.execBtn.clicked.connect(self.exec)
#         # self.input.returnPressed.connect(self.exec)
#         self.outputHistory = []
#         self.layout.addWidget(self.input)
#         self.layout.addWidget(self.output)
#         self.setLayout(self.layout)
#         self.setStyleSheet("""
#         QLineEdit {
#             color: #000;
#             background: #fff;
#         }
#         QTextEdit {
#             color: #000;
#             background: #fff;
#         }""")
#     def exec(self):
#         code = self.input.toPlainText()
#         try:
#             exec(code)
#         except Exception as e:
#             print("\x1b[31;1mbrowser.exec\x1b[0m", e)
#             self.output.setText(str(e))
class BrowserViewGroup(DashWidgetGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(BrowserViewGroup, self).__init__(parent, "View")
        self.wordCountBtn = self.initBtn(
            icon="browser/word_count.svg", 
            tip="toggle visibility of word count, time to read display",
        )
        self.layout.addStretch(1)
        self.layout.addWidget(self.wordCountBtn)
        self.layout.addStretch(1) 

    def connectWindow(self, window):
        self.dash_window = window
        # self.tabs = self.dash_window.tabs
        self.wordCountBtn.clicked.connect(
            self.dash_window.page_info.toggle
        )

# browser menu.
class BrowserMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(BrowserMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # create groups.
        self.viewgroup = BrowserViewGroup()
        # create layout.
        self.layout.addWidget(self.viewgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addStretch(1)
        # set layout.
        self.setLayout(self.layout)

    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #292929''')
        sep.setLineWidth(2)
        sep.setMaximumHeight(100)

        return sep

    def connectWindow(self, widget):
        self.viewgroup.connectWindow(widget)


class BrowserSearchPanelBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(BrowserSearchPanelBtn, self).__init__(parent)
        icon = args.get('icon')
        if icon:
            self.inactive_icon = os.path.join(
                "browser", icon
            )
            stem, ext = os.path.splitext(icon)
            self.active_icon = os.path.join(
                "browser", 
                stem+"_active"+ext
            )
            self.setIcon(
                FigD.Icon(self.inactive_icon)
            )
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(BrowserSearchPanelBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(BrowserSearchPanelBtn, self).leaveEvent(event)


class BrowserSearchPanel(QWidget):
    searched = pyqtSignal(str, QWebEnginePage.FindFlag)
    def __init__(self, parent: Union[None, QWidget]=None):
        super(BrowserSearchPanel, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.query = ""
        self.entry = QLineEdit()
        self.label = QLabel("0/0")
        self.entry.setStyleSheet("background: #fff; color: #000;")
        self.entry.setMinimumWidth(320)
        self.closeBtn = BrowserSearchPanelBtn(
            icon="close.svg", size=(20,20),
            tip="close page search",
        )
        self.prevBtn = BrowserSearchPanelBtn(
            icon="prev.svg", size=(20,20),
            tip="go to previous match (Shift+Enter)",
        )# #eb5f34
        self.nextBtn = BrowserSearchPanelBtn(
            icon="next.svg", size=(20,20),
            tip="go to next match (Enter)",
        )
        self.findInSelectionBtn = BrowserSearchPanelBtn(
            icon="find_in_selection.png", size=(20,20),
            tip="find matches in selection",
        )
        self.entry.setClearButtonEnabled(True)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.layout.addWidget(self.prevBtn)
        self.layout.addWidget(self.nextBtn)
        self.layout.addWidget(self.findInSelectionBtn)
        self.layout.addWidget(self.closeBtn)
        self.nextBtn.clicked.connect(self.update_searching)
        self.prevBtn.clicked.connect(lambda: self.update_searching(QWebEnginePage.FindBackward))
        self.closeBtn.clicked.connect(self.closePanel)
        self.label.setStyleSheet("""
        QLabel {
            color: #6e6e6e;
            background: transparent;
        }""")
        wrapper = QWidget()
        wrapper.setObjectName("Wrapper")
        wrapper.setLayout(self.layout)
        wrapper.setStyleSheet("""
        QWidget#Wrapper {
            color: #fff;
            border: 0px;
            border-radius: 10px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }""")
        self.entry.setStyleSheet("""
        QLineEdit {
            color: #fff;
            font-size: 18px;
            border-radius: 0px;
            border: 1px solid rgba(235, 95, 52, 0.5);
            padding-top: 10px;
            padding-bottom: 10px;
            background-color: transparent;
        }""")
        self.caseAction = QAction()
        self.matchWholeAction = QAction()
        self.regexAction = QAction()

        self.caseAction.setIcon(
            FigD.Icon("browser/case.svg")
        )
        self.matchWholeAction.setIcon(
            FigD.Icon("browser/match_whole.svg")
        )
        self.regexAction.setIcon(
            FigD.Icon("browser/regex.svg")
        )
        
        self.entry.addAction(
            self.caseAction, 
            self.entry.TrailingPosition
        )
        self.entry.addAction(
            self.matchWholeAction, 
            self.entry.TrailingPosition
        )
        self.entry.addAction(
            self.regexAction, 
            self.entry.TrailingPosition
        )
        self.entry.returnPressed.connect(self.search)
        self.entry.textChanged.connect(self.search)
        self.setFocusProxy(self.entry)
        # # Qt compatible flag object.
        # self.flags = QWebEnginePage.FindFlags()
        # python boolean flags.
        self.isCaseSensitive = False
        # connect slots to signals.
        self.nextBtn.clicked.connect(self.nextResult)
        self.prevBtn.clicked.connect(self.prevResult)
        self.caseAction.triggered.connect(
            self.toggleCaseFlag
        )

        tip = "search in webpage"
        self.setToolTip(tip)
        self.setStatusTip(tip)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0,0)
        shadow.setColor(QColor(0, 0, 0))
        # shadow.setColor(QColor(235, 95, 52, 255))
        wrapper.setFixedHeight(60)
        wrapper.setFixedWidth(500)
        wrapper.setGraphicsEffect(shadow)

        dummy = QVBoxLayout()
        dummy.setContentsMargins(0, 0, 0, 0)
        dummy.addWidget(wrapper)
        self.setLayout(dummy)
        
    def toggleCaseFlag(self):
        # print("toggling case flag")
        self.isCaseSensitive = not(self.isCaseSensitive)
        if self.isCaseSensitive:
            self.caseAction.setIcon(
                FigD.Icon("browser/case_active.svg")
            )
        else:
            self.caseAction.setIcon(
                FigD.Icon("browser/case.svg")
            )

    def updateMatches(self, findTextResult: QWebEngineFindTextResult):
        match_idx = findTextResult.activeMatch()
        tot_matches = findTextResult.numberOfMatches()
        self.label.setText(f"{match_idx}/{tot_matches}")

    def showEvent(self, event):
        super(BrowserSearchPanel, self).showEvent(event)
        self.setFocus(True)

    def update_searching(self, direction=QWebEnginePage.FindFlag()):
        flag = direction
        # if self.case_button.isChecked():
            # flag |= QWebEnginePage.FindCaseSensitively
        self.searched.emit(self.entry.text(), flag)

    def show(self):
        super(BrowserSearchPanel, self).show()
        # print(f"\x1b[31;1mshowing: currently {self.isVisible()}\x1b[0m")
    def hide(self):
        super(BrowserSearchPanel, self).hide()
        # print(f"\x1b[31;1mhiding: currently {self.isVisible()}\x1b[0m")
    def closePanel(self):
        self.entry.clear()
        self.search("")
        self.hide()

    def callback(self, has_match: str):
        pass
        # print("has_match:", has_match)
    def search(self, query=None):
        if query is None:
            query = self.entry.text()
        self.query = query
        if self.isCaseSensitive:
            self.browser.findText(query, resultCallback=self.callback, 
                                  options=QWebEnginePage.FindCaseSensitively)
        else:
            self.browser.findText(query, resultCallback=self.callback,
                                  options=QWebEnginePage.FindFlags())

    def nextResult(self):
        if self.isCaseSensitive:
            self.browser.findText(self.query, options=QWebEnginePage.FindCaseSensitively)
        else: 
            self.browser.findText(self.query)

    def prevResult(self):
        if self.isCaseSensitive:
            self.browser.findText(self.query, options=QWebEnginePage.FindBackward | QWebEnginePage.FindCaseSensitively)
        else:
            self.browser.findText(self.query, options=QWebEnginePage.FindBackward)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + self.x(), self.y() + self.y())
        self.oldPos = event.globalPos()

    def connectBrowser(self, browser):
        self.browser = browser

    def setPos(self):
        WB = self.browser.width()
        self.move(WB/2-250, -200)

    def show(self):
        self.setParent(self.browser)
        self.setPos()
        super(BrowserSearchPanel, self).show()


class SilentWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, *args, **kwargs):
        pass
# def findTextResultCallback(result):
#     print(f"{result.activeMatch()}/{result.numberOfMatches()}")
class CustomWebPage(QWebEnginePage):
    def __init__(self, *args, logging_level=0, 
                 dash_window=None, search_panel=None, 
                 **kwargs) -> None:
        super(CustomWebPage, self).__init__(*args, **kwargs)
        from fig_dash.api.system.translate import DashTranslator
        if search_panel is not None:
            self.search_panel = search_panel
            self.findTextFinished.connect(
                self.search_panel.updateMatches
            )
        self.consoleLoggingLevel = logging_level
        self.translator = DashTranslator()
        self.dash_window = dash_window
        self.featurePermissionRequested.connect(self.permissionDialog)
        self.scrollPositionChanged.connect(self.updateScrollPos)
    # def connectWindow(self, window: QWidget) -> None:
    #     self.dash_window = window
    #     print(f"\x1b[32;1mconnectWindow:\x1b[0m connected {window} to {self}")
    def updateScrollPos(self):
        scrollPos = self.scrollPosition()
        x = scrollPos.x()
        y = scrollPos.y()
        try:
            menu = self.dash_window.menu
            menu.browser_statusbar.updateScrollPos(x, y)
        except Exception as e: 
            # it will be noisy for FileViewerWidget.
            pass
    # def createWindow(self, windowType: QWebEnginePage.WebWindowType):
    #     if windowType == QWebEnginePage.WebBrowserTab:
    #         if self.dash_window:
    #             return self.dash_window.tabs.openUrl("https://google.com")
    #         else: return None
    #     elif windowType == QWebEnginePage.WebBrowserWindow:
    #         app = QApplication.instance()
    #         try:
    #             window = app.newMainWindow()
    #             return window.tabs.openTab()
    #         except Exception as e:
    #             print(e)
    #             return None
    #     else:
    #         # handle this case appropriately.
    #         print(windowType)
    #         return None
    def createWindow(self, windowType: QWebEnginePage.WebWindowType):
        page: Union[QWebEnginePage, None] = None
        window = QApplication.instance().activeWindow()
        if windowType == QWebEnginePage.WebBrowserTab:
            print("\x1b[32;1mopening link in new tab\x1b[0m")
            if hasattr(window, "tabs"):
                page = window.tabs.openTab()
        elif windowType == QWebEnginePage.WebBrowserWindow:
            print("\x1b[32;1mopening link in new window\x1b[0m")
            if hasattr(window, "tabs"):
                figd_window = window.tabs.openWindow()
                if hasattr(figd_window, "webview"):
                    page = figd_window.webview.page()
                elif hasattr(figd_window, "browser"):
                    page = figd_window.browser.page()

        return page
            
    def permissionDialog(self, securityOrigin: QUrl, feature: QWebEnginePage.Feature):
        print(f"{securityOrigin.toString()}: opening permission dialog for {feature}")
        """
        QWebEnginePage::PermissionUnknown	0	It is unknown whether the user grants or denies permission.
        QWebEnginePage::PermissionGrantedByUser	1	The user has granted permission.
        QWebEnginePage::PermissionDeniedByUser	2	The user has denied permission.
        """
        self.setFeaturePermission(
            securityOrigin, feature, 
            QWebEnginePage.PermissionGrantedByUser
        )

    def translate(self, target_lang="en"):
        self.target_lang = target_lang
        self.runJavaScript("document.getElementsByTagName('p')", self.translate_p)

    def translate_p(self, p_texts: List[str]) -> None:
        """[summary]
        get the list of strings.

        Args:
            p_texts (List[str]): [description]
        """
        print(p_texts)
        new_texts = []
        for p_text in p_texts:
            new_texts.append(p_text)
            self.translator(p_text, self.target_lang)
        print(new_texts)

    def javaScriptConsoleMessage(self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, 
                                 message: str, lineNumber: int, sourceID: str) -> None:
        """[summary]

        Args:
            level (QWebEnginePage.JavaScriptConsoleMessageLevel): [description] Level indicates the severity of the event that triggered the message
            
            QWebEnginePage::InfoMessageLevel (0) The message is purely informative and can safely be ignored.
            
            QWebEnginePage::WarningMessageLevel	(1)	The message informs about unexpected behavior or errors that may need attention.
            
            QWebEnginePage::ErrorMessageLevel (2) The message indicates there has been an error.
            message (str): [description] the string message
            lineNumber (int): [description] In case of evaluation errors the source URL may be provided in sourceID as well as the lineNumber.
            sourceID (str): [description] In case of evaluation errors the source URL may be provided in sourceID as well as the lineNumber.
        """
        if level == QWebEnginePage.InfoMessageLevel:
            if level >= self.consoleLoggingLevel:
                print(f"\x1b[34;1mjs:\x1b[0m {lineNumber}: {level} {message}")
        elif level == QWebEnginePage.WarningMessageLevel:
            if level >= self.consoleLoggingLevel:
                print(f"\x1b[33;1mjs:\x1b[0m {lineNumber}: {level} {message}")
        elif level == QWebEnginePage.ErrorMessageLevel:
            if level >= self.consoleLoggingLevel:
                print(f"\x1b[31;1mjs:\x1b[0m {lineNumber}: {level} {message}")
    
    def acceptNavigationRequest(self, url: QUrl, navType: int, isMainFrame: bool):
        """[summary]
        modified method to change reaction to url being clicked.

        Args:
            url (QUrl): [description]
            navType (int): [description]
            isMainFrame (bool): [description]

        Returns:
            [type]: [description]
        """
        # print(f"\x1b[32;1m{navType == QWebEnginePage.NavigationTypeLinkClicked}\x1b[0m: {url}")
        # if navType == QWebEnginePage.NavigationTypeLinkClicked:
        #     print(url.toString())
        # self.dash_window.statusBar().showMessage(url.toString())
        return super(CustomWebPage, self).acceptNavigationRequest(
            url, navType, isMainFrame
        )


class DevToolbarBtn(QToolButton):
    def __init__(self, icon, type="svg", 
                 size=(30,30), tip="a tip") -> None:
        super(DevToolbarBtn, self).__init__()
        self.inactive_icon = FigD.Icon(f"browser/{icon}.{type}") 
        self.active_icon = FigD.Icon(f"browser/{icon}_active.{type}")
        self.setIcon(self.inactive_icon)
        self.setIconSize(QSize(*size))
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            background: transparent;
        }""")
        self.setToolTip(tip)
        self.setStatusTip(tip)

    def __str__(self):
        return "\x1b[34mui::browser::DevToolbarBtn\x1b[0m"

    def enterEvent(self, event):
        self.setIcon(self.active_icon)
        super(DevToolbarBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.inactive_icon)
        super(DevToolbarBtn, self).leaveEvent(event)

# zoom factor object.
class ZoomFactor:
    '''browser zoom factor'''
    def __init__(self, zoom_factor):
        if zoom_factor > 5:
            zoom_factor /= 100
        zoom_factor = max(min(zoom_factor, 5), 0.25)
        self.value = zoom_factor

    def __str__(self):
        return f"zoom: {self.value}"

    def __repr__(self):
        return f"zoom: {self.value}"

    def __eq__(self, other):
        return self.value == other.value 

    def __lt__(self, other):
        return self.value < other.value 

    def __gt__(self, other):
        return self.value > other.value 

    def gt(self, zoom_factors):
        for value in zoom_factors:
            # print(f"{value.value} > {self.value}: {value > self}")
            if value > self: 
                return value
        return value

    def lt(self, zoom_factors):
        for value in zoom_factors:
            if value.value < self.value: 
                return value
        return value

    def set(self, value):
        self.value = value

    def __call__(self):
        return self.value
# class DebugWebView(QWebEngineView):
#     zoomChanged = pyqtSignal(float)
#     backgroundChanged = pyqtSignal(int, int, int)
#     def __init__(self, parent: Union[QWidget, None]=None, zoomFactor: float=1.25, 
#                  dev_tools_zoom: float=1.35, accent_color: str="green"):
#         super(DebugWebView, self).__init__(parent)
#         self.accent_color = accent_color
#         self.devTools = self.initDevTools()
#         self.devCloseBtn.clicked.connect(self.devTools.hide)
#         self.devToolsBtn = DevToolsBtn(self)    
#         self.dev_tools_zoom = dev_tools_zoom
#         self.devToolsBtn.clicked.connect(self.toggleDevTools)
#         # current zoom factor of the main web view.
#         self.currentZoomFactor = zoomFactor
#         zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
#         self.zoomFactors = [ZoomFactor(zf) for zf in zoomFactors]

#         self.splitter = QSplitter(Qt.Horizontal)
#         self.splitter.addWidget(self)
#         self.splitter.addWidget(self.devTools)
#         # self.splitter.addWidget(self.py_dev_view)
#         self.splitter.setSizes([500, 300])
#         # back reference to browser.
#         self.splitter.browser = self
#         self._page_background_colors = []

#         self.searchPanel = BrowserSearchPanel()
#         self.searchPanel.connectBrowser(self)
#         self.searchPanel.move(50,50)

#         custom_page = CustomWebPage(
#             self, logging_level=3, 
#             search_panel=self.searchPanel,            
#         )
#         self.setPage(custom_page)
#         # shortcuts.
#         self.Esc = QShortcut(QKeySequence("Esc"), self)
#         self.Esc.activated.connect(self.searchPanel.closePanel)

#         self.CtrlF = QShortcut(QKeySequence("Ctrl+F"), self)
#         self.CtrlF.activated.connect(self.reactToCtrlF)
        
#         self.RefreshShortcut = QShortcut(QKeySequence.Refresh, self)
#         self.RefreshShortcut.activated.connect(self.reload)
        
#         self.ForwardShortcut = QShortcut(QKeySequence.Forward, self)
#         self.ForwardShortcut.activated.connect(self.forward)
        
#         self.BackShortcut = QShortcut(QKeySequence.Back, self)
#         self.BackShortcut.activated.connect(self.back)
        
#         self.CtrlShiftI = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
#         self.CtrlShiftI.activated.connect(self.toggleDevTools)
        
#         self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
#         self.CtrlPlus.activated.connect(self.__zoomIn)
        
#         self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)
#         self.CtrlMinus.activated.connect(self.__zoomOut)

#         self.devTools.hide()
#         self.dev_view.loadFinished.connect(self.setDevToolsZoom)
#         self.titlebar = None

#     def __zoomIn(self):
#         """zoom into browser."""
#         currentZoom = self.currentZoomFactor
#         zoomFactor = ZoomFactor(currentZoom).gt(self.zoomFactors).value
#         self.setZoomFactor(zoomFactor)
#         self.currentZoomFactor = zoomFactor
#         self.zoomChanged.emit(self.currentZoomFactor)

#     def __zoomOut(self):
#         """zoom out of browser."""
#         currentZoom = self.currentZoomFactor
#         zoomFactor = ZoomFactor(currentZoom).lt(self.zoomFactors[::-1]).value
#         self.setZoomFactor(zoomFactor)
#         self.currentZoomFactor = zoomFactor
#         self.zoomChanged.emit(self.currentZoomFactor)

#     def getPageBackground(self):
#         """get page background colors from computed css style."""
#         self.page().runJavaScript(
#             "window.getComputedStyle(document.body).backgroundColor", 
#             self._set_background_color,
#         )

#     def _set_background_color(self, bgColor: str):
#         """set the background gradient from the returned gradient result."""
#         # print("\x1b[34;1mbgColor\x1b[0m:", bgColor)
#         import parse
#         try: 
#             matchExpr = "rgb({},{},{})"
#             bgColor = tuple(parse.parse(
#                 matchExpr, bgColor
#             ))
#         except Exception as e:
#             print("\x1b[31;1mui.browser.DebugWebView._set_background_color\x1b[0m:", e)
#             # handle a case where alpha is also present.
#             try:
#                 matchExpr = "rgba({},{},{},{})"
#                 bgColor = tuple(parse.parse(
#                     matchExpr, bgColor
#                 ))
#             except Exception as e:
#                 print("\x1b[31;1mui.browser.DebugWebView._set_background_color\x1b[0m:", e)
#                 # the default color.
#                 bgColor = [89,89,89]
#         self.backgroundChanged.emit(bgColor[0], bgColor[1], bgColor[2])
#         # print("\x1b[34;1mbgColor\x1b[0m:", bgColor)
#         self._page_background_color = bgColor
#         # print("\x1b[31;1mself.titlebar =\x1b[0m", self.titlebar)
#         if self.titlebar is not None:
#             r = bgColor[0]
#             g = bgColor[1]
#             b = bgColor[2]
#             self.titlebar.setTitleBarColor(r, g, b)

#     def prevInHistory(self):
#         self.back()

#     def nextInHistory(self):
#         self.forward()

#     def onPrintRequest(self):
#         print("\x1b[34mprint requested\x1b[0m")
#         defaultPrinter = QPrinter(
#                 QPrinterInfo.defaultPrinter()
#             )
#         dialog = QPrintDialog(defaultPrinter, self)
#         if dialog.exec():
#             # printer object has to be persistent
#             self._printer = dialog.printer()
#             self.page().print(self._printer, self.printResult)

#     def printResult(self, success):
#         print("\x1b[32mprint result\x1b[0m")
#         if success:
#             QMessageBox.information(self, 'Print completed', 
#                 'Printing has been completed!', QMessageBox.Ok)
#         else:
#             QMessageBox.warning(self, 'Print failed', 
#                 'Printing has failed!', QMessageBox.Ok)
#             # self.onPrintRequest()
#         del self._printer    
    
#     def setSpellCheck(self, lang: str="en-US") -> None:
#         """[summary]
#         set the dictionary for spellchecking.
#         Args:
#             lang (str, optional): [description]. Defaults to "en-US".
#         """
#         # print(f"setting spell check for {lang}")
#         self.page().profile().setSpellCheckEnabled(True)
#         self.page().profile().setSpellCheckLanguages((lang,))

#     def initDevTools(self) -> QWidget:
#         """[summary]
#         create the dev tools widget.
#         (dev toolbar and dev tools webpage view.)
#         Returns:
#             QWidget: [description]
#         """
#         self.dev_view = QWebEngineView()
#         sizePolicy = self.dev_view.sizePolicy()
#         sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
#         self.dev_view.setSizePolicy(sizePolicy)
#         devTools = QSplitter(Qt.Vertical)
#         devTools.setStyleSheet("""QWidget {
#             background: transparent;
#         }""")
#         self.devToolbar = self.initDevToolbar()
#         self.devToolbar.setFixedHeight(30)
#         devTools.addWidget(self.devToolbar)
#         devTools.addWidget(self.dev_view)
#         # devToolsLayout.addStretch(1)
#         return devTools

#     def initDevToolbar(self) -> QWidget:
#         devToolbar = QWidget()
#         # devToolbar.setMaximumWidth(200)
#         devToolbarLayout = QHBoxLayout()
#         devToolbarLayout.setSpacing(10)
#         devToolbarLayout.setContentsMargins(0, 0, 0, 0)
#         self.devCloseBtn = DevToolbarBtn("close", type="png", tip="close dev tools")
#         devToolbar.setFixedHeight(20)
#         devToolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
#         devToolbar.setStyleSheet("""
#         QWidget {
#             background: transparent;
#         }""")
#         devToolbarLayout.addStretch(1)
#         devToolbarLayout.addWidget(self.devCloseBtn, 0)
#         # devToolbarLayout.addWidget(self.devMinBtn, 0)
#         devToolbarLayout.addStretch(1)
#         devToolbar.setLayout(devToolbarLayout)

#         return devToolbar

#     def getPageScreenshot(self):
#         size = self.contentsRect()
#         img = QPixmap(size.width(), size.height())
#         self.render(img)
#         # print(img)
#         return img

#     def saveAs(self, name: str):
#         self.saveAsName = name
#         self.page().runJavaScript(
#             "document.body.outerHTML", 
#             self._save_as_callback
#         )

#     def _save_as_callback(self, content: str):
#         try:
#             with open(self.saveAsName, "w") as f:
#                 print(f"writing content to {self.saveAsName}")
#                 f.write(content)
#         except Exception as e:
#             print(f"\x1b[31;1mbrowser._save_as_callback\x1b[0m:", e)

#     def reactToCtrlF(self):
#         # print("is browser pane in focus: ", self.hasFocus())
#         print("triggered \x1b[34;1mui.browser.reactToCtrlF\x1b[0m")
#         print(f"self.searchPanel.isVisible(): {self.searchPanel.isVisible()}")
#         self.searchPanel.show()
#         print(self.searchPanel.x(), self.searchPanel.y())

#     def focusInEvent(self, event):
#         print("entering focus")
#         self.CtrlF.setEnabled(True)

#     def focusOutEvent(self, event):
#         print("exiting focus")
#         self.CtrlF.setEnabled(False)

#     def setUrl(self, url):
#         # self.searchPanel.closePanel()
#         super(DebugWebView, self).setUrl(url)

#     def load(self, url):
#         # self.searchPanel.closePanel()
#         super(DebugWebView, self).load(url)

#     def contextMenuEvent(self, event):
#         self.contextMenu = self.page().createStandardContextMenu()
#         self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
#         for action in self.contextMenu.actions():
#             if action.text() == "Back":
#                 action.setShortcut(QKeySequence.Back)
#             elif action.text() == "Forward":
#                 action.setShortcut(QKeySequence.Forward)
#             elif action.text() == "Reload":
#                 action.setShortcut(QKeySequence.Refresh)
#         self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
#         self.contextMenu.popup(event.globalPos())
#         # # update palette.
#         # palette = self.menu.palette()
#         # palette.setColor(QPalette.Base, QColor(0,0,0))
#         # palette.setColor(QPalette.Text, QColor(125,125,125))
#         # palette.setColor(QPalette.ButtonText, QColor(255,255,255))
#         # print(vars(QPalette))
#         # palette.setColor(QPalette.PlaceholderText, QColor(125,125,125))
#         # palette.setColor(QPalette.Window, QColor(48,48,48))
#         # palette.setColor(QPalette.Highlight, QColor(235,95,52))
#         # # palette.setColor(QPalette.HighlightText, QColor(0,0,0))
#         # self.menu.setPalette(palette)
#         # # apply rounding mask.
#         # roundingPath = QPainterPath()
#         # self.menu.popup(event.globalPos())
#         # roundingPath.addRoundedRect(QRectF(self.menu.rect()), 15, 15)
#         # mask = QRegion(roundingPath.toFillPolygon().toPolygon())
#         # self.menu.setMask(mask)
#     def alert(self, msg: str):
#         self.page().runJavaScript(f"alert(`{msg}`);")

#     def setDevToolsZoom(self):
#         self.dev_view.setZoomFactor(self.dev_tools_zoom)
        
#     def toggleDevTools(self):
#         if self.dev_view.isVisible():
#             self.devTools.hide()
#         else:
#             self.devTools.show()

#     def loadDevTools(self):
#         self.dev_view.load(QUrl("http://0.0.0.0:5000/"))
#         dev_view_page = SilentWebPage(self.dev_view)
#         self.dev_view.setPage(dev_view_page)
#         self.page().setDevToolsPage(dev_view_page)
class EditFlagsDict:
    def __init__(self, editFlags):
        tot = int(editFlags)
        self.tot = int(editFlags)
        self.flag_names = ["Undo", "Redo", "Cut", "Copy", "Paste", "Delete", "SelectAll", "Translate", "EditRichly"] 
        self.flag_enums = [getattr(QWebEngineContextMenuData, f"Can{flag_name}") for flag_name in self.flag_names]
        self.flag_ints = [int(flag_enum) for flag_enum in self.flag_enums]
        self.flag_values = [False for i in range(len(self))]
        # 
        for i in range(len(self)):
            flag_int = self.flag_ints[len(self)-1-i]
            if tot - flag_int >= 0:
                self.flag_values[len(self)-1-i] = True
                tot -= flag_int

    def __str__(self):
        return str({f"Can{k}": v for k,v in zip(self.flag_names, self.flag_values)})

    def __len__(self):
        return len(self.flag_names)

    def __iter__(self):
        for name in self.flag_names:
            yield name

    def __getattr__(self, flag_name: str):
        index = self.flag_names.index(flag_name)
        return self.flag_values[index]

# QWebEngineView for debug web view splitter.
class DebugWebBrowser(QWebEngineView):
    zoomChanged = pyqtSignal(float)
    def __init__(self, accent_color: str="green",
                 zoomFactor: float=1.25, 
                 parent: Union[QWidget, None]=None):
        super(DebugWebBrowser, self).__init__(parent)
        self.accent_color = accent_color
        # search panel for "find in page".
        self.searchPanel = BrowserSearchPanel()
        self.searchPanel.connectBrowser(self)
        self.searchPanel.move(50,50)
        # custom web page.
        custom_page = CustomWebPage(
            self, logging_level=3, 
            search_panel=self.searchPanel,            
        )
        self.setPage(custom_page)
        # update settings.
        self.settings().setFontFamily(QWebEngineSettings.StandardFont, "Noto Sans")
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        # current zoom factor and webview.
        self.currentZoomFactor = zoomFactor
        zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
        self.zoomFactors = [ZoomFactor(zf) for zf in zoomFactors]
        # shortcuts.
        self.Esc = QShortcut(QKeySequence("Esc"), self)
        self.CtrlF = QShortcut(QKeySequence("Ctrl+F"), self)
        self.RefreshShortcut = QShortcut(QKeySequence.Refresh, self)
        self.ForwardShortcut = QShortcut(QKeySequence.Forward, self)
        self.BackShortcut = QShortcut(QKeySequence.Back, self)
        self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
        self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)

        self.Esc.activated.connect(self.searchPanel.closePanel)
        self.CtrlF.activated.connect(self.reactToCtrlF)
        self.RefreshShortcut.activated.connect(self.reload)
        self.ForwardShortcut.activated.connect(self.forward)
        self.BackShortcut.activated.connect(self.back)
        self.CtrlPlus.activated.connect(self.__zoomIn)
        self.CtrlMinus.activated.connect(self.__zoomOut)

    def changeUserAgent(self):
        userAgentStr = "Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0" 
        self.page().profile().setHttpUserAgent(userAgentStr)    

    def reactToCtrlF(self):
        # print("is browser pane in focus: ", self.hasFocus())
        print("triggered \x1b[34;1mui.browser.reactToCtrlF\x1b[0m")
        print(f"self.searchPanel.isVisible(): {self.searchPanel.isVisible()}")
        self.searchPanel.show()
        print(self.searchPanel.x(), self.searchPanel.y())

    def focusInEvent(self, event):
        print("entering focus")
        self.CtrlF.setEnabled(True)
        super(DebugWebBrowser, self).focusInEvent(event)

    def focusOutEvent(self, event):
        print("exiting focus")
        self.CtrlF.setEnabled(False)
        super(DebugWebBrowser, self).focusOutEvent(event)

    def setUrl(self, url):
        # self.searchPanel.closePanel()
        super(DebugWebBrowser, self).setUrl(url)

    def load(self, url):
        # self.searchPanel.closePanel()
        super(DebugWebBrowser, self).load(url)

    def alert(self, msg: str):
        self.page().runJavaScript(f"alert(`{msg}`);")

    def prevInHistory(self):
        self.back()

    def nextInHistory(self):
        self.forward()

    def __zoomIn(self):
        """zoom into browser."""
        currentZoom = self.currentZoomFactor
        zoomFactor = ZoomFactor(currentZoom).gt(self.zoomFactors).value
        self.setZoomFactor(zoomFactor)
        self.currentZoomFactor = zoomFactor
        self.zoomChanged.emit(self.currentZoomFactor)

    def __zoomOut(self):
        """zoom out of browser."""
        currentZoom = self.currentZoomFactor
        zoomFactor = ZoomFactor(currentZoom).lt(self.zoomFactors[::-1]).value
        self.setZoomFactor(zoomFactor)
        self.currentZoomFactor = zoomFactor
        self.zoomChanged.emit(self.currentZoomFactor)

    def onPrintRequest(self):
        defaultPrinter = QPrinter(QPrinterInfo.defaultPrinter())
        dialog = QPrintDialog(defaultPrinter, self)
        if dialog.exec():
            self._printer = dialog.printer() # printer object has to be persistent
            self.page().print(self._printer, self.printResult)

    def printResult(self, success):
        print("\x1b[32mprint result\x1b[0m")
        if success:
            QMessageBox.information(self, 'Print completed', 
                'Printing has been completed!', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Print failed', 
                'Printing has failed!', QMessageBox.Ok)
            # self.onPrintRequest()
        del self._printer    

    def addCMenuAction(self, key: str, text: str, icon: str="", 
                       shortcut: QKeySequence=None, add_sep: bool=False) -> QAction:
        if key not in self.actionMap: return None
        slot_fn = self.actionMap[key]
        is_enabled = self.enabledMap[key]
        base, ext = os.path.splitext(icon)
        # set disabled icon if it exists and action is disabled.
        if not is_enabled:
            if os.path.exists(FigD.icon(base+"_disabled"+ext)):
                icon = base+"_disabled"+ext
        if shortcut is None:
            action = self.contextMenu.addAction(
                FigD.Icon(icon), 
                text, slot_fn,
            )
        else:
            action = self.contextMenu.addAction(
                FigD.Icon(icon), text, 
                slot_fn, shortcut,
            )
        action.setEnabled(is_enabled)
        if add_sep: self.contextMenu.addSeparator()

        return action

    def invokeInspect(self, trigger):
        print("\x1b[32minvokeInspect\x1b[0m")
        if hasattr(self, "webview_ptr"):
            self.webview_ptr.devTools.show()
        trigger()

    def contextMenuEvent(self, event):
        baseContextMenu = self.page().createStandardContextMenu()
        data = self.page().contextMenuData()
        actionMap = {}
        enabledMap = {}
        for action in baseContextMenu.actions():
            actionMap[action.text()] = action.trigger
            enabledMap[action.text()] = action.isEnabled()
        self.actionMap = actionMap
        self.enabledMap = enabledMap
        # new context menu.
        self.contextMenu = QMenu()
        def blank(): pass
        print(f"""\x1b[34;1mdata: {data.mediaType()}\x1b[0m""")
        editFlags = EditFlagsDict(data.editFlags())
        # print(editFlags)
        if data.mediaType() == QWebEngineContextMenuData.MediaTypeNone:
            undo = self.addCMenuAction("Undo", "&Undo", "textedit/undo.svg", QKeySequence.Undo)
            redo = self.addCMenuAction("Redo", "&Redo", "textedit/redo.svg", QKeySequence.Redo)
            cut = self.addCMenuAction("Cut", "Cu&t", "textedit/cut.svg", QKeySequence.Cut)
            copy = self.addCMenuAction("Copy", "Copy", "textedit/copy.svg", QKeySequence.Copy)
            paste = self.addCMenuAction("Paste", "&Paste", "textedit/paste.svg", QKeySequence.Paste)
            openLinkInNewTab = self.addCMenuAction(
                "Open link in new tab", 
                "Open link in new tab",
            )
            openLinkInNewWindow = self.addCMenuAction(
                "Open link in new window", 
                "Open link in new window",
            )
            openLinkInNewIncogWin = self.addCMenuAction(
                "Open link in new window", 
                "Open link in incognito window", add_sep=True,
            )
            saveLink = self.addCMenuAction(
                "Save link", 
                "Save link as...", 
            )
            copyLinkAddress = self.addCMenuAction(
                "Copy link address", 
                "Copy link address", add_sep=True,
            )
            pasteAndMatchStyle = self.addCMenuAction( 
                "Paste and match style",
                "Paste and match style      ",
                shortcut=QKeySequence("Ctrl+Shift+V"),
            )
            pasteAsPlainText = self.addCMenuAction(
                "Paste as plain text",
                "Paste as plain text      ", 
                shortcut=QKeySequence("Ctrl+Shift+V"),
            )
            selectAll = self.addCMenuAction(
                "Select all", "Select all", 
                shortcut=QKeySequence.SelectAll,
                add_sep=True, 
            )
            back = self.addCMenuAction(
                "Back", "Back", "textedit/back.svg",
                shortcut=QKeySequence.Back,
            )
            forward = self.addCMenuAction(
                "Forward", "Forward", 
                "textedit/forward.svg",
                shortcut=QKeySequence.Forward,
            )
            reload_ = self.addCMenuAction(
                "Reload", "Reload", "textedit/reload.svg", 
                shortcut=QKeySequence.Refresh, add_sep=True,
            )
            savePage = self.addCMenuAction(
                "Save page", "Save as...", 
                "titlebar/save.svg", 
                shortcut=QKeySequence.Save,
            )
            if not data.isContentEditable():
                self.contextMenu.addAction(
                    FigD.Icon("titlebar/print.svg"),
                    "Print...", self.onPrintRequest, 
                    QKeySequence.Print,
                )
                self.contextMenu.addAction(
                    FigD.Icon("navbar/cast.svg"),
                    "Cast...", blank
                )
                self.contextMenu.addAction(
                    FigD.Icon("browser/google_lens.png"),
                    "Search images with Google Lens      ",
                )
                self.contextMenu.addSeparator()
                self.contextMenu.addAction(
                    FigD.Icon("tabbar/devices.svg"), 
                    "Send to your devices"
                )
                self.contextMenu.addAction(
                    FigD.Icon("system/fileviewer/qr.svg"), 
                    "Create QR code for this page"
                )
                self.contextMenu.addSeparator()
                self.contextMenu.addAction(
                    FigD.Icon("trans.svg"), 
                    "Translate to English",
                )
                self.contextMenu.addSeparator()
            else:
                self.spellCheckMenu = self.contextMenu.addMenu("Spell check")
                self.spellCheckMenu.addAction("All your languages")
                self.spellCheckMenu.addAction("English (United States)")
                self.spellCheckMenu.addAction("English")
                self.spellCheckMenu.addAction("Language settings")
                self.spellCheckMenu.addSeparator()
                self.spellCheckMenu.addAction("Use basic spell check")
                self.spellCheckMenu.addAction("Use enhanced spell check")
                self.spellCheckMenu = styleContextMenu(
                    self.spellCheckMenu, 
                    self.accent_color,
                )
                # sub menu to change writing direction,
                self.writingMenu = self.contextMenu.addMenu("Writing Direction")
                self.writingMenu.addAction("Default")
                self.writingMenu.addAction("Left to Right")
                self.writingMenu.addAction("Right to Left")
                self.writingMenu = styleContextMenu(
                    self.writingMenu, 
                    self.accent_color,
                )
                self.contextMenu.addSeparator()
            viewPageSource = self.addCMenuAction(
                "View page source", 
                "View page source",
                "titlebar/source.svg",
                shortcut=QKeySequence("Ctrl+U"),
            )
        elif data.mediaType() == QWebEngineContextMenuData.MediaTypeImage:
            self.contextMenu.addAction("Open image in new tab") 
            saveImage = self.contextMenu.addAction(
                "Save image as...",
                actionMap["Save image"],
            ) 
            saveImage.setEnabled(enabledMap["Save image"])
            copyImage = self.contextMenu.addAction(
                "Copy image", 
                actionMap["Copy image"]
            )
            copyImage.setEnabled(enabledMap["Copy image"]) 
            copyImageAddress = self.contextMenu.addAction(
                "Copy image address", 
                actionMap["Copy image address"]
            )
            copyImageAddress.setEnabled(enabledMap["Copy image address"])
            self.contextMenu.addSeparator()            
            self.contextMenu.addAction(
                FigD.Icon("system/fileviewer/qr.svg"), 
                "Create QR code for this image",
            )
            self.contextMenu.addAction("Search image with Google Lens      ")
            self.contextMenu.addSeparator()
            self.contextMenu.addAction(
                "Search Google with this image"
            )
            self.contextMenu.addSeparator()
        else: 
            self.contextMenu = baseContextMenu
        if "Inspect" in actionMap:
            self.contextMenu.addAction(
                FigD.Icon("browser/inspect.svg"), "Inspect", 
                partial(self.invokeInspect, actionMap["Inspect"]),
                QKeySequence("Ctrl+Shift+I"),
            )
        print(actionMap)
        # style context menu.
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        # self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
        # show context menu popup with global position based on the event.
        self.contextMenu.popup(event.globalPos())

    def setSpellCheck(self, lang: str="en-US") -> None:
        """[summary]
        set the dictionary for spellchecking.
        Args:
            lang (str, optional): [description]. Defaults to "en-US".
        """
        print(f"setting spell check for {lang}")
        self.page().profile().setSpellCheckEnabled(True)
        self.page().profile().setSpellCheckLanguages((lang,))

    def getPageScreenshot(self):
        size = self.contentsRect()
        img = QPixmap(size.width(), size.height())
        self.render(img)

        return img

    def saveAs(self, name: str):
        self._save_as_name = name
        self.page().runJavaScript(
            "document.body.outerHTML", 
            self._save_as_callback
        )

    def __str__(self):
        return "\x1b[33;1mui::browser::DebugWebBrowser\x1b[0m"

    def _save_as_callback(self, content: str):
        try:
            with open(self._save_as_name, "w") as f:
                print(f"writing content to {self._save_as_name}")
                f.write(content)
        except Exception as e:
            print(f"\x1b[31;1mbrowser._save_as_callback\x1b[0m:", e)

# dev tools view (QWebEngineView)
class DevToolsView(QWebEngineView):
    def __str__(self):
        return "\x1b[31;1mui::browser::DevToolsView\x1b[0m"

# spitter with web browser and dev tools.
class DebugWebView(QSplitter):
    showMessage = pyqtSignal(str)
    changeTabIcon = pyqtSignal(str)
    changeTabTitle = pyqtSignal(str)
    changeTabToolTip = pyqtSignal(str)
    backgroundChanged = pyqtSignal(int, int, int)
    def __init__(self, browser, parent: Union[QWidget, None]=None,
                 dev_tools_zoom: float=1.35, accent_color: str="green"):
        super(DebugWebView, self).__init__(Qt.Horizontal, parent)
        self.accent_color = accent_color
        self._page_background_colors = []
        # dev tools pane.
        self.devTools = self.initDevTools()
        self.devTools.hide()
        self.devCloseBtn.clicked.connect(self.devTools.hide)
        # self.devToolsBtn = DevToolsBtn()    
        self.dev_tools_zoom = dev_tools_zoom
        # self.devToolsBtn.clicked.connect(self.toggleDevTools)
        # browser.
        self.browser = browser
        self.browser.webview_ptr = self
        self.browser.urlChanged.connect(self.onUrlChange)
        self.addWidget(self.browser)
        self.addWidget(self.devTools)
        # splitter sizes.
        self.setSizes([500, 300])
        # dev tools toggling shortcut.
        self.CtrlShiftI = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
        self.CtrlShiftI.activated.connect(self.toggleDevTools)
        self.dev_view.loadFinished.connect(self.setDevToolsZoom)
        self.titlebar_ptr = None

    def onUrlChange(self):
        self.browser.setZoomFactor(self.browser.currentZoomFactor)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def viewSource(self):
        print("trigger viewSource for ui::browser::DebugWebView")

    def emitTabIcon(self, html: str):
        import requests
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, features="html.parser")
        icon_links = soup.findAll("link", **{"rel": "icon"})
        icon_path, is_svg = None, False
        qurl = self.browser.url()
        # base url for the server (scheme+host).
        url = f"{qurl.scheme()}://{qurl.host()}"
        
        # check in icon links for viable URL.
        for icon in icon_links:
            icon_path = icon["href"]
            if icon.get("type")=="image/svg+xml": 
                is_svg = True
                break
        # if no icon path is found make the guess url/favicon.ico
        if icon_path is None:
            icon_path = os.path.join(url, "favicon.ico")
        elif isinstance(icon_path, str):
            if not icon_path.startswith("http"):
                if url.endswith("/"): url = url[:-1]
                icon_path = url+icon_path
        if icon_path:
            try:
                content = requests.get(icon_path)
                path = "/tmp/lol1_2hjalx_ffl2c."
                if is_svg: 
                    path += "svg"
                    with open(path, "w") as f:
                        f.write(content.text)
                else: 
                    path += "png"
                    with open(path, "wb") as f:
                        f.write(content.content)
                # print(f"icon fetched from url: {icon_path}")
                icon_path = path
            except MissingSchema as e:
                # print(e)
                icon_path = FigD.icon("browser.svg")
                # print(f"default icon: {icon_path}")
            except InvalidSchema as e:
                # print(e)  
                icon_path = icon_path.replace("file://","")
                # print(f"locally sourced icon: {icon_path}")
        else:
            icon_path = FigD.icon("browser.svg")
            # print(f"default icon: {icon_path}")
        self.changeTabIcon.emit(icon_path)
        # tabBar = self.tabWidget.tabBar()
        # animLabel = tabBar.tabButton(self.i, QTabBar.LeftSide)
        # if animLabel is None: animLabel = QLabel()
        # print("\x1b[34;1msetting pixmap\x1b[0m")
        # self.pagePixmap = pageIcon.pixmap(QSize(20,20))
        # self.pagePixmap.save("DELETE_THIS_BROWSER_PIXMAP.png")
        # print("pixmap:", animLabel.pixmap())
        # print("movie:", animLabel.movie())
        # animLabel.setPixmap(self.pagePixmap)
    def changeZoom(self, value: float):
        self.browser.setZoomFactor(value/100)

    def setIcon(self, tabs, i: int):
        self.i = i
        self.tabs = tabs
        self.page().toHtml(self.iconSetCallback)

    def onLoadFinished(self):
        lang: str="en-US"        
        self.loadDevTools()
        self.browser.setSpellCheck(lang)
        self.changeTabTitle.emit(
            self.browser.page().title()
        )
        self.browser.page().printRequested.connect(
            self.browser.onPrintRequest
        )
        # navbar.reloadBtn.setStopMode(False)
        # navbar stuff: set url to searchbar.
        
        # use page background to change navbar color.
        # self.browser.getPageBackground()

        # show howered link on statusbar.
        self.browser.page().linkHovered.connect(
            self.emitStatusBarMessage
        )
        # if browser.isTerminalized():
        #     browser.execTerminalJS()
        # else:
        # change user agent.
        self.browser.changeUserAgent()

        # load annotation tools and update word count.
        # browser.execAnnotationJS() 
        # browser.setWordCount()
        
        # fetch page icon and emit changeTabIcon
        self.browser.page().toHtml(self.emitTabIcon)
        # update scrollbar and selection style.
        # browser.setSelectionStyle()
        # browser.setScrollbar(scrollbar_style)
        
        # emit tab tool tip.
        self.browser.page().runJavaScript(
            "document.body.outerHTML",
            self.emitTabToolTip,
        )

    def emitStatusBarMessage(self, message: str):
        self.showMessage.emit(message)

    def emitTabToolTip(self, html):
        """emit tab tooltip once document.body.outerHTML is constructed."""
        screenshot = self.browser.getPageScreenshot()
        screenshot = screenshot.scaled(
            400, 400, 
            aspectRatioMode=Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation
        )
        # convert pixmap to base 64 in memory.
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        screenshot.save(buffer, "PNG")
        encoded = buffer.data().toBase64()
        # create the tooltip
        tabToolTip = f"""
        <img src="data:image/png;base64,{bytes(encoded).decode()}">
        <div style='text-align: center;'>
            <h3 style='font-weight: bold;'>{self.browser.page().title()}</h3>
            <br> 
            <span style='color: #6e6e6e;'>{self.browser.url().host()}</span>
        </div>
        """
        self.changeTabToolTip.emit(tabToolTip)

    def getPageBackground(self):
        """get page background colors from computed css style."""
        self.browser.page().runJavaScript(
            "window.getComputedStyle(document.body).backgroundColor", 
            self._set_background_color,
        )

    def _set_background_color(self, bgColor: str):
        """set the background gradient from the returned gradient result."""
        # print("\x1b[34;1mbgColor\x1b[0m:", bgColor)
        scope_str = "\x1b[31;1mui.browser.DebugWebView._set_background_color\x1b[0m:"
        import parse
        try: 
            matchExpr = "rgb({},{},{})"
            bgColor = tuple(parse.parse(
                matchExpr, bgColor
            ))
        except Exception as e:
            print(scope_str, e)
            # handle a case where alpha is also present.
            try:
                matchExpr = "rgba({},{},{},{})"
                bgColor = tuple(parse.parse(
                    matchExpr, bgColor
                ))
            except Exception as e:
                print(scope_str, e)
                bgColor = [89,89,89] # the default color.
        # emit background changed signal for the browser.
        self.backgroundChanged.emit(bgColor[0], bgColor[1], bgColor[2])
        self._page_background_color = bgColor
        if self.titlebar_ptr is not None:
            r = bgColor[0]
            g = bgColor[1]
            b = bgColor[2]
            self.titlebar_ptr.setTitleBarColor(r, g, b)

    def initDevTools(self) -> QWidget:
        """[summary]
        create the dev tools widget.
        (dev toolbar and dev tools webpage view.)
        Returns:
            QWidget: [description]
        """
        self.dev_view = DevToolsView()
        sizePolicy = self.dev_view.sizePolicy()
        sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
        self.dev_view.setSizePolicy(sizePolicy)
        # create dev tools.
        dev_tools = QSplitter(Qt.Vertical)
        dev_tools.addWidget(self.initDevToolbar())
        dev_tools.addWidget(self.dev_view)
        dev_tools.setStyleSheet("""QWidget {
            background: transparent;
        }""")
        return dev_tools

    def initDevToolbar(self) -> QWidget:
        toolbar = QWidget()
        toolbar.setFixedHeight(20)
        toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        toolbar.setStyleSheet("""
        QWidget {
            background: transparent;
        }""")
        self.devCloseBtn = DevToolbarBtn("close", type="png", tip="close dev tools")
        # create dev toolbar layout.
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)        
        # build layout.
        layout.addStretch(1)
        layout.addWidget(self.devCloseBtn, 0)
        layout.addStretch(1)
        # set layout.
        toolbar.setLayout(layout)
        toolbar.setFixedHeight(30)

        return toolbar

    def __str__(self):
        return "\x1b[32;1mui::browser::DebugWebView\x1b[0m"

    def getPageScreenshot(self):
        return self.browser.getPageScreenshot()

    def saveAs(self, name: str):
        self.browser.saveAs(name)

    def setDevToolsZoom(self):
        self.dev_view.setZoomFactor(self.dev_tools_zoom)
        
    def toggleDevTools(self):
        if self.dev_view.isVisible():
            self.devTools.hide()
        else:
            self.devTools.show()

    def loadDevTools(self):
        self.dev_view.load(QUrl("http://0.0.0.0:5000/"))
        dev_view_page = SilentWebPage(self.dev_view)
        self.dev_view.setPage(dev_view_page)
        self.browser.page().setDevToolsPage(dev_view_page)
        
scrollbar_style = '''*::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
*::-webkit-scrollbar-track:hover {
    background: rgba(29, 29, 29, 0.4);
}    
*::-webkit-scrollbar-track {
    /* background-color: rgba(235, 235, 235, 0.8); */
    background: linear-gradient(0deg, rgba(235,95,52,0.8) 0%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-thumb {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb:hover {
    background: rgb(235,95,52);
    background: linear-gradient(0deg, rgba(235,95,52,1) 40%, rgba(235,204,52,1) 94%);
}
*::-webkit-scrollbar-corner {
    background-color: transparent;
    /* background: rgba(235, 235, 235, 0.1); */
}'''
selection_style = '''
::selection {
	color: #fff;
    background-color: rgb(235,95,52);
}
::selection:window-inactive {
	color: #000;
    background-color: rgb(235,204,52);
}'''
class PageInfo(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(PageInfo, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        # page info.
        self.label = QLabel("Page Info")
        self.label.setStyleSheet('''
        QLabel {
            border: 0px;
            padding: 10px;
            color: #eb5f34;
            font-size: 20px;
            font-weight: bold;
        }''')
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        # word count of page.
        self.word_count = QToolButton(self)
        self.word_count.setIcon(FigD.Icon("time_to_read.svg"))
        self.word_count.setIconSize(QSize(20,20))
        self.word_count.setText(" 0 words")
        self.word_count.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.word_count.setToolTip("word count of webpage.")
        self.word_count.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.word_count.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.word_count)
        # time taken to read.
        self.time_to_read = QToolButton(self)
        self.time_to_read.setIcon(FigD.Icon("word_count.svg"))
        self.time_to_read.setIconSize(QSize(20,20))
        self.time_to_read.setText(" 0 mins")
        self.time_to_read.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.time_to_read.setToolTip("time taken to read webpage.")
        self.time_to_read.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.time_to_read.setAttribute(Qt.WA_TranslucentBackground)
        self.layout.addWidget(self.time_to_read)
        self.layout.addStretch(1)

        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        
        wrapper = QWidget()
        wrapper.setObjectName("wrapper")
        wrapper.setStyleSheet('''
        QWidget#wrapper {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }''')
        wrapper.setLayout(self.layout)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.word_count.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            padding: 5px;
        }''')
        self.time_to_read.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            padding: 5px;
        }''')

        self.setGraphicsEffect(glow_effect)
        self.setFixedWidth(150)
        layout.addWidget(wrapper)
        self.setLayout(layout)
        # self.setFixedWidth(100)
    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()
    
    def update(self, word_count: Union[int, None]):
        if word_count is None:
            word_count = 0
        '''assuming average human adult reads at 200 wpm'''
        self.word_count.setText(f" {word_count} words")
        self.time_to_read.setText(f" {word_count // 200} mins")
        # self.setFixedHeight(100)

# class WrappedAction(QAction):
#     def __init__(self, action: QAction):
#         super(WrappedAction, self).__init__()
#         self._original_action_ref = action
#         self.triggered.connect(self.callback)

#     def original(self):
#         return self._original_action_ref

#     def callback(self):
#         print(f"wrapped action for {self.original.text()} triggered")
#         self._original_action_ref.trigger()
#         print(f"after triggering of {self.original.text()} is done")
def inspectTriggered(browser, inspect_action):
    if not browser.dev_view.isVisible():
        browser.dev_view.show()
    inspect_action.trigger()

def parse_debug_webview_args():
	parser = argparse.ArgumentParser("system imageviewer application for Fig Dashboard")
	parser.add_argument("-p", "--path", type=str, default=None,
                        help="path to file to be opened")
	parser.add_argument("-u", "--url", type=str, 
                        default="https://www.google.com", 
						help="url to be opened")

	return parser.parse_args()

def debug_webview_factory(**args):
    """factory method to create debug webview."""
    path = args.get("path")
    url = args.get("url", "https://www.google.com")
    accent_color = args.get("accent_color", 'orange')
    browser = DebugWebBrowser(accent_color=accent_color)
    webview = DebugWebView(
        browser=browser,
        accent_color=accent_color,
    )
    if path is None: url = QUrl(url)
    else: url = QUrl.fromLocalFile(path)
    browser.load(url)

    return webview

def debug_webview_window_factory(**args):
    from fig_dash.ui import wrapFigDWindow
    from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
    # accent color.
    icon_size = (25,25)
    icon = FigDSystemAppIconMap["debug_webview"]
    accent_color = FigDAccentColorMap["debug_webview"]
    widget_args = {
		# "css_grad": create_css_grad(extract_colors_from_qt_grad(accent_color)),
		"path": args.get("path"),
        "accent_color": accent_color,
        "url": args.get("url", "https://www.google.com"),
	}
    webview = debug_webview_factory(**widget_args)
    tab_title = f"Welcome {getpass.getuser()}"
    tab_icon = FigD.icon("browser.svg")
    window = wrapFigDWindow(
		webview, title="Debug Webview", icon=icon, size=icon_size, autohide=False,
        name="debug_webview", accent_color=accent_color, widget_args=widget_args,
        widget_factory=debug_webview_factory, window_args=args, 
		titlebar_callbacks={
			"viewSourceBtn": webview.viewSource,
		}, window_factory=debug_webview_window_factory,
		find_function=webview.browser.reactToCtrlF,
		tab_title=tab_title, tab_icon=tab_icon,
	)

    return window

# test debug webview.
def test_debug_webview():
    FigD("/home/atharva/GUI/fig-dash/resources")
    from fig_dash.ui import FigDAppContainer
    app = FigDAppContainer(sys.argv)
    args = parse_debug_webview_args()
    window = debug_webview_window_factory(**vars(args))
    window.show()
    app.exec()

# main function
if __name__ == "__main__":
    test_debug_webview()