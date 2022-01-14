#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
import getpass
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSignal, QFileInfo, Qt, QPoint, QMimeDatabase, QUrl, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QFileIconProvider, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QTabBar, QPushButton, QGraphicsDropShadowEffect
# fig-dash imports.
from ..utils import collapseuser
from fig_dash.assets import FigD
from fig_dash.ui.browser import Browser


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

        self.layout.addWidget(self.initBlank())
        self.layout.addWidget(self.plusBtn)
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
            # print(value)
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
        self.dropdownBtn = tabCornerWidget.dropdownBtn
        self.dropdown = tabCornerWidget.dropdown
        self.plusBtn = tabCornerWidget.plusBtn
        self.plusBtn.clicked.connect(lambda: self.openUrl())
        self.icon_provider = QFileIconProvider()
        # list of zoom factors.
        self.zoomFactors = [0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.1, 1.25, 1.5, 1.75, 2, 2.5, 3, 4, 5]
        self.zoomFactors = [ZoomFactor(zf) for zf in self.zoomFactors]
        # print(f"\x1b[34;1m{self.zoomFactors}\x1b[0m")
        self.tabbar = TabBar()
        self.setTabBar(self.tabbar)

        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.setDocumentMode(False)
        self.tabCloseRequested.connect(self.removeTab)
        self.setMovable(True)
        self.setCornerWidget(tabCornerWidget)
        self.setObjectName("DashTabWidget")
        self.setStyleSheet(dash_tab_widget_style.render())
        self.tabIcons = []
        # print(dash_tab_widget_style.render())
    def connectWindow(self, window):
        self.dash_window = window

    def connectDropdown(self, splitter):
        splitter.addWidget(self.dropdown)
        self.splitter = splitter
        self.dropdown.hide()

    def setupTabForBrowser(self, i: int, browser):
        try: dash_window = self.dash_window
        except AttributeError as e: return
        url = browser.url().toString()
        browser.loadDevTools()

        if url != "file:///tmp/fig_dash.rendered.content.html":    
            dash_window.navbar.searchbar.setText(url)
        else:
            dash_window.navbar.searchbar.setText("")
            dash_window.navbar.searchbar.setPlaceholderText("Search Google or type a URL")

        self.setTabText(i, "  "+browser.page().title())
        browser.changeUserAgent()
        browser.setZoomFactor(browser.currentZoomFactor)
        browser.setScrollbar(scrollbar_style)
        browser.setWordCount()
        browser.setSelectionStyle()
        browser.setIcon(tabs=self, i=i)
        # print(icon.isNull())
        # if not icon.isNull(): 
            # self.setTabIcon(i, icon) 
    def home(self):
        currentWidget = self.currentWidget()
        if isinstance(currentWidget, Browser):
            currentWidget.load(
                FigD.static(
                    "home.html",
                    USERNAME=getpass.getuser(),
                    HOME_CSS=FigD.staticUrl("home.css"),
                )
            )

    def openHome(self):
        self.openUrl(url=FigD.static(
            "home.html",
            USERNAME=getpass.getuser(),
            HOME_CSS=FigD.staticUrl("home.css"),
        ).toString())

    def openFolder(self, folder: str):
        pass

    def openWidget(self, widget: QWidget, 
                   title: str="", icon: str=""):
        i = self.addTab(widget, QIcon(icon), "  "+title)
        self.setCurrentIndex(i)

    def openUrl(self, url: str="https://google.com"):
        qurl = QUrl(url)
        browser = Browser(self)
        browser.connectTabWidget(self)
        browser.setUrl(qurl)
        i = self.addTab(browser.splitter, FigD.Icon("browser.svg"), "  "+url.strip())
        self.setTabText(i, "  "+url.strip())
        browser.loadFinished.connect(
            lambda _, i = i, browser = browser:
				self.setupTabForBrowser(i, browser)
        )
        self.setCurrentIndex(i)

    def nextUrl(self, i: int):
        currentWidget = self.currentWidget().browser
        try:
            currentWidget.nextInHistory()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"tab-{i} is not a browser instance") 

    def save(self):
        currentWidget = self.currentWidget().browser
        if isinstance(currentWidget, Browser):
            print(currentWidget.page())

    def setTabZoom(self, zoom):
        zoom /= 100
        try:
            browser = self.currentWidget().browser
            browser.currentZoomFactor = zoom
            browser.setZoomFactor(zoom)
            # print(f"setting tab zoom: {zoom}")
        except AttributeError as e:
            print(e)

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
        except AttributeError as e:
            print(e)

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
        except AttributeError as e:
            print(e)

    def prevUrl(self, i: int):
        currentWidget = self.currentWidget().browser
        try:
            currentWidget.prevInHistory()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"tab-{i} is not a browser instance") 

    def reloadUrl(self, i: int):
        currentWidget = self.currentWidget().browser
        try:
            currentWidget.reload()
        except AttributeError as e: 
            i = self.currentIndex()
            print(f"tab-{i} is not a browser instance") 

    def loadUrl(self, i: int, url: str):
        qurl = QUrl(url)
        self.setCurrentIndex(i)
        # use back reference from the splitter object.
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
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # contextMenu.setIconSize(QSize(30,30))
        newTabToRight = contextMenu.addAction(FigD.Icon("tabbar/new-tab.png"), "New tab to the right")
        addToReadingList = contextMenu.addAction(FigD.Icon("tabbar/reading_list.svg"), "Add tab to reading list")
        addToGroup = contextMenu.addAction("Add tab to group")
        moveTab = contextMenu.addAction("Move tab to new window")
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
        glow_effect.setOffset(3,3)
        glow_effect.setColor(QColor(235, 95, 52))
        contextMenu.setGraphicsEffect(glow_effect)
        contextMenu.setStyleSheet('''
        QMenu {
            color: #fff;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
        }
        QMenu:selected  {
            color: #292929;
            font-weight: bold;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        }
        QMenu::separator {
            background: #484848;
        }''')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

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
