#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::browser")
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
import sys
import copy
import jinja2
import socket
import getpass
import pathlib
import subprocess
from typing import Union, Tuple, List
from requests.exceptions import MissingSchema, InvalidSchema
# Qt5 imports.
from PyQt5.QtPrintSupport import QPrinter, QPrinterInfo, QPrintDialog
from PyQt5.QtWebEngineCore import QWebEngineFindTextResult
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings, QWebEngineContextMenuData
from PyQt5.QtGui import QColor, QFont, QPalette, QKeySequence, QIcon, QMovie, QPixmap, QGradient, QLinearGradient, QPainterPath, QRegion
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize, QPoint, QPointF, QRectF, QObject
from PyQt5.QtWidgets import QTabBar, QToolBar, QToolButton, QSplitter, QLabel, QWidget, QAction, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QTextEdit, QPlainTextEdit, QShortcut, QMessageBox, QFrame
# fig_dash
from fig_dash.assets import FigD
from fig_dash.utils import QFetchIcon, collapseuser
from fig_dash.api.browser.extensions import ExtensionManager
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

# web view class with dev tools.
class DebugWebView(QWebEngineView):
    zoomChanged = pyqtSignal(float)
    backgroundChanged = pyqtSignal(int, int, int)
    def __init__(self, parent: Union[QWidget, None]=None, zoomFactor: float=1.25, 
                 dev_tools_zoom: float=1.35, accent_color: str="green"):
        super(DebugWebView, self).__init__(parent)
        self.accent_color = accent_color
        self.devTools = self.initDevTools()
        self.devCloseBtn.clicked.connect(self.devTools.hide)
        self.devToolsBtn = DevToolsBtn(self)    
        self.dev_tools_zoom = dev_tools_zoom
        self.devToolsBtn.clicked.connect(self.toggleDevTools)
        # current zoom factor of the main web view.
        self.currentZoomFactor = zoomFactor
        zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
        self.zoomFactors = [ZoomFactor(zf) for zf in zoomFactors]

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self)
        self.splitter.addWidget(self.devTools)
        # self.splitter.addWidget(self.py_dev_view)
        self.splitter.setSizes([500, 300])
        # back reference to browser.
        self.splitter.browser = self
        self._page_background_colors = []

        self.searchPanel = BrowserSearchPanel()
        self.searchPanel.connectBrowser(self)
        self.searchPanel.move(50,50)

        custom_page = CustomWebPage(
            self, logging_level=3, 
            search_panel=self.searchPanel,            
        )
        self.setPage(custom_page)
        # shortcuts.
        self.Esc = QShortcut(QKeySequence("Esc"), self)
        self.Esc.activated.connect(self.searchPanel.closePanel)

        self.CtrlF = QShortcut(QKeySequence("Ctrl+F"), self)
        self.CtrlF.activated.connect(self.reactToCtrlF)
        
        self.RefreshShortcut = QShortcut(QKeySequence.Refresh, self)
        self.RefreshShortcut.activated.connect(self.reload)
        
        self.ForwardShortcut = QShortcut(QKeySequence.Forward, self)
        self.ForwardShortcut.activated.connect(self.forward)
        
        self.BackShortcut = QShortcut(QKeySequence.Back, self)
        self.BackShortcut.activated.connect(self.back)
        
        self.CtrlShiftI = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
        self.CtrlShiftI.activated.connect(self.toggleDevTools)
        
        self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
        self.CtrlPlus.activated.connect(self.__zoomIn)
        
        self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)
        self.CtrlMinus.activated.connect(self.__zoomOut)

        self.devTools.hide()
        self.dev_view.loadFinished.connect(self.setDevToolsZoom)
        self.titlebar = None

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

    def getPageBackground(self):
        """get page background colors from computed css style."""
        self.page().runJavaScript(
            "window.getComputedStyle(document.body).backgroundColor", 
            self._set_background_color,
        )

    def _set_background_color(self, bgColor: str):
        """set the background gradient from the returned gradient result."""
        # print("\x1b[34;1mbgColor\x1b[0m:", bgColor)
        import parse
        try: 
            matchExpr = "rgb({},{},{})"
            bgColor = tuple(parse.parse(
                matchExpr, bgColor
            ))
        except Exception as e:
            print("\x1b[31;1mui.browser.DebugWebView._set_background_color\x1b[0m:", e)
            # handle a case where alpha is also present.
            try:
                matchExpr = "rgba({},{},{},{})"
                bgColor = tuple(parse.parse(
                    matchExpr, bgColor
                ))
            except Exception as e:
                print("\x1b[31;1mui.browser.DebugWebView._set_background_color\x1b[0m:", e)
                # the default color.
                bgColor = [89,89,89]
        self.backgroundChanged.emit(bgColor[0], bgColor[1], bgColor[2])
        # print("\x1b[34;1mbgColor\x1b[0m:", bgColor)
        self._page_background_color = bgColor
        # print("\x1b[31;1mself.titlebar =\x1b[0m", self.titlebar)
        if self.titlebar is not None:
            r = bgColor[0]
            g = bgColor[1]
            b = bgColor[2]
            self.titlebar.setTitleBarColor(r, g, b)

    def prevInHistory(self):
        self.back()

    def nextInHistory(self):
        self.forward()

    def onPrintRequest(self):
        print("\x1b[34mprint requested\x1b[0m")
        defaultPrinter = QPrinter(
                QPrinterInfo.defaultPrinter()
            )
        dialog = QPrintDialog(defaultPrinter, self)
        if dialog.exec():
            # printer object has to be persistent
            self._printer = dialog.printer()
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
    
    def setSpellCheck(self, lang: str="en-US") -> None:
        """[summary]
        set the dictionary for spellchecking.
        Args:
            lang (str, optional): [description]. Defaults to "en-US".
        """
        # print(f"setting spell check for {lang}")
        self.page().profile().setSpellCheckEnabled(True)
        self.page().profile().setSpellCheckLanguages((lang,))

    def initDevTools(self) -> QWidget:
        """[summary]
        create the dev tools widget.
        (dev toolbar and dev tools webpage view.)
        Returns:
            QWidget: [description]
        """
        self.dev_view = QWebEngineView()
        sizePolicy = self.dev_view.sizePolicy()
        sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
        self.dev_view.setSizePolicy(sizePolicy)
        devTools = QSplitter(Qt.Vertical)
        devTools.setStyleSheet("""QWidget {
            background: transparent;
        }""")
        self.devToolbar = self.initDevToolbar()
        self.devToolbar.setFixedHeight(30)
        devTools.addWidget(self.devToolbar)
        devTools.addWidget(self.dev_view)
        # devToolsLayout.addStretch(1)
        return devTools

    def initDevToolbar(self) -> QWidget:
        devToolbar = QWidget()
        # devToolbar.setMaximumWidth(200)
        devToolbarLayout = QHBoxLayout()
        devToolbarLayout.setSpacing(10)
        devToolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.devCloseBtn = DevToolbarBtn("close", type="png", tip="close dev tools")
        devToolbar.setFixedHeight(20)
        devToolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        devToolbar.setStyleSheet("""
        QWidget {
            background: transparent;
        }""")
        devToolbarLayout.addStretch(1)
        devToolbarLayout.addWidget(self.devCloseBtn, 0)
        # devToolbarLayout.addWidget(self.devMinBtn, 0)
        devToolbarLayout.addStretch(1)
        devToolbar.setLayout(devToolbarLayout)

        return devToolbar

    def getPageScreenshot(self):
        size = self.contentsRect()
        img = QPixmap(size.width(), size.height())
        self.render(img)
        # print(img)
        return img

    def saveAs(self, name: str):
        self.saveAsName = name
        self.page().runJavaScript(
            "document.body.outerHTML", 
            self._save_as_callback
        )

    def _save_as_callback(self, content: str):
        try:
            with open(self.saveAsName, "w") as f:
                print(f"writing content to {self.saveAsName}")
                f.write(content)
        except Exception as e:
            print(f"\x1b[31;1mbrowser._save_as_callback\x1b[0m:", e)

    def reactToCtrlF(self):
        # print("is browser pane in focus: ", self.hasFocus())
        print("triggered \x1b[34;1mui.browser.reactToCtrlF\x1b[0m")
        print(f"self.searchPanel.isVisible(): {self.searchPanel.isVisible()}")
        self.searchPanel.show()
        print(self.searchPanel.x(), self.searchPanel.y())

    def focusInEvent(self, event):
        print("entering focus")
        self.CtrlF.setEnabled(True)

    def focusOutEvent(self, event):
        print("exiting focus")
        self.CtrlF.setEnabled(False)

    def setUrl(self, url):
        # self.searchPanel.closePanel()
        super(DebugWebView, self).setUrl(url)

    def load(self, url):
        # self.searchPanel.closePanel()
        super(DebugWebView, self).load(url)

    def contextMenuEvent(self, event):
        self.contextMenu = self.page().createStandardContextMenu()
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        for action in self.contextMenu.actions():
            if action.text() == "Back":
                action.setShortcut(QKeySequence.Back)
            elif action.text() == "Forward":
                action.setShortcut(QKeySequence.Forward)
            elif action.text() == "Reload":
                action.setShortcut(QKeySequence.Refresh)
        self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
        self.contextMenu.popup(event.globalPos())
        # # update palette.
        # palette = self.menu.palette()
        # palette.setColor(QPalette.Base, QColor(0,0,0))
        # palette.setColor(QPalette.Text, QColor(125,125,125))
        # palette.setColor(QPalette.ButtonText, QColor(255,255,255))
        # print(vars(QPalette))
        # palette.setColor(QPalette.PlaceholderText, QColor(125,125,125))
        # palette.setColor(QPalette.Window, QColor(48,48,48))
        # palette.setColor(QPalette.Highlight, QColor(235,95,52))
        # # palette.setColor(QPalette.HighlightText, QColor(0,0,0))
        # self.menu.setPalette(palette)
        # # apply rounding mask.
        # roundingPath = QPainterPath()
        # self.menu.popup(event.globalPos())
        # roundingPath.addRoundedRect(QRectF(self.menu.rect()), 15, 15)
        # mask = QRegion(roundingPath.toFillPolygon().toPolygon())
        # self.menu.setMask(mask)
    def alert(self, msg: str):
        self.page().runJavaScript(f"alert(`{msg}`);")

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
        self.page().setDevToolsPage(dev_view_page)

        
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

# class BrowserHistory:
#     def __init__(self, path: str=CHROME_LINUX_PATH):
#         self.history = []
#         # open chrome's browsing history file.
#         if os.path.exists(path):
#         # use custom history file
#         elif os.p
#         else:    
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


class Browser(DebugWebView):
    def __init__(self, parent: Union[None, QWidget], zoomFactor: float=1.25, window: QWidget=None):
        super(Browser, self).__init__(parent=parent)
        self.mime_database = QMimeDatabase()
        self.historyIndex = 0
        self.dash_window = window
        custom_page = CustomWebPage(
            self, search_panel=self.searchPanel, 
            logging_level=3, dash_window=window)
        self.setPage(custom_page)
        # if window is not None:
        #     self.page().connectWindow(self.dash_window)
        # self.pbar = tqdm(range(100)) 
        # self.currentZoomFactor = zoomFactor
        # self.setZoomFactor(self.currentZoomFactor)
        # self.extension_manager = ExtensionManager()
        # modify settings.
        self.progress_started = False
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        # set true if clipboard permission is granted.
        # self.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        # set true to allow spatial navigation
        # self.settings().setAttribute(QWebEngineSettings.SpatialNavigationEnabled, True)
        self.progress = 0
        self._is_bookmarked = False
        self._is_terminalized = False
        self.loadProgress.connect(self.setProgress)
        self.selectionChanged.connect(self.onSelectionChange)
        # # shortcuts.
        # self.SelectAll = QShortcut(QKeySequence.SelectAll, self)
        # self.SelectAll.activated.connect(self.selectAll)
        # self.Deselect = QShortcut(QKeySequence.Deselect, self)
        # self.Deselect.activated.connect(self.deselect)
    def onSelectionChange(self):
        selText = self.selectedText()
        selText = " ".join(selText.strip().split("\n"))
        try:
            menu = self.dash_window.menu
            menu.browser_statusbar.updateSelection(selText)
        except Exception as e:
            print("\x1b[31;1mbrowser.onSelectionChange\x1b[0m", e)
        # print(f"selection changed {self.selectedText()}")
    def setBookmark(self, status: bool):
        self._is_bookmarked = status

    def setTerminalized(self, status: bool):
        self._is_terminalized = status

    def isBookmarked(self):
        return self._is_bookmarked

    def isTerminalized(self):
        return self._is_terminalized

    def setProgress(self, progress):
        self.progress = progress
        tabBar = self.tabWidget.tabBar()
        i = self.tabWidget.currentIndex()
        # when progress is started for the first time.
        if self.progress_started == False:
            # set the progress started for first time flag.
            self.progress_started = True
            # create animation label if it doesn't exist.
            animLabel = tabBar.tabButton(i, QTabBar.LeftSide)
            if animLabel is None: animLabel = QLabel()
            # create the loading animation/movie/gif object.
            movie = QMovie(FigD.icon("tabbar/loading.gif"))
            # set the size.
            movie.setScaledSize(QSize(20,20))
            # set the movie for the label.
            animLabel.setMovie(movie)
            movie.start() # start showing the animation
            tabBar.setTabButton(i, QTabBar.LeftSide, animLabel)
        # when progress is finished.
        if progress == 100:
            # set the progress started flag to false.
            self.progress_started = False
            return 
        try:
            pass
            # self.tabWidget.setTabText(i, f"Loading {self.progress}")
            # print(f"Loaded {self.url().toString()} {self.progress}%")
            # self.pbar.update(progress-self.pbar.n)
        except Exception as e:
            print("\x1b[31;1mbrowser.setProgress\x1b[0m", e)

    def deselect(self):
        pass
    # def selectAll(self):
    #     print("select all")
    #     self.page().runJavaScript('''document.execCommand("selectAll");''')
    # def pageIconCallback(self, html: str):
    #     from bs4 import BeautifulSoup
    #     soup = BeautifulSoup(html, features="html.parser")
    #     icon_links = soup.findAll("link", **{"rel": "icon"})
    #     icon_path = None
    #     is_svg = False
    #     for icon in icon_links:
    #         icon_path = icon["href"]
    #         if icon["type"] == "image/svg+xml": 
    #             is_svg = True
    #             break
    #     if icon_path:
    #         self.pageIcon = QFetchIcon(
    #             icon_path, 
    #             is_svg
    #         )
    #         pprint(icon_path)
    def execTerminalCommand(self, cmd: str=""):
        cmd = cmd.strip()
        orig_cmd = copy.deepcopy(cmd)
        if cmd == "clear":
            self.page().runJavaScript(f"FigTerminal.clear();")            
            return
        argv = cmd.split()
        for i in range(len(argv)):
            if argv[i].startswith("$"):
                argv[i] = os.environ.get(
                    argv[i].replace("$","")
                )
        cmd = " ".join(argv)
        if argv[0] == "cd":
            path = cmd[2:].strip()
            path = os.path.expanduser(path)
            if path == ".": pass
            elif path == "..":
                path = str(pathlib.Path(os.getcwd()).parent)
                os.chdir(path)                
            else: 
                try: 
                    os.chdir(path)   
                except FileNotFoundError:
                    msg = f"bash: cd: {path}: No such file or directory"
                    self.page().runJavaScript(
                        f"FigTerminal.writeLine(`{orig_cmd}`, `{msg}`);"
                    )                    
            self.page().runJavaScript(
                f"FigTerminal.write(`{orig_cmd}`, ``);"
            )
            path = collapseuser(path)
            self.page().runJavaScript(f"FigTerminal.chdir(`{path}`);")
            return
        try:
            result = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            op_str = result.communicate()[0].decode('utf-8')
            err_str = result.communicate()[1].decode('utf-8')
            ret_code = result.returncode
            if ret_code == 0:
                self.page().runJavaScript(
                    f"FigTerminal.writeLine(`{orig_cmd}`, `{op_str}`);"
                )
            else:
                self.page().runJavaScript(
                    f"FigTerminal.writeErrorLine(`{orig_cmd}`, `{err_str}`);"
                )
        except FileNotFoundError:
            # wow: command not found
            self.page().runJavaScript(
                f"FigTerminal.writeLine(`{orig_cmd}`, `{argv[0].strip()}: command not found`);"
            )
        except Exception as e:
            self.page().runJavaScript(
                f"FigTerminal.writeLine(`{orig_cmd}`, `{e}`);"
            )
            print("\x1b[31;1mbrowser.execTerminalCommand\x1b[0m", e)

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        data = self.page().contextMenuData()
        # print(QWebEngineContextMenuData.CanCopy) 
        
        print("None:", data.mediaType() == data.MediaTypeNone)
        print("Image:", data.mediaType() == data.MediaTypeImage)
        print("Video:", data.mediaType() == data.MediaTypeVideo)
        print("Audio:", data.mediaType() == data.MediaTypeAudio)
        print("Canvas:", data.mediaType() == data.MediaTypeCanvas)
        print("Plugin:", data.mediaType() == data.MediaTypePlugin)
        print(data.selectedText())
        # this code snippet makes sure that the inspect action displays the dev tools if they are hidden.
        transToEnglish = None
        # openLinkInNewTab = None
        # actions = self.menu.actions()
        # for i, action in enumerate(actions):
        #     if action.text() == "Open link in new tab":
        #         openLinkInNewTab = actions[i]
        # # open link in new tab action.
        # if openLinkInNewTab:
        #     qurl = data.linkUrl()
        #     # print(f"open {qurl.toString()} in new tab")
        #     openLinkInNewTab.triggered.connect(
        #         lambda: self.tabs.openUrl(url=qurl)
        #     )
        # edit actions.
        for action in self.menu.actions():
            # print(action.text())
            if action.text() == "Back":
                if action.isEnabled():
                    action.setIcon(FigD.Icon("navbar/prev.svg"))
                else:
                    action.setIcon(FigD.Icon("navbar/prev_disabled.svg"))
                action.setShortcut(QKeySequence.Back)
            elif action.text() == "Undo":
                action.setShortcut(QKeySequence.Undo)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/undo.svg"))
                else:
                    action.setIcon(FigD.Icon("browser/undo_disabled.svg"))                
            elif action.text() == "Redo":
                action.setShortcut(QKeySequence.Redo)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/redo.svg"))
                else:
                    action.setIcon(FigD.Icon("browser/redo_disabled.svg"))  
            elif action.text() == "Forward":
                action.setShortcut(QKeySequence.Forward)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("navbar/next.svg"))
                else:
                    action.setIcon(FigD.Icon("navbar/next_disabled.svg"))
            elif action.text() == "Reload":
                action.setShortcut(QKeySequence.Refresh)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("navbar/reload.svg"))
                else:
                    action.setIcon(FigD.Icon("navbar/reload_disabled.svg"))
            elif action.text() == "Cut":
                action.setShortcut(QKeySequence.Cut)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/cut.svg"))
                else:
                    action.setIcon(FigD.Icon("browser/cut_disabled.svg"))
            elif action.text() == "Select all":
                action.setShortcut(QKeySequence.SelectAll)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/select_all.png"))
                else:
                    action.setIcon(FigD.Icon("browser/select_all_disabled.png"))
            elif action.text() == "Paste":
                action.setShortcut(QKeySequence.Paste)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/paste.svg"))
                else:
                    action.setIcon(FigD.Icon("browser/paste_disabled.svg"))
            elif action.text() == "Paste and match style":
                action.setShortcut(QKeySequence("Ctrl+Shift+V"))
                if action.isEnabled():
                    action.setIcon(FigD.Icon("browser/paste_and_match_style.png"))
                else:
                    action.setIcon(FigD.Icon("browser/paste_and_match_style_disabled.png"))
            elif action.text() == "Copy":
                action.setShortcut(QKeySequence.Copy)
                action.setIcon(FigD.Icon("browser/copy.svg"))
                copyLinkToHighlight = self.menu.addAction(FigD.Icon("browser/highlight.svg"), "Copy link to highlight")
                self.menu.insertAction(action, copyLinkToHighlight)
                def truncateText(text, thresh=30, num_dots=3):
                    if len(text) > 30:
                        text = text[:(30-num_dots)]+"."*num_dots
                    else: text = text
                    return text.strip()
                searchGoogleFor = self.menu.addAction(FigD.Icon("browser/google.svg"), f'Search Google for "{truncateText(data.selectedText())}"')
                self.menu.insertAction(action, searchGoogleFor)
                copyLowerCase = self.menu.addAction("Copy lower case")
                self.menu.insertAction(action, copyLowerCase)
                copyUpperCase = self.menu.addAction("Copy upper case") 
                self.menu.insertAction(action, copyUpperCase)
                copyTitleCase = self.menu.addAction("Copy title case")
                self.menu.insertAction(action, copyTitleCase)
            elif action.text() == "Save page":
                action.setShortcut(QKeySequence.Save)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("titlebar/save.svg"))
                else:
                    action.setIcon(FigD.Icon("titlebar/save.svg"))
            elif action.text() == "View page source":
                action.setShortcut(QKeySequence("Ctrl+U"))
                if action.isEnabled():
                    action.setIcon(FigD.Icon("titlebar/source.svg"))
                else:
                    action.setIcon(FigD.Icon("titlebar/source.svg"))
        # insert actions.
        for action in self.menu.actions():
            if action.text() == "Save page":
                # print("adding print action")
                printAction = self.menu.addAction(FigD.Icon("titlebar/print.svg"), "Print", print, shortcut=QKeySequence("Ctrl+P"))
                self.menu.insertAction(action, printAction)
                break
        for action in self.menu.actions():
            if data.mediaType() == data.MediaTypeImage:
                if action.text() in ["Back", "Forward", "Reload", "Print", "Save page"]:
                    action.setVisible(False)
            # elif data.mediaType() == data.MediaTypeNone:
            else:
                if action.text() in ["Back", "Forward", "Reload", "Print", "Save page"]:
                    action.setVisible(True)
        # open link in new tab, window, incognito window for image media type.
        if data.mediaType() == data.MediaTypeImage:
            for action in self.menu.actions():
                if action.text() == "Save image": break
            openLinkInNewTab = self.menu.addAction("Open link in new  tab")
            openLinkInNewWindow = self.menu.addAction("Open link in new window")
            openLinkInIncognitoWindow = self.menu.addAction("Open link in incognito window")
            self.menu.insertAction(action, openLinkInIncognitoWindow)
            self.menu.insertAction(openLinkInIncognitoWindow, openLinkInNewWindow)
            self.menu.insertAction(openLinkInNewWindow, openLinkInNewTab)
            self.menu.insertSeparator(action)
            copyLinkAddress = self.menu.addAction("Copy link address")
            saveLinkAs = self.menu.addAction("Save link as...")
            self.menu.insertAction(action, copyLinkAddress)
            self.menu.insertAction(copyLinkAddress, saveLinkAs)
            self.menu.insertSeparator(action)
            action.setText("Save image as...")
            # self.menu.addSeparator(action)
        # get the inspect action
        inspectAction = self.menu.actions()[-1]
        # verify that it is in fact the Inspect action.
        if inspectAction.text() == "Inspect":
            # create a new action that trigger the Inspect action after opening dev tools if not opened.
            wrappedInspectAction = self.menu.addAction("Inspect")
            wrappedInspectAction.setShortcut(QKeySequence("Ctrl+Shift+I"))
            if wrappedInspectAction.isEnabled():
                wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
            else:
                wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
            wrappedInspectAction.triggered.connect(
                lambda: inspectTriggered(
                    browser=self,
                    inspect_action=inspectAction,
                )
            )
            # hide original inspect action.
            inspectAction.setVisible(False)
        palette = self.menu.palette()
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128,128,128))
        palette.setColor(QPalette.Base, QColor(48,48,48,255))
        palette.setColor(QPalette.Text, QColor(125,125,125))
        palette.setColor(QPalette.Window, QColor(48,48,48,255))
        palette.setColor(QPalette.WindowText, QColor(255,255,255,255))
        palette.setColor(QPalette.ButtonText, QColor(255,255,255))
        # gradient = QLinearGradient(QPointF(0,0), QPointF(50,100))
        # gradient = QGradient(QGradient.YoungPassion)
        # gradient.setColorAt(0, QColor(161,31,83))
        # gradient.setColorAt(1, QColor(91,54,54))
        # gradient.setColorAt(2, QColor(235,95,52))
        palette.setColor(QPalette.Highlight, QColor(235,95,52,90))
        # palette.setColor(QPalette.Highlight, QColor(235,95,52))
        # palette.setColor(QPalette.HighlightedText, QColor(29,29,29,255))
        self.menu.setPalette(palette)
        # self.menu.palette().setBackground(
        #     QColor(29,29,29)
        # )
        # self.menu.setStyleSheet("background: #292929; color: #fff;")
        font = QFont("Be Vietnam Pro", 10)
        self.menu.setFont(font)
        self.menu.addSeparator()
        if data.mediaType() == data.MediaTypeNone:  
            shareToDevice = self.menu.addAction(FigD.Icon("system/fileviewer/devices.svg"), "Send to your devices")
            self.menu.addAction(FigD.Icon("qrcode.svg"), "Create QR code for this page")
        elif data.mediaType() == data.MediaTypeImage:
            self.menu.addAction(FigD.Icon("qrcode.svg"), "Create QR code for this page")
            shareToDevice = self.menu.addAction(FigD.Icon("system/fileviewer/devices.svg"), "Send link to your devices")
        # browser/copy_link_to_highlight.svg
        if data.mediaType() == data.MediaTypeNone:
            # highighting features.
            highlightAction = self.menu.addAction(FigD.Icon("browser/copy_link_to_highlight.svg"), "Highlight selected text")
            self.menu.addSeparator()
            highlightAction.triggered.connect(self.highlightSelectedText)
            # translate webpage to English.
            transToEnglish = self.menu.addAction(FigD.Icon("trans.svg"), "Translate to English")
            transToEnglish.triggered.connect(
                lambda: self.page().translate(target_lang="en")
            )
        if data.mediaType() == data.MediaTypeNone:  
            searchImageGoogleLens = self.menu.addAction(FigD.Icon("browser/google_lens.png"), "Search images with Google Lens") 
            castToTv = self.menu.addAction(FigD.Icon("browser/cast.svg"), "Cast")  
        elif data.mediaType() == data.MediaTypeImage:
            searchImageGoogleLens = self.menu.addAction(FigD.Icon("browser/google_lens.png"), "Search image with Google Lens") 
        # profile = self.page().profile()
        # languages = profile.spellCheckLanguages()
        # menu = self.page().createStandardContextMenu()
        # menu.setParent(self)
        # menu.addSeparator()

        # spellcheckAction = QAction(self.tr("Check Spelling"), None)
        # spellcheckAction.setCheckable(True)
        # spellcheckAction.setChecked(profile.isSpellCheckEnabled())
        # spellcheckAction.toggled.connect(profile.setSpellCheckEnabled)
        # menu.addAction(spellcheckAction)
        # if profile.isSpellCheckEnabled():
        #     subMenu = menu.addMenu(self.tr("Select Language"))
        #     for key, lang in self.m_spellCheckLanguages.items():
        #         action = subMenu.addAction(key)
        #         action.setCheckable(True)
        #         action.setChecked(lang in languages)
        #         action.triggered.connect(partial(self.on_spell_check, lang))
        # menu.aboutToHide.connect(menu.deleteLater)
        # menu.popup(event.globalPos())

        # print(f"context menu has {len(self.menu.actions())} actions")
        # self.menu.actions()[0].setIcon(FigD.Icon("qrcode.svg"))
        # highlight action.
        self.menu.popup(event.globalPos())
   
    def prevInHistory(self):
        self.back()
        # try:
        #     if self.history().canGoBack():
        #         self.dash_window.navbar.prevBtn.setEnabled(True)
        #     else:
        #         self.dash_window.navbar.prevBtn.setEnabled(False)
        # except Exception as e:
        #     print(f"\x1b[31;1mbrowser.prevInHistory:\x1b[0m", e)
    def nextInHistory(self):
        self.forward()
        # try:
        #     if self.history().canGoForward():
        #         self.dash_window.navbar.nextBtn.setEnabled(True)
        #     else:
        #         self.dash_window.navbar.nextBtn.setEnabled(False)
        # except Exception as e:
        #     print(f"\x1b[31;1mbrowser.prevInHistory:\x1b[0m", e)

    def load(self, url):
        '''redefined load function which shows url being loaded on status bar.'''
        # print(f"\x1b[33;1mloading {url}\x1b[0m")
        self.dash_window.statusBar().showMessage(f"loading {url.toString()}")
        super(DebugWebView, self).load(url)

    def dragEnterEvent(self, e):
        from pathlib import Path
        from pprint import pprint

        mimeData = e.mimeData()
        print(mimeData.formats())
        filename = mimeData.text().strip()
        filename = filename.replace("file://", "")
        mimetype = self.mime_database.mimeTypeForFile(filename).name()
        print(f"dragEvent for {'folder' if os.path.isdir(filename) else 'file'}: {filename}, with mimetype: {mimetype}")
        if os.path.isdir(filename):
            # case when item being opened is actually a folder.
            self.dash_window.tabs.openWidget(
                widget=self.dash_window.menu.fileviewer,
                icon=FigD.Icon("system/fileviewer/folder.svg"),
                title=filename, 
            )
            self.dash_window.menu.fileviewer.connectWindow(self.dash_window)
            self.dash_window.menu.fileviewer.open(filename)
        else:
            # if mimetype == "application/octet-stream":
            #     import urllib.parse
            #     # url = urllib.parse.urlencode(filename)
            #     url = QUrl(filename)
            #     print(filename, url.toString())
            #     self.dash_window.tabs.loadUrl(filename)
            super(Browser, self).dragEnterEvent(e)

    def changeUserAgent(self):
        try:
            userAgentStr = "Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0" 
            # userAgentStr = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
            self.page().profile().setHttpUserAgent(userAgentStr)
            # print("changed user agent.")
        except Exception as e:
            print("\x1b[31;1mbrowser.changeUserAgent\x1b[0m", e)

    def updateTabTitle(self):
        try:
            # self.searchPanel.closePanel()
            self.dash_window.navbar.searchbar.setText(
                self.url().toString(QUrl.FullyEncoded)
            )
            self.dash_window.statusBar().clearMessage()
            # print(f"\x1b[33murlChanged({self.url().toString()})\x1b[0m")
        except AttributeError as e:
            print(f"\x1b[31;1mbrowser.updateTabTitle:\x1b[0m {e}")
        try:
            # change title of the tab that contains this browser only.
            currentWidget =  self.tabWidget.currentWidget()
            if currentWidget is None: return 
            if self != currentWidget.browser: return
            i = self.tabWidget.currentIndex()
            if i < 0: return
            navbar = self.dash_window.navbar
            navbar.reloadBtn.setStopMode(True)
            # print(f"\x1b[33mscheduling setupTabForBrowser for urlChanged({self.url().toString()})\x1b[0m")
            self.page().loadFinished.connect(
                lambda: self.tabWidget.setupTabForBrowser(
                    i=i, browser=self,
                )
            )
        except AttributeError as e:
            print(f"\x1b[31;1mbrowser.updateTabTitle:\x1b[0m {e}")
            # print("not connected to a TabWidget")
    def setUrl(self, url):
        self.dash_window.statusBar().showMessage(f"loading {url.toString()}")
        super(Browser, self).setUrl(url)

    def setWordCount(self):
        code = '''
        function calculateWordCount(text) {
            const wordsArr = text.trim().split(" ")
            return wordsArr.filter(word => word !== "").length
        }
        calculateWordCount(document.body.textContent);
        '''
        self.page().runJavaScript(code, self._word_count_callback)

    def _word_count_callback(self, word_count: int):
        try:
            self.dash_window.page_info.update(word_count)
        except AttributeError as e:
            print(f"\x1b[31;1mbrowser._word_count_callback:\x1b[0m {e}")
            # print("TabWidget not connected to DashWindow") 
    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget 
        self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
        self.CtrlPlus.activated.connect(tabWidget.zoomInTab)
        self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)
        self.CtrlMinus.activated.connect(tabWidget.zoomOutTab)
        self.urlChanged.connect(self.updateTabTitle)
        try: 
            self.titlebar = self.dash_window.titlebar
            print("self.titlebar =", self.titlebar)
            self.dash_window = tabWidget.dash_window
            self.dash_window.statusBar().addWidget(self.statusbar)
        except AttributeError as e:
            print(f"\x1b[31;1mbrowser.connectTabWidget:\x1b[0m {e}")
            # print("TabWidget not connected to DashWindow") 
    def highlightSelectedText(self):
        '''highlight selected text by using the highlightSelection() function.'''
        print("\x1b[33;1mhighlighting selected text\x1b[0m")
        self.page().runJavaScript("highlightSelection()")
        print("selected text:", self.selectedText())

    def execAnnotationJS(self):
        '''execute javascript needed for annotation shit'''
        self.page().runJavaScript(WEBPAGE_ANNOT_JS)

    def execTerminalJS(self):
        '''execute javascript needed for running terminal related shit'''
        self.page().runJavaScript(WEBPAGE_TERMINAL_JS)

    def setScrollbar(self, style: str=scrollbar_style):
        code = f'''Style = `{scrollbar_style}`
newScrollbarStyle = document.createElement('style');
newScrollbarStyle.innerHTML = Style
document.head.appendChild(newScrollbarStyle);'''
        self.page().runJavaScript(code)

    def setSelectionStyle(self, style: str=selection_style):
        code = f'''Style = `{style}`
newSelectStyle = document.createElement('style');
newSelectStyle.innerHTML = Style
document.head.appendChild(newSelectStyle);
'''
        self.page().runJavaScript(code)

    # def drop

    def iconSetCallback(self, html: str):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, features="html.parser")
        icon_links = soup.findAll("link", **{"rel": "icon"})
        icon_path, is_svg = None, False
        for icon in icon_links:
            icon_path = icon["href"]
            if icon.get("type")=="image/svg+xml": is_svg = True; break
        if icon_path:
            try:
                pageIcon = QFetchIcon(icon_path, is_svg)
            except MissingSchema:
                pageIcon = FigD.Icon("browser.svg")
            except InvalidSchema:  
                pageIcon = QIcon(icon_path.replace("file://",""))
        else:
            pageIcon = FigD.Icon("browser.svg")
        
        tabBar = self.tabWidget.tabBar()
        animLabel = tabBar.tabButton(self.i, QTabBar.LeftSide)
        if animLabel is None: animLabel = QLabel()
        
        print("\x1b[34;1msetting pixmap\x1b[0m")
        self.pagePixmap = pageIcon.pixmap(QSize(20,20))
        self.pagePixmap.save("DELETE_THIS_BROWSER_PIXMAP.png")
        # print("pixmap:", animLabel.pixmap())
        # print("movie:", animLabel.movie())
        animLabel.setPixmap(self.pagePixmap)
        tabBar.setTabButton(self.i, QTabBar.LeftSide, animLabel)
        # self.tabs.setTabIcon(self.i, pageIcon)
    def setIcon(self, tabs, i: int):
        self.i = i
        self.tabs = tabs
        self.page().toHtml(self.iconSetCallback)

    def terminalize(self):
        rendered = TermViewerHtml.render(
            TERM_VIEWER_JS=TermViewerJS,
            TERM_VIEWER_CSS=TermViewerCSS,
        )
        self.setTerminalized(True)
        url = FigD.createTempUrl(rendered)
        self.load(QUrl(url))

    def unterminalize(self):
        self.setTerminalized(False)
        self.back()
# class MainWindow(QWidget):
#     def __init__(self, parent=None):
#         super(QWidget, self).__init__(parent)
#         self.defaultUrl = QUrl()


#         toolbar = self.addToolBar("")
#         toolbar.addWidget(self.urlLe)
#         toolbar.addWidget(self.favoriteButton)

#         self.addToolBarBreak()
#         self.bookmarkToolbar = BookmarkBar()
#         self.bookmarkToolbar.bookmarkClicked.connect(self.add_new_tab)
#         self.addToolBar(self.bookmarkToolbar)
#         self.readSettings()

#     def onReturnPressed(self):
#         self.tabs.currentWidget().setUrl(QUrl.fromUserInput(self.urlLe.text()))

#     def addFavoriteClicked(self):
#         loop = QtCore.QEventLoop()

#         def callback(resp):
#             setattr(self, "title", resp)
#             loop.quit()

#         web_browser = self.tabs.currentWidget()
#         web_browser.page().runJavaScript("(function() { return document.title;})();", callback)
#         url = web_browser.url()
#         loop.exec_()
#         self.bookmarkToolbar.addBookmarkAction(getattr(self, "title"), url)

#     def add_new_tab(self, qurl=QUrl(), label='Blank'):
#         web_browser = QtWebEngineWidgets.QWebEngineView()
#         web_browser.setUrl(qurl)
#         web_browser.adjustSize()
#         web_browser.urlChanged.connect(self.updateUlrLe)
#         index = self.tabs.addTab(web_browser, label)
#         self.tabs.setCurrentIndex(index)
#         self.urlLe.setText(qurl.toString())

#     def updateUlrLe(self, url):
#         self.urlLe.setText(url.toDisplayString())

#     def readSettings(self):
#         settings = QtCore.QSettings()
#         self.defaultUrl = settings.value("defaultUrl", QUrl('http://www.google.com'))
#         self.add_new_tab(self.defaultUrl, f'Hello {getpass.getuser()}!')
#         bookmarks = settings.value("bookmarks", [])
#         if bookmarks is None: bookmarks = []
#         # print(settings.value("bookmarks", []))
#         self.bookmarkToolbar.setBookmarks(bookmarks)

#     def saveSettings(self):
#         settings = QtCore.QSettings()
#         settings.setValue("defaultUrl", self.defaultUrl)
#         settings.setValue("bookmarks", self.bookmarkToolbar.bookmark_list)

#     def closeEvent(self, event):
#         self.saveSettings()
#         super(MainWindow, self).closeEvent(event)
class HomePageView(Browser):
    # def dragEnterEvent(self, e):
    #     e.ignore()
    pass

class ChromeBrowserContainer:
    pass


def test_page_info():
    FigD("/home/atharva/GUI/fig-dash/resources")
    import sys
    app = QApplication(sys.argv)
    page_info = PageInfo()
    page_info.show()
    app.exec()


if __name__ == "__main__":
    test_page_info()