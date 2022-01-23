#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
from pprint import pprint
from typing import Union, Tuple
from requests.exceptions import MissingSchema
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QMimeDatabase, Qt, QUrl, QSize, QPoint
from PyQt5.QtWidgets import QToolBar, QToolButton, QSplitter, QLabel, QWidget, QAction, QVBoxLayout, QHBoxLayout, QApplication, QSizePolicy, QGraphicsDropShadowEffect, QLineEdit, QTextEdit, QPlainTextEdit, QShortcut
# fig_dash
from ..utils import QFetchIcon
from fig_dash.assets import FigD
from fig_dash.api.browser.extensions import ExtensionManager

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
#fig_webpage_annotation_context_menu {
    color: #fff;
    font-weight: bold;
    background-color: #000;
    padding-left: 20px;
    padding-right: 20px;
}`
document.head.appendChild(style);
let annotation_context_menu = document.createElement("div");
annotation_context_menu.id = "fig_webpage_annotation_context_menu";
annotation_context_menu.innerHTML = `
<p>Change highlight color</p>
<p>Clear highlight</p>
<p>Add a note</p>
<p onclick='alert("Thank you!")'>Upvote</p>`;
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
# HOME_URL = "file:///tmp/fig_dash.rendered.content.html"
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
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(DevToolsBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(DevToolsBtn, self).leaveEvent(event)


class PyDevToolsBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, 
                size: Tuple[int, int]=(23,23)):
        super(PyDevToolsBtn, self).__init__(parent)
        self.inactive_icon = "browser/dev_tools.svg"
        self.active_icon = "browser/dev_tools_active.svg"
        self.setIcon(FigD.Icon(self.inactive_icon))
        self.setIconSize(QSize(*size))
        self.setToolTip("open python devtools")
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')


class PyDevToolsView(QWidget):
    def __init__(self):
        super(PyDevToolsView, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.execBtn = QToolButton()
        self.execBtn.setText("run")
        self.layout.addWidget(self.execBtn)

        self.input = QPlainTextEdit()
        self.input.setPlainText("input")
        self.output = QTextEdit()
        self.output.setText("output")
        self.output.setReadOnly(True)
        # bind events.
        self.execBtn.clicked.connect(self.exec)
        # self.input.returnPressed.connect(self.exec)
        self.outputHistory = []
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.output)
        self.setLayout(self.layout)
        self.setStyleSheet("""
        QLineEdit {
            color: #000;
            background: #fff;
        }
        QTextEdit {
            color: #000;
            background: #fff;
        }""")
    # def _exec(self, code: str):
    #     Vars = {}
    #     try:
    #         exec(code, globals(), Vars)
    #         Result = Vars.get('Result')
    #     except Exception as E:
    #         Result = E
    #     return Result
    def exec(self):
        code = self.input.toPlainText()
        # codeEvalOutput = str(self._exec(code))
        # self.outputHistory.append(codeEvalOutput)
        try:
            exec(code)
        except Exception as e:
            self.output.setText(str(e))


class BrowserSearchPanelBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(BrowserSearchPanelBtn, self).__init__(parent)
        icon = args.get('icon')
        if icon:
            self.inactive_icon = os.path.join(
                "system/fileviewer", icon
            )
            stem, ext = os.path.splitext(icon)
            self.active_icon = os.path.join(
                "system/fileviewer", 
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
        self.entry = QLineEdit()
        self.label = QLabel("0/0")
        self.entry.setStyleSheet("background: #fff; color: #000;")
        self.entry.setMinimumWidth(350)
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
        self.entry.setClearButtonEnabled(True)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.layout.addWidget(self.prevBtn)
        self.layout.addWidget(self.nextBtn)
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
        wrapper.setLayout(self.layout)
        wrapper.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            border-radius: 5px;
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
            FigD.Icon("system/fileviewer/case.svg")
        )
        self.matchWholeAction.setIcon(
            FigD.Icon("system/fileviewer/match_whole.svg")
        )
        self.regexAction.setIcon(
            FigD.Icon("system/fileviewer/regex.svg")
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

        tip = "search in webpage"
        self.setToolTip(tip)
        self.setStatusTip(tip)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0,0)
        shadow.setColor(QColor(235, 95, 52, 255))
    
        wrapper.setFixedHeight(60)
        wrapper.setFixedWidth(500)
        wrapper.setGraphicsEffect(shadow)

        dummy = QVBoxLayout()
        dummy.setContentsMargins(0, 0, 0, 0)
        dummy.addWidget(wrapper)
        self.setLayout(dummy)
        
    def showEvent(self, event):
        super(BrowserSearchPanel, self).showEvent(event)
        self.setFocus(True)

    def update_searching(self, direction=QWebEnginePage.FindFlag()):
        flag = direction
        # if self.case_button.isChecked():
            # flag |= QWebEnginePage.FindCaseSensitively
        self.searched.emit(self.entry.text(), flag)

    def show(self):
        print(f"\x1b[31;1mshowing: currently {self.isVisible()}\x1b[0m")
        super(BrowserSearchPanel, self).show()

    def hide(self):
        print(f"\x1b[31;1mhiding: currently {self.isVisible()}\x1b[0m")
        super(BrowserSearchPanel, self).hide()

    def closePanel(self):
        self.entry.clear()
        self.search("")
        self.hide()

    def search(self, query=None):
        if query is None:
            query = self.entry.text()
        self.browser.findText(query)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + self.x(), self.y() + self.y())
        self.oldPos = event.globalPos()

    def connectBrowser(self, browser):
        self.browser = browser

    def show(self):
        self.setParent(self.browser)
        WB = self.browser.width()
        self.move(WB/2-250, -200)
        print("display search panel")
        super(BrowserSearchPanel, self).show()


class SilentWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, *args, **kwargs):
        '''silence javascript error mesages'''
        pass


class DebugWebView(QWebEngineView):
    def __init__(self, parent=None,
                 zoomFactor=1.25, dev_tools_zoom=1.35):
        super(DebugWebView, self).__init__(parent)
        self.dev_view = QWebEngineView()
        # self.py_dev_view = PyDevToolsView()
        self.devToolsBtn = DevToolsBtn(self)
        # self.pyDevToolsBtn = PyDevToolsBtn(self)
        
        self.dev_tools_zoom = dev_tools_zoom
        self.devToolsBtn.clicked.connect(self.toggleDevTools)
        # self.pyDevToolsBtn.clicked.connect(self.togglePyDevTools)

        # current zoom factor of the main web view.
        self.currentZoomFactor = zoomFactor

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self)
        self.splitter.addWidget(self.dev_view)
        # self.splitter.addWidget(self.py_dev_view)
        self.splitter.setSizes([500, 300])
        # back reference to browser.
        self.splitter.browser = self

        self.searchPanel = BrowserSearchPanel()
        self.searchPanel.connectBrowser(self)
        self.searchPanel.move(50,50)
        # shortcuts.
        self.Esc = QShortcut(QKeySequence("Esc"), self)
        self.Esc.activated.connect(self.searchPanel.closePanel)
        # self.CtrlA = QShortcut(QKeySequence("Ctrl+A"), self)
        # self.CtrlA.activated.connect(self.selectAll)
        self.CtrlF = QShortcut(QKeySequence("Ctrl+F"), self)
        self.CtrlF.activated.connect(self.reactToCtrlF)
        self.CtrlShiftI = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
        self.CtrlShiftI.activated.connect(self.toggleDevTools)

        self.dev_view.hide()
        # self.py_dev_view.hide()
        self.dev_view.loadFinished.connect(self.setDevToolsZoom)
    # def selectAll(self):
    #     print("select all")
    #     self.page().runJavaScript('''document.execCommand("selectAll");''')
    def reactToCtrlF(self):
        # print("is browser pane in focus: ", self.hasFocus())
        self.searchPanel.show()

    def focusInEvent(self, event):
        print("entering focus")
        self.CtrlF.setEnabled(True)

    def focusOutEvent(self, event):
        print("exiting focus")
        self.CtrlF.setEnabled(False)

    def setUrl(self, url):
        self.searchPanel.closePanel()
        super(DebugWebView, self).setUrl(url)

    def load(self, url):
        self.searchPanel.closePanel()
        super(DebugWebView, self).load(url)

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        # print(dir(self.menu))
        self.menu.setStyleSheet("background: #292929; color: #fff;")
        self.menu.popup(event.globalPos())

    def alert(self, msg: str):
        self.page().runJavaScript(f"alert(`{msg}`);")

    def setDevToolsZoom(self):
        self.dev_view.setZoomFactor(self.dev_tools_zoom)

    def toggleDevTools(self):
        if self.dev_view.isVisible():
            self.dev_view.hide()
        else:
            self.dev_view.show()
        
    def togglePyDevTools(self):
        if self.py_dev_view.isVisible():
            self.py_dev_view.hide()
        else:
            self.py_dev_view.show()

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
class Browser(DebugWebView):
    def __init__(self, parent: Union[None, QWidget], zoomFactor: float=1.25):
        super(Browser, self).__init__(parent=parent)
        self.mime_database = QMimeDatabase()
        self.historyIndex = 0
        self.browsingHistory = []
        # self.currentZoomFactor = zoomFactor
        # self.setZoomFactor(self.currentZoomFactor)
        # self.extension_manager = ExtensionManager()
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
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        # print(dir(self.menu))
        self.menu.setStyleSheet("background: #292929; color: #fff;")
        self.menu.addAction(FigD.Icon("qrcode.svg"), "Create QR code for this page")
        self.menu.addAction(FigD.Icon("browser/highlight.svg"), "Highlight selected text")
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("trans.svg"), "Translate to English")
        # print(f"context menu has {len(self.menu.actions())} actions")
        # self.menu.actions()[0].setIcon(FigD.Icon("qrcode.svg"))
        # highlight action.
        self.menu.actions()[-2].triggered.connect(self.highlightSelectedText)
        self.menu.popup(event.globalPos())

    def append(self, url: Union[str, QUrl]):
        '''append url to browsing history.'''
        try: url = url.toString()
        except AttributeError as e: pass
        # store in local tab browsing history.
        if len(self.browsingHistory) > 0 and self.browsingHistory[-1] == url:
            self.browsingHistory.append(url)
            self.historyIndex = len(self.browsingHistory)-1
        try:
            if len(self.dash_window.browsingHistory) > 0 and self.dash_window.browsingHistory[-1] == url:
                return
            else:
                self.dash_window.browsingHistory.append(url)
                print(f"\x1b[31;1m{self.dash_window.browsingHistory}\x1b[0m")
        except AttributeError as e:
            print("not connected to a DashWindow")
            return    

    def prevInHistory(self):
        self.historyIndex -= 1
        self.historyIndex = max(0, self.historyIndex)
        self.back()

    def nextInHistory(self):
        self.historyIndex += 1
        self.historyIndex = min(len(self.browsingHistory)-1, self.historyIndex)
        self.forward()

    def load(self, url):
        '''redefined load function which shows url being loaded on status bar.'''
        # print(f"\x1b[33;1mloading {url}\x1b[0m")
        self.dash_window.statusBar().showMessage(f"loading {url.toString()}")
        super(DebugWebView, self).load(url)

    def dragEnterEvent(self, e):
        from pathlib import Path
        from pprint import pprint

        filename = e.mimeData().text().strip()
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
            super(Browser, self).dragEnterEvent(e)

    def changeUserAgent(self):
        # print("changing user agent.")
        try:
            self.page().profile().setHttpUserAgent(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
            )
            # print("changed user agent.")
        except Exception as e:
            print(e) 

    def updateTabTitle(self):
        try:
            self.dash_window.navbar.searchbar.setText(
                self.url().toString()
            )
            self.dash_window.statusBar().clearMessage()
        except AttributeError as e:
            print("not connected to DashWindow") 
        self.append(self.url())
        try:
            # change title ofthe tab that contains this browser only.
            if self != self.tabWidget.currentWidget(): return
            i = self.tabWidget.currentIndex()
            if i < 0: return
            print(f"updating title for tab-{i}")
            self.loadFinished.connect(
                lambda: self.tabWidget.setupTabForBrowser(
                    i=i, browser=self,
                )
            )
        except AttributeError as e:
            print("not connected to a TabWidget")

    def setUrl(self, url):
        self.append(url)
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
            print("TabWidget not connected to DashWindow") 

    def connectTabWidget(self, tabWidget):
        self.tabWidget = tabWidget 
        self.CtrlPlus = QShortcut(QKeySequence.ZoomIn, self)
        self.CtrlPlus.activated.connect(tabWidget.zoomInTab)
        self.CtrlMinus = QShortcut(QKeySequence.ZoomOut, self)
        self.CtrlMinus.activated.connect(tabWidget.zoomOutTab)
        self.urlChanged.connect(self.updateTabTitle)
        try: self.dash_window = tabWidget.dash_window
        except AttributeError as e:
            print("TabWidget not connected to DashWindow") 

    def highlightSelectedText(self):
        '''highlight selected text by using the highlightSelection() function.'''
        print("\x1b[33;1mhighlighting selected text\x1b[0m")
        self.page().runJavaScript("highlightSelection()")

    def execAnnotationJS(self):
        '''execute javascript needed for annotation shit'''
        self.page().runJavaScript(WEBPAGE_ANNOT_JS)

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
        else:
            pageIcon = FigD.Icon("browser.svg")
        self.tabs.setTabIcon(self.i, pageIcon)

    def setIcon(self, tabs, i: int):
        self.i = i
        self.tabs = tabs
        self.page().toHtml(self.iconSetCallback)
    # def fetchIcon(self):
    #     self.page().toHtml(self.pageIconCallback)
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
    def dragEnterEvent(self, e):
        e.ignore()


def test_page_info():
    FigD("/home/atharva/GUI/fig-dash/resources")
    import sys
    app = QApplication(sys.argv)
    page_info = PageInfo()
    page_info.show()
    app.exec()


if __name__ == "__main__":
    test_page_info()