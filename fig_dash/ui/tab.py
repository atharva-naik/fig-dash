#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import jinja2
import getpass
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon, QColor, QKeySequence, QMouseEvent
from PyQt5.QtCore import pyqtSignal, QFileInfo, Qt, QPoint, QMimeDatabase, QUrl, QSize, QBuffer, QIODevice, QEvent, QObject
from PyQt5.QtWebEngineWidgets import QWebEngineHistoryItem, QWebEnginePage
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QFileIconProvider, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QTabBar, QPushButton, QShortcut, QGraphicsDropShadowEffect, QInputDialog, QFileDialog
# fig-dash imports.
from ..utils import collapseuser
from fig_dash.assets import FigD
from fig_dash.ui.browser import Browser, HomePageView

scrollbar_style = '''*::-webkit-scrollbar {
    width: 10px;
    height: 7px;
}    
*::-webkit-scrollbar-track {
    background-color: rgba(235, 235, 235, 0.1);
}

*::-webkit-scrollbar-thumb {
    background-color: #292929;
}
*::-webkit-scrollbar-thumb:hover {
    background-color: #FF0082;
}
*::-webkit-scrollbar-corner {
    background-color: transparent;
    /* background: rgba(235, 235, 235, 0.1); */
}'''
class TabsSearchDropdown(QWidget):
    def __init__(self, btn):
        super(TabsSearchDropdown, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Popup)
        self.btn = btn
        layout = QVBoxLayout()
        
        self.setObjectName("TabsSearchDropdown")
        self.searchbar = self.initSearchBar()
        layout.addWidget(self.searchbar)
        layout.addWidget(QLabel("this is something"))
        self.setLayout(layout)
        # self.setFixedWidth(300)
    def toggle(self):
        if self.isVisible(): self.hide()
        else: self.show()
    # def initPos(self, width: int, offset: int=200):
    #     geo = self.geometry()
    #     pos = self.btn.pos()
    #     w, h = geo.width(), geo.height()
    #     x, y = pos.x()+width-offset, pos.y()+h/2
    #     print(f"setGeometry({x}, {y}, {w}, {h})")
    #     self.setGeometry(x, y, w, h)
    # def rePos(self, width: int, offset: int=200):
    #     geo = self.geometry()
    #     pos = self.btn.pos()
    #     w, h = geo.width(), geo.height()
    #     x, y = pos.x()-180, pos.y()+h/2
    #     # print(f"setGeometry({x}, {y}, {w}, {h})")
    #     self.setGeometry(x, y, w, h)
    def initSearchBar(self):
        searchbar = QLineEdit(self)
        searchAction = QAction()
        searchAction.setIcon(FigD.Icon("tabbar/search.svg"))
        searchbar.addAction(searchAction)

        return searchbar

    def Show(self):
        self.show()
    # def Move(self, x: int, y: int):
    #     self.setGeometry(x-100, y+100, 100, 100)
tab_btn_style = jinja2.Template('''
QToolButton {
    border: 0px;
    border-radius: 15px;
}
QToolButton:hover {
    background: rgba(125, 125, 125, 0.7);
}''')
class TabsSearchBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabsSearchBtn, self).__init__(parent)
        self.setObjectName("TabsSearchBtn")
        self.dropdown = TabsSearchDropdown(btn=self)
        self.clicked.connect(self.dropdown.toggle)
        self.setIcon(FigD.Icon("tabbar/dropdown.svg"))
        self.setStyleSheet(tab_btn_style.render())
    #     contextMenu = self.initDropdown()
    #     contextMenu.exec_(self.mapToGlobal(event.pos()))        
    # def contextMenuEvent(self, event):
    #     contextMenu = QMenu(self)
    #     quitAct = contextMenu.addAction("Close Search")
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAct:
    #         self.close()
class TabPlusBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabPlusBtn, self).__init__(parent)
        self.setObjectName("TabPlusBtn")
        self.setIcon(FigD.Icon("tabbar/new_tab.svg"))
        self.setStyleSheet(tab_btn_style.render()) 


class TabSplitVBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabSplitVBtn, self).__init__(parent)
        self.setObjectName("TabSplitVBtn")
        self.setIcon(FigD.Icon("tabbar/tab_split_v.svg"))
        self.setStyleSheet(tab_btn_style.render())    


class TabSplitHBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabSplitHBtn, self).__init__(parent)
        self.setObjectName("TabSplitHtn")
        self.setIcon(FigD.Icon("tabbar/tab_split_h.svg"))
        self.setStyleSheet(tab_btn_style.render())    


class TabCornerWidget(QWidget):
    def __init__(self, parent: Union[None, QWidget]):
        super(TabCornerWidget, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        # self.layout.setSpacing(0)
        # self.layout.addStretch(1)
        self.dropdownBtn = TabsSearchBtn(self)
        self.dropdown = self.dropdownBtn.dropdown
        self.plusBtn = TabPlusBtn(self)
        self.splitHBtn = TabSplitHBtn(self)
        self.splitVBtn = TabSplitVBtn(self)

        self.layout.addWidget(self.initBlank())
        self.layout.addWidget(self.plusBtn)
        self.layout.addWidget(self.splitHBtn)
        self.layout.addWidget(self.splitVBtn)
        self.layout.addWidget(self.dropdownBtn)
        self.layout.addWidget(self.initBlank())
        # self.layout.addStretch(1)
        self.setLayout(self.layout)

    def initBlank(self):
        btn = QToolButton(self)
        btn.setStyleSheet('''
        QToolButton {
            border: 0px;
            color: transparent;
        }''')
        btn.setMaximumWidth(5)

        return btn


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


dash_tab_widget_style = jinja2.Template('''
QTabWidget {
    background: #292929;
}
QTabWidget::pane {
    border: 0px;
}''')
class DashTabWidget(QTabWidget):
    def __init__(self, parent: Union[None, QWidget]):
        self.mimetype_db = QMimeDatabase()
        super(DashTabWidget, self).__init__(parent)
        # tab corner widget.
        tabCornerWidget = TabCornerWidget(self)
        tabCornerWidget.splitHBtn.clicked.connect(self.HSplitCurrentTab)
        tabCornerWidget.splitVBtn.clicked.connect(self.VSplitCurrentTab)
        self.dropdownBtn = tabCornerWidget.dropdownBtn
        self.dropdown = tabCornerWidget.dropdown
        self.plusBtn = tabCornerWidget.plusBtn
        self.plusBtn.clicked.connect(lambda: self.openUrl())
        self.icon_provider = QFileIconProvider()
        # list of zoom factors.
        self.zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
        self.zoomFactors = [ZoomFactor(zf) for zf in self.zoomFactors]
        self.tabbar = TabBar()
        self.setTabBar(self.tabbar)
        self.tabbar.tabs = self

        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.setDocumentMode(False)
        self.currentChanged.connect(self.onTabChange)
        self.tabCloseRequested.connect(self.removeTab)
        self.setMovable(True)
        self.setCornerWidget(tabCornerWidget)
        self.setObjectName("DashTabWidget")
        self.setStyleSheet(dash_tab_widget_style.render())
        self.tabIcons = []
        # keyboard shortcuts.
        self.CtrlW = QShortcut(QKeySequence("Ctrl+W"), self)
        self.CtrlW.activated.connect(lambda: self.removeTab(self.currentIndex()))
        # print(dash_tab_widget_style.render())
    def partialConnectWindow(self, window):
        self.dash_window = window

    def eventFilter(self, obj: QObject, event:  QEvent):
        """[summary]

        Args:
            obj (QObject): [description]
            event (QEvent): [description]

        Returns:
            [type]: [description]
        """
        if (obj != self.tabBar()):
            return super(DashTabWidget, self).eventFilter(obj, event)
        if (event.type() != QEvent.MouseButtonPress):
            return super(DashTabWidget, self).eventFilter(obj, event)
        # compute the tab number.
        mouseEvent = QMouseEvent(event)
        pos: QPoint = mouseEvent.pos()
        count = self.tabBar().count()
        clickedItem = -1
        for i in range(count):
            if self.tabBar().tabRect(i).contains(pos):
                clickedItem = i
                break
        # just in case.
        if clickedItem == -1:
            return super(DashTabWidget, self).eventFilter(obj, event)
        print(clickedItem)
        if mouseEvent.button() == Qt.LeftButton:
            return super(DashTabWidget, self).eventFilter(obj, event)
        elif mouseEvent.button() == Qt.RightButton:
            return self.onTabRightClick()
        elif mouseEvent.button() == Qt.MidButton:
            return super(DashTabWidget, self).eventFilter(obj, event)
        else:
            return super(DashTabWidget, self).eventFilter(obj, event)            

    def onTabRightClick(self):
        print("tab right click!")

    def printPage(self):
        browser = self.currentWidget().browser
        try:
            page = browser.page()
            page.printRequested.emit()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.viewSource:\x1b[0m {e}")


    def viewSource(self):
        browser = self.currentWidget().browser
        try:
            page = browser.page()
            page.action(QWebEnginePage.ViewSource).trigger()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.viewSource:\x1b[0m {e}")

    def toggleTabBar(self) -> None:
        """[summary]
        actually topbar is toggled. 
        This function is called toggleTabBar because the topbar is what a normal browser would have as a tabbar.
        """
        try:
            topbar = self.dash_window.topbar
            if topbar.isVisible(): 
                topbar.hide()
            else: topbar.show()
        except Exception as e:
            print(f"\x1b[31;1mtab.toggleTabBar:\x1b[0m {e}")

    def connectWindow(self, window):
        self.dash_window = window

    def onTabChange(self, i: int):
        try: 
            dash_window = self.dash_window
            browser = self.widget(i).browser
            dash_window.navbar.searchbar.setUrl(browser.url())
            if browser.history().canGoBack():
                dash_window.navbar.prevBtn.setEnabled(True)
            else: 
                dash_window.navbar.prevBtn.setEnabled(False)
            if browser.history().canGoForward():
                dash_window.navbar.nextBtn.setEnabled(True)
            else: 
                dash_window.navbar.nextBtn.setEnabled(False)
            # dash_window.menu.browsermenu.devToolsBtn = browser.devToolsBtn
        except AttributeError as e: 
            print("\x1b[31;1mtab.onTabChange:\x1b[0m", e)

    def triggerFind(self):
        '''trigger the default response of the browser to Ctrl+F'''
        try: 
            debug_web_view_splitter = self.currentWidget()
            debug_web_view_splitter.browser.reactToCtrlF()
        except Exception as e: 
            print(f"\x1b[31;1mtab.triggerFind:\x1b[0m {e}")

    def connectDropdown(self, splitter):
        splitter.addWidget(self.dropdown)
        self.splitter = splitter
        self.dropdown.hide()

    def setupTabForBrowser(self, i: int, browser, 
                           lang: str="en-US"):
        try: dash_window = self.dash_window
        except AttributeError as e: 
            print(f"\x1b[31;1mtab.setupTabForBrowser:\x1b[0m {e}")
            return
        browser.page().printRequested.connect(
            browser.onPrintRequest
        )
        browser.loadDevTools()
        browser.setSpellCheck(lang)
        self.setTabText(i, "  "+browser.page().title())
        # print(f"\x1b[34mupdated tab title for urlChanged({browser.url().toString()})\x1b[0m")
        browser.page().linkHovered.connect(self.showLinkOnStatusBar)
        browser.setZoomFactor(browser.currentZoomFactor)
        if browser.history().canGoBack():
            self.dash_window.navbar.prevBtn.setEnabled(True)
        else:
            self.dash_window.navbar.prevBtn.setEnabled(False)
        if browser.history().canGoForward():
            self.dash_window.navbar.nextBtn.setEnabled(True)
        else:
            self.dash_window.navbar.nextBtn.setEnabled(False)
        if browser.isTerminalized():
            browser.execTerminalJS()
        else:
            browser.changeUserAgent()
            browser.execAnnotationJS()
            browser.setWordCount()
            browser.setIcon(tabs=self, i=i)
            dash_window.navbar.searchbar.setUrl(browser.url())
        self._tab_tooltip_setter_data = (browser, i)
        # browser.setSelectionStyle()
        # browser.setScrollbar(scrollbar_style)
        browser.page().runJavaScript(
            "document.body.outerHTML",
            self._tab_tooltip_setter,
        )

    def _tab_tooltip_setter(self, rendered_html):
        i = self._tab_tooltip_setter_data[1]
        browser = self._tab_tooltip_setter_data[0]
        # screenshot = self.screen().grabWindow(browser.winId())
        screenshot = browser.getPageScreenshot()
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
        <div style='text-align: center'>
            <h3 style='font-weight: bold;'>{browser.page().title()}</h3> 
            <br>
            <span style='color: #6e6e6e;'>{browser.url().host()}</span>
        </div>
        <br>
        <img src="data:image/png;base64,{bytes(encoded).decode()}">
        """
        # print(tabToolTip)
        self.setTabToolTip(i, tabToolTip)

    def HSplitCurrentTab(self):
        currentSplitter = self.currentWidget()
        qurl = currentSplitter.browser.url()
        url = qurl.toString()
        browser = Browser(self, window=self.dash_window)
        browser.connectTabWidget(self)
        browser.setUrl(qurl)
        i = self.addTab(browser.splitter, FigD.Icon("browser.svg"), "  "+url.strip())
        self.setTabText(i, "  "+url.strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )
        currentSplitter.addWidget(browser)

        return browser.page()
        # self.setCurrentIndex(i)
    def VSplitCurrentTab(self):
        pass

    def showLinkOnStatusBar(self, link):
        try:
            self.dash_window.statusBar().show()
            self.dash_window.statusBar().showMessage(link)
        except Exception as e:
            print(f"\x1b[31;1mtab.showLinkOnStatusBar:\x1b[0m {e}")

    def renameCurrentTab(self, text):
        i = self.currentIndex()
        self.setTabText(i, text)

    def renameDialog(self, i: Union[int, None]):
        '''initiate an input dialog to rename the current tab.'''
        if i is None: i = self.currentIndex()
        currentText = self.tabText(i).strip()
        newText, done = QInputDialog.getText(self.tabBar(), f"Rename tab '{currentText}'", f"Rename tab from {currentText} to", QLineEdit.Normal, "New Name")
        if done:
            self.setTabText(i, newText)

    def home(self):
        currentWidget = self.currentWidget()
        try:
            self.dash_window.navbar.setFocus()
        except Exception as e:
            print("\x1b[31;1mtab.home:\x1b[0m", e)
        try:
            currentWidget.browser.load(
                FigD.static(
                    "home.html",
                    USERNAME=getpass.getuser(),
                    HOME_CSS=FigD.staticUrl("home.css"),
                    CAROUSEL_JS=FigD.staticUrl("carousel.js"),
                    CAROUSEL_CSS=FigD.staticUrl("carousel.css"),
                )
            )
        except AttributeError as e: 
            print(f"\x1b[31;1mtab.home:\x1b[0m {e}")

    def openHome(self):
        url=FigD.static(
            "home.html",
            USERNAME=getpass.getuser(),
            HOME_CSS=FigD.staticUrl("home.css"),
            HOME_ICON="file:///home/atharva/GUI/fig-dash/resources/icons/logo.png",
            CAROUSEL_JS=FigD.staticUrl("carousel.js"),
            CAROUSEL_CSS=FigD.staticUrl("carousel.css"),
        ).toString()
        qurl = QUrl(url)
        browser = HomePageView(self, window=self.dash_window)
        browser.connectTabWidget(self)
        browser.setUrl(qurl)
        i = self.addTab(browser.splitter, FigD.Icon("browser.svg"), "  "+url.strip())
        try:
            self.dash_window.navbar.setFocus()
        except Exception as e:
            print("\x1b[31;1mtab.openHome:\x1b[0m", e)
        self.setTabText(i, "  "+url.strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )
        self.setCurrentIndex(i)

        return browser.page()

    def openFolder(self, folder: str):
        pass

    def terminal(self):
        '''terminalize current terminal.'''
        self.currentWidget().browser.terminalize()

    def unterminal(self):
        '''terminalize current terminal.'''
        self.currentWidget().browser.unterminalize()

    def openTerminal(self):
        self.openHome()
        self.terminal()

    def openWidget(self, widget: QWidget, 
                   title: str="", icon: str=""):
        i = self.addTab(widget, QIcon(icon), "  "+title)
        self.setCurrentIndex(i)
        try:
            browser = widget.browser
            page = browser.page()
            self._tab_tooltip_setter_data = (browser, i)
            browser.loadFinished.connect(
                lambda: page.runJavaScript(
                    "document.body.outerHTML",
                    self._tab_tooltip_setter,
                )
            )
        except Exception as e: 
            print(f"\x1b[31;1mtab.openWidget:\x1b[0m {e}")

    def openTab(self):
        browser = Browser(self, window=self.dash_window)
        browser.connectTabWidget(self)
        i = self.addTab(browser.splitter, FigD.Icon("browser.svg"), "  ")
        try:
            self.dash_window.navbar.setFocus()
        except Exception as e:
            print("\x1b[31;1mtab.openUrl:\x1b[0m", e)
        self.setCurrentIndex(i)

        return browser.page()

    def openUrl(self, url: str="file:///tmp/fig_dash.rendered.content.html"):
        if isinstance(url, str):
            qurl = QUrl(url)
        else: 
            qurl = url
            url = url.toString()
        browser = Browser(self, window=self.dash_window)
        browser.connectTabWidget(self)
        browser.setUrl(qurl)
        i = self.addTab(browser.splitter, FigD.Icon("browser.svg"), "  "+url.strip())
        try:
            self.dash_window.navbar.setFocus()
        except Exception as e:
            print("\x1b[31;1mtab.openUrl:\x1b[0m", e)
        self.setTabText(i, "  "+url.strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )
        self.setCurrentIndex(i)

        return browser.page()

    def nextUrl(self, i: int):
        currentWidget = self.currentWidget().browser
        try:
            currentWidget.nextInHistory()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.nextUrl:\x1b[0m {e}")
            print(f"tab-{i} is not a browser instance") 

    def save(self):
        print(f"\x1b[32;1msaving page using tab.DashTabWidget.save\x1b[0m")
        browser = self.currentWidget().browser
        try:
            page = browser.page()
            print(page.save(page.title()+".html"))
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.save:\x1b[0m {e}")

    def saveAs(self):
        browser = self.currentWidget().browser
        if isinstance(browser, Browser):
            placeholder_filename = browser.page().title()+".html"
            name, _ = QFileDialog.getSaveFileName(
                self, 'Save document.body.outerHTML as', 
                placeholder_filename, filter="*.html"
            )
            if name != "":
                browser.saveAs(name)

    def setTabZoom(self, zoom):
        zoom /= 100
        try:
            browser = self.currentWidget().browser
            browser.currentZoomFactor = zoom
            browser.setZoomFactor(zoom)
            # print(f"setting tab zoom: {zoom}")
        except AttributeError as e:
            print(f"\x1b[31;1mtab.setTabZoom\x1b[0m {e}")

    def zoomInTab(self):
        try:
            browser = self.currentWidget().browser
            currentZoom = browser.currentZoomFactor
            zoomFactor = ZoomFactor(currentZoom).gt(
                self.zoomFactors
            ).value
            # print(f"setting zoomFactor {zoomFactor}")
            self.currentWidget().browser.setZoomFactor(zoomFactor)
            browser.currentZoomFactor = zoomFactor
            # print(zoomFactor)
            self.titlebar.zoomSlider.setValue(100*zoomFactor)
            self.titlebar.zoomLabel.setText(f'{int(100*zoomFactor)}')
        except AttributeError as e:
            print(f"\x1b[31;1mtab.zoomInTab\x1b[0m {e}")

    def zoomOutTab(self):
        try:
            browser = self.currentWidget().browser
            currentZoom = browser.currentZoomFactor
            zoomFactor = ZoomFactor(currentZoom).lt(
                self.zoomFactors[::-1]
            ).value
            # print(f"setting zoomFactor {zoomFactor}")
            browser.setZoomFactor(zoomFactor)
            browser.currentZoomFactor = zoomFactor
            # print(zoomFactor)
            self.titlebar.zoomSlider.setValue(100*zoomFactor)
            self.titlebar.zoomLabel.setText(f'{int(100*zoomFactor)}')
        except AttributeError as e:
            print("\x1b[31;1mtab.zoomOutTab\x1b[0m", e)

    def connectTitleBar(self, titlebar):
        '''connect the title bar with tab widget so that the zoom slider and zoom label may be modified when the zoom in and zoom out buttons are clicked.'''
        self.titlebar = titlebar

    def prevUrl(self, i: int):
        currentWidget = self.currentWidget().browser
        try:
            currentWidget.prevInHistory()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.prevUrl:\x1b[0m {e}")
            print(f"tab-{i} is not a browser instance") 

    def reloadUrl(self, i: int):
        try:
            browser = self.currentWidget().browser
            browser.reload()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"\x1b[31;1mtab.reloadUrl:\x1b[0m {e}")
            print(f"tab-{i} is not a browser instance") 

    def goToItem(self, item: QWebEngineHistoryItem) -> None:
        """[summary]

        Args:
            item (QWebEngineHistoryItem): [description]
        """
        try:
            browser = self.currentWidget().browser
            browser.history().goToItem(item)
        except Exception as e:
            print("\x1b[31;1mtab.goToItem:\x1b[0m", e)

    def loadUrlForIndex(self, i: int, url: Union[str, QUrl]):
        if isinstance(url, str):
            qurl = QUrl(url)
        else: qurl = url
        self.setCurrentIndex(i)
        # use back reference from the splitter object.
        browser = self.currentWidget().browser
        browser.setUrl(qurl)
        self.setTabText(i, "  "+qurl.toString().strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )

    def loadUrl(self, url: str):
        qurl = QUrl(url)
        # use back reference from the splitter object.
        i = self.currentIndex()
        browser = self.currentWidget().browser
        browser.setUrl(qurl)
        self.setTabText(i, "  "+url.strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )

    def openFile(self, path: str):
        iconName = self.getIconName(path)
        icon = QIcon.fromTheme(iconName)
        self.tabIcons.append(icon)
        # print(icon, iconName)
        label = QLabel()
        label.setText(open(path).read())
        title = collapseuser(path)
        i = self.addTab(label, self.tabIcons[-1], title)
        try:
            self.dash_window.navbar.setFocus()
        except Exception as e:
            print("\x1b[31;1mtab.openFile:\x1b[0m", e)
        self.setCurrentIndex(i)

    def getIconName(self, path: str):
        file_info = QFileInfo(path)
        mimeType = self.mimetype_db.mimeTypeForFile(file_info)
        # print(QIcon.fromTheme(mimeType.iconName()))
        iconName = mimeType.iconName() 
        # print(iconName, QIcon.fromTheme(iconName))
        return iconName


class TabBar(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""
    # plusClicked = pyqtSignal()
    def __init__(self):
        super(TabBar, self).__init__()
        self.setAcceptDrops(True)
        # # Plus Button
        # self.plusButton = QPushButton("+")
        # self.plusButton.setParent(self)
        # self.plusButton.setFixedSize(20, 20)  # Small Fixed size
        # self.plusButton.clicked.connect(self.plusClicked.emit)
        # self.movePlusButton() # Move to the correct location
        # # end Constructor
    # def sizeHint(self):
    #     """Return the size of the TabBar with increased width for the plus button."""
    #     sizeHint = QTabBar.sizeHint(self) 
    #     width = sizeHint.width()
    #     height = sizeHint.height()
    #     return QSize(width+50, height)
    def dragEnterEvent(self, event):
        if event.mimeData():
            print("tab.TabBar.dragEnterEvent", event.mimeData.formats())
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        pos = event.pos()
        # compute the tab number.
        # mouseEvent = QMouseEvent(event)
        # pos: QPoint = mouseEvent.pos()
        count = self.count()
        clickedItem = -1
        for i in range(count):
            if self.tabRect(i).contains(pos):
                clickedItem = i
                break
        print(clickedItem)
        # contextMenu.setIconSize(QSize(30,30))
        newTabToRight = contextMenu.addAction(FigD.Icon("tabbar/new-tab.png"), "New tab to the right")
        addToReadingList = contextMenu.addAction(FigD.Icon("tabbar/reading_list.svg"), "Add tab to reading list")
        addToGroup = contextMenu.addAction("Add tab to group")
        moveTab = contextMenu.addAction("Move tab to new window")
        renameTab = contextMenu.addAction("Rename tab")
        contextMenu.addSeparator()
        reloadAct = contextMenu.addAction(FigD.Icon("tabbar/reload.svg"), "Reload") 
        duplicate = contextMenu.addAction(FigD.Icon("tabbar/duplicate.png"), "Duplicate") 
        pin = contextMenu.addAction(FigD.Icon("tabbar/pin.svg"), "Pin")
        mute = contextMenu.addAction(FigD.Icon("tabbar/mute.svg"), "Mute site")
        contextMenu.addSeparator()
        close = contextMenu.addAction(FigD.Icon("tabbar/close-tab.png"), "Close")
        closeOther = contextMenu.addAction("Close other tabs")
        closeToRight = contextMenu.addAction(FigD.Icon("tabbar/close-all-tabs.png"), "Close tabs to the right")
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(5)
        glow_effect.setOffset(0,0)
        glow_effect.setColor(QColor(235, 95, 52))
        # contextMenu.setGraphicsEffect(glow_effect)
        contextMenu.setWindowOpacity(0.9)
        contextMenu.setStyleSheet('''
        QMenu {
            color: #fff;
            font-family: 'Be Vietnam Pro', sans-serif;
            /* background: rgba(29,29,29,0.8); */
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(0,0,0,0.9), stop : 0.6 rgba(29,29,29,0.9));
        }
        QMenu:selected  {
            color: #292929;
            font-weight: bold;
            background: #eb5f34; /* qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
        }
        QMenu::separator {
            background: #484848;
        }''')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == renameTab:
            # print(event.x(), event.y())
            try: self.tabs.renameDialog(clickedItem)
            except Exception as e: 
                print("\x1b[31;1mtab.contextMenuEvent\x1b[0m", e)

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super(TabBar, self).resizeEvent(event)
        # self.movePlusButton()
    # def tabLayoutChange(self):
    #     """This virtual handler is called whenever the tab layout changes.
    #     If anything changes make sure the plus button is in the correct location.
    #     """
    #     super().tabLayoutChange()

    #     self.movePlusButton()
    # # end tabLayoutChange

    # def movePlusButton(self):
    #     """Move the plus button to the correct location."""
    #     # Find the width of all of the tabs
    #     size = sum([self.tabRect(i).width() for i in range(self.count())])
    #     # size = 0
    #     # for i in range(self.count()):
    #     #     size += self.tabRect(i).width()

    #     # Set the plus button location in a visible area
    #     h = self.geometry().top()
    #     w = self.width()
    #     if size > w: # Show just to the left of the scroll buttons
    #         self.plusButton.move(w-30, h)
    #     else:
    #         self.plusButton.move(size, h)
