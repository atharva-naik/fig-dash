#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
from pprint import pprint
from typing import Union, Tuple, List
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QPoint
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect
# fig_dash
from fig_dash.assets import FigD
from fig_dash.api.system.audio import PulseController


toggle_btn_style = """ 
QToolButton {
    color: #fff;
    border: 4px solid orange;
    margin: 0px;
    padding: 10px;
    border-radius: 29px;
    background: transparent;
    /* background: transparent; */
}
QToolButton:hover {
    border: 0px;
    border-top-left-radius: 0px;
    border-top-right-radius: 29px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 29px;
    background: qradialgradient(cx: 0.75, cy: 0.75, radius: 0.7, stop : 0.3 rgba(235, 204, 52, 255), stop : 0.6 rgba(235, 95, 52, 225));
}
QToolTip {
    color: #fff;
    border: 0px;
    background: transparent;
}"""
class SocialMediaBtn(QToolButton):
    def __init__(self, site, **args) -> None:
        super(SocialMediaBtn, self).__init__(None)
        self.site = site
        self.url = args.get("url")
        self.inactive_icon_path = os.path.join(
            "shortcutbar", 
            self.site+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcutbar", 
            self.site+"_active.svg"
        )
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        tip = f"open {site}"
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.clicked.connect(self.trigger)
        self.tabs = None
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding: 5px;
            background: transparent;
        }""")

    def enterEvent(self, event):
        if os.path.exists(FigD.icon(self.active_icon_path)):
            self.setIcon(FigD.Icon(self.active_icon_path))
        # print("enter event")
        super(SocialMediaBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        super(SocialMediaBtn, self).leaveEvent(event)

    def trigger(self):
        url = QUrl(self.url)
        if self.tabs:
            browser = self.tabs.currentWidget().browser
            try: browser.setUrl(url)
            except AttributeError as e:
                print(e)

    def connectTabs(self, tabs):
        self.tabs = tabs


class SystemBtn(QToolButton):
    def __init__(self, icon, **args) -> None:
        super(SystemBtn, self).__init__(None)
        self.inactive_icon_path = os.path.join(
            "shortcutbar", 
            icon+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcutbar", 
            icon+"_active.svg"
        )
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        tip = args.get("tip", "some system function")
        callback = args.get("callback")
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.clicked.connect(callback)
        self.tabs = None
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding: 5px;
            background: transparent;
        }""")

    def setCallback(self, callback):
        '''set callback.'''
        self.clicked.connect(callback)

    def enterEvent(self, event):
        if os.path.exists(FigD.icon(self.active_icon_path)):
            self.setIcon(FigD.Icon(self.active_icon_path))
        # print("enter event")
        super(SystemBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        super(SystemBtn, self).leaveEvent(event)

    def connectTabs(self, tabs):
        self.tabs = tabs


class PlayPauseBtn(SystemBtn):
    def __init__(self, **args) -> None:
        super(PlayPauseBtn, self).__init__("pause", tip="toggle media play/pause", callback=print)        
        self.mode = "play"
        self.clicked.connect(self.toggle)

    def toggle(self):
        import pyautogui
        pyautogui.hotkey("playpause")
        if self.mode == "play":
            self.mode = "pause"
        else:
            self.mode = "play"
        self.inactive_icon_path = os.path.join(
            "shortcutbar", 
            self.mode+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcutbar", 
            self.mode+"_active.svg"
        )
        self.setIcon(FigD.Icon(self.active_icon_path))


class MoreToolbar(QToolBar):
    def focusOutEvent(self, event):
        super(MoreToolbar, self).focusOutEvent(event)
        self.hide()


class MoreBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 buttons: List[SocialMediaBtn]=[]) -> None:
        super(MoreBtn, self).__init__(parent)
        self.inactive_icon_path = "shortcutbar/more.svg"
        self.active_icon_path = "shortcutbar/more_active.svg"
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        tip = "show more options"
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.clicked.connect(self.showOptions)
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding: 5px;
            background: transparent;
        }""")
        self.buttons = buttons
        self.more_toolbar = MoreToolbar()
        self.more_toolbar.setStyleSheet("""background-color: qlineargradient(x1 : 0.7, y1 : 1, x2 : 0, y2 : 0, stop : 0.3 rgba(32, 32, 32, 1), stop : 0.6 rgba(16, 16, 16, 1)); color: #fff; border: 0px;""")
        # set icon size.
        self.more_toolbar.setIconSize(QSize(35,35))
        # make unmovable.
        self.more_toolbar.setMovable(False)
        for button in self.buttons:
            self.more_toolbar.addWidget(button)
        # self.more_toolbar.setWindowFlags(Qt.Popup)
        self.more_toolbar.hide()

    def enterEvent(self, event):
        if os.path.exists(FigD.icon(self.active_icon_path)):
            self.setIcon(FigD.Icon(self.active_icon_path))
        super(MoreBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        super(MoreBtn, self).leaveEvent(event)

    def connectTabs(self, tabWidget):
        self.tabs = tabWidget
        self.more_toolbar.setParent(tabWidget)

    def setPos(self):
        self.more_toolbar.move(0, self.y()-110)

    def showOptions(self):
        self.setPos()
        if self.more_toolbar.isVisible():
            self.more_toolbar.hide()
        else: 
            self.more_toolbar.show()
            self.more_toolbar.setFocus()


class GShortcutBtn(QToolButton):
    '''
    shortcut button for google utilities: images, videos, news, shopping, travel, maps, books, flights, finance
    '''
    def __init__(self, parent: Union[QWidget, None]=None, **args) -> None:
        super(GShortcutBtn, self).__init__(parent)
        self.type = args.get("type")
        self.inactive_icon_path = os.path.join(
            "shortcutbar", 
            self.type+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcutbar", 
            self.type+"_active.svg"
        )
        # self.size = args.get("size", (30,30)) 
        # self.setIconSize(QSize(*self.size))
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        tip = args.get("tip", "a tip")
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.clicked.connect(self.trigger)
        self.tabs = None
        self.setStyleSheet("""
        QToolButton {
            color: #fff;
            border: 0px;
            padding: 5px;
            background: transparent;
        }""")

    def enterEvent(self, event):
        if os.path.exists(FigD.icon(self.active_icon_path)):
            self.setIcon(FigD.Icon(self.active_icon_path))
        # print("enter event")
        super(GShortcutBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon_path))
        super(GShortcutBtn, self).leaveEvent(event)

    def trigger(self):
        url = QUrl(f"https://{self.type}.google.com")
        if self.tabs:
            browser = self.tabs.currentWidget().browser
            try: browser.setUrl(url)
            except AttributeError as e:
                print(e)

    def connectTabs(self, tabs):
        self.tabs = tabs
# #eb5f34, #ebcc34
# #a11f53, #eb5f34
def windowSwitcher():
    # pyautogui.keyDown("alt")
    # pyautogui.hotkey("tab")
    print("exited")


class AppLauncher(QToolBar):
    def __init__(self, parent: Union[QWidget, None]=None) -> None:
        super(AppLauncher, self).__init__(parent)
        self.metaBtns = {}
        self.setStyleSheet("""background-color: qlineargradient(x1 : 0.7, y1 : 1, x2 : 0, y2 : 0, stop : 0.3 rgba(32, 32, 32, 1), stop : 0.6 rgba(16, 16, 16, 1)); color: #fff; border: 0px;""")
        # set icon size.
        self.setIconSize(QSize(35,35))
        self.setMovable(False)
        self.hide()

    def connectMetaBar(self, **btns): 
        for key, value in btns.items():
            self.metaBtns[key] = value

    def focusInEvent(self, event):
        # print(f"\x1b[33mShortcutSidebar: focus in\x1b[0m")
        super(AppLauncher, self).focusInEvent(event)

    def focusOutEvent(self, event):
        super(AppLauncher, self).focusOutEvent(event)
        # print(f"\x1b[33mShortcutSidebar: {event}\x1b[0m")
        self.hide()
        for btn in self.metaBtns.values():
            btn.show()

    def toggle(self):
        if self.isVisible():
            self.hide()
            for btn in self.metaBtns.values():
                btn.show()
        else:
            for btn in self.metaBtns.values():
                btn.hide()
            self.show()
            self.setFocus()


class ShortcutBar(QToolBar):
    '''[summary]
    ## Purpose
    Shortcut bar for various functions
    ### google shortcuts 
    images, videos, news, shopping, travel, maps, books, flights, finance
    ### social media sites
    whatsapp, twitch, twitter, linkedin, reddit
    '''
    def __init__(self, parent: Union[QWidget, None]=None) -> None:
        super(ShortcutBar, self).__init__("Shortcuts", parent)
        # desktop utilties.
        import pyautogui
        self.desktopBtn = SystemBtn(
            "desktop", tip="show desktop", 
            callback=lambda : pyautogui.hotkey("win","d")
        )
        self.workspaceBtn = SystemBtn(
            "window_switcher", callback=windowSwitcher,
            tip="open window switcher (Alt+Tab) on Linux", 
        )
        self.screenshotBtn = SystemBtn(
            "screenshot", tip="print screen (screenshot)", 
            callback=lambda : pyautogui.hotkey("prtscr")
        )
        self.dimBtn = SystemBtn(
            "dim", tip="decrease screen brightness", 
            callback=lambda: pyautogui.hotkey("win","d")
        )
        self.brightBtn = SystemBtn(
            "bright", tip="increase screen brightness", 
            callback=lambda: pyautogui.hotkey("win","d")
        )
        # media tools.
        self.volumeUpBtn = SystemBtn(
            "volumeup", tip="increase volume",
            callback=lambda: pyautogui.hotkey(),
        ) 
        self.volumeDownBtn = SystemBtn(
            "volumedown", tip="decrease volume",
            callback=lambda: pyautogui.hotkey(),
        ) 
        self.volumeMuteBtn = SystemBtn(
            "volumemute", tip="mute audio",
            callback=lambda: pyautogui.hotkey(),
        ) 
        self.playPauseBtn = PlayPauseBtn() 
        self.forwardBtn = SystemBtn(
            "forward", tip="next track",
            callback=lambda: pyautogui.hotkey("nexttrack"),
        ) 
        self.backwardBtn = SystemBtn(
            "backward", tip="previous track",
            callback=lambda: pyautogui.hotkey("prevtrack"),
        ) 
        self.volume_backend = PulseController()
        # create GShortcut buttons.
        self.imagesBtn = GShortcutBtn(type="images", tip="open Google images search")
        self.videosBtn = GShortcutBtn(type="video", tip="open Google video search")
        self.newsBtn = GShortcutBtn(type="news")
        self.booksBtn = GShortcutBtn(type="books")
        self.mapsBtn = GShortcutBtn(type="maps")
        self.shoppingBtn = GShortcutBtn(type="shopping")
        self.travelBtn  = GShortcutBtn(type="travel")
        self.flightsBtn = GShortcutBtn(type="flights")
        self.financeBtn = GShortcutBtn(type="finance")
        self.twitchBtn = SocialMediaBtn("twitch", url="https://twitch.com")
        self.twitterBtn = SocialMediaBtn("twitter", url="https://twitter.com")
        self.youtubeBtn = SocialMediaBtn("youtube", url="https://youtube.com")
        self.whatsappBtn = SocialMediaBtn("whatsapp", url="https://web.whatsapp.com/")
        self.hangoutsBtn = SocialMediaBtn("hangouts", url="https://hangouts.com/")
        self.instagramBtn = SocialMediaBtn("instagram", url="https://instagram.com")
        self.facebookBtn = SocialMediaBtn("facebook", url="https://facebook.com")
        self.redditBtn = SocialMediaBtn("reddit", url="https://reddit.com")
        self.linkedinBtn = SocialMediaBtn("linkedin", url="https://linkedin.com")
        
        self.moreSystemBtn = MoreBtn(
            parent=self,
            buttons=[
                self.workspaceBtn, 
                self.screenshotBtn,
            ] 
        )
        self.moreMediaBtn = MoreBtn(
            parent=self,
            buttons=[
                self.backwardBtn,
                self.playPauseBtn,
                self.forwardBtn,
            ] 
        )
        self.morePagesBtn = MoreBtn(
            parent=self,
            buttons=[
                self.booksBtn,
                self.mapsBtn,
                self.shoppingBtn,
                self.travelBtn,
                self.flightsBtn,
                self.financeBtn,
            ]
        )
        self.moreSocialBtn = MoreBtn(
            parent=self,
            buttons=[
                self.facebookBtn,
                self.twitterBtn, 
                self.redditBtn,
                self.linkedinBtn,
                self.whatsappBtn,
                self.hangoutsBtn,
            ]
        )
        
        # add all widgets to layout.
        self.addWidget(self.imagesBtn)
        self.addWidget(self.videosBtn)
        self.addWidget(self.newsBtn)
        # self.addWidget(self.booksBtn)
        self.addWidget(self.morePagesBtn)
        # self.addWidget(self.mapsBtn)
        # self.addWidget(self.shoppingBtn)
        # self.addWidget(self.travelBtn)
        # self.addWidget(self.flightsBtn)
        # self.addWidget(self.financeBtn)
        self.addWidget(self.youtubeBtn)
        self.addWidget(self.twitchBtn)
        self.addWidget(self.instagramBtn)
        # self.addWidget(self.facebookBtn)
        # self.addWidget(self.twitterBtn)
        # self.addWidget(self.redditBtn)
        # self.addWidget(self.linkedinBtn)
        # self.addWidget(self.whatsappBtn)
        # self.addWidget(self.hangoutsBtn)
        self.addWidget(self.moreSocialBtn)
        self.addSpacer()
        self.addWidget(self.desktopBtn)
        # self.addWidget(self.workspaceBtn)
        # self.addWidget(self.screenshotBtn)
        self.addWidget(self.brightBtn)
        self.addWidget(self.dimBtn)
        # self.addWidget(self.appsBtn)
        self.addWidget(self.moreSystemBtn)
        self.addWidget(self.volumeMuteBtn)
        self.addWidget(self.volumeDownBtn)
        self.addWidget(self.volumeUpBtn)
        self.addWidget(self.moreMediaBtn)
        self.addSpacer()
        self.setStyleSheet("""background-color: qlineargradient(x1 : 0.7, y1 : 1, x2 : 0, y2 : 0, stop : 0.3 rgba(32, 32, 32, 1), stop : 0.6 rgba(16, 16, 16, 1)); color: #fff; border: 0px;""")
        # set icon size.
        self.setIconSize(QSize(35,35))
        # make unmovable.
        self.setMovable(False)
        self.toggleBtn = SystemBtn(
            "fig", callback=self.toggle,
            tip="toggle fig-dash shortcut panel"
        )
        self.toggleBtn = self.initMetaBtn(
            icon="fig", parent=parent, callback=self.toggle,
            tip="toggle fig-dash shortcut panel",
        )
        self.app_launcher = AppLauncher(parent)
        # intialization of appsBtn depends on initialization of app launcher
        # as the appsBtn needs the app launcher show method as it's 
        self.appsBtn = self.initMetaBtn(
            icon="apps", tip="open app launcher",
            callback=self.app_launcher.toggle,
            parent=parent
        )
        self.app_launcher.connectMetaBar(
            appsBtn=self.appsBtn,
            toggleBtn=self.toggleBtn,
        )
        self.hide()
        self.setMetaBarPos(0)
        self.volumeUpBtn.setCallback(self.volume_backend.increase)
        self.volumeDownBtn.setCallback(self.volume_backend.decrease)
        # self.toggleBtn.setFixedSize(QSize(50,50))
        # print("parent:", parent)
    def initMetaBtn(self, **args):
        '''meta buttons constitute the meta launcher'''
        w = args.get("width", 60)
        h = args.get("height", 60)
        tip = args.get("tip", "a tip")
        icon = args.get("icon")
        parent = args.get("parent")
        callback = args.get("callback")
        icon_size = args.get("icon_size", (55,55))
        # shadow effect.
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0,0)
        shadow.setColor(QColor(255, 165, 0))

        metaBtn = SystemBtn(icon, callback=callback, tip=tip)
        metaBtn.setParent(parent)
        metaBtn.setStyleSheet(toggle_btn_style)
        metaBtn.setIconSize(QSize(*icon_size))
        metaBtn.setGraphicsEffect(shadow)
        metaBtn.setFixedHeight(h)
        metaBtn.setFixedWidth(w)
        
        return metaBtn
    
    def setMetaBarPos(self, w=55):
        parent = self.parent()
        if parent is None: height = 400
        else: height = parent.height()//2 
        self.toggleBtn.move(0, height-35)
        self.appsBtn.move(0, height+35)
        self.h = height

    def focusInEvent(self, event):
        # print(f"\x1b[33mShortcutSidebar: focus in\x1b[0m")
        super(ShortcutBar, self).focusInEvent(event)

    def focusOutEvent(self, event):
        super(ShortcutBar, self).focusOutEvent(event)
        # print(f"\x1b[33mShortcutSidebar: {event}\x1b[0m")
        self.hide()
        self.toggleBtn.show()
        self.appsBtn.show()

    def toggle(self):
        if self.isVisible():
            self.hide()
            self.toggleBtn.show()
            self.appsBtn.show()
            # self.toggleBtn.move(0,self.h)
        else:
            # self.toggleBtn.move(55,self.h)
            self.toggleBtn.hide()
            self.appsBtn.hide()
            self.show()
            self.setFocus()

    def addSpacer(self):
        spacer = QWidget()
        spacer.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            background: transparent;
        }""")
        spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.addWidget(spacer)
    # def connectVolMethods(self, **methods):
    #     '''
    #     connect instance of the VolumeSlider class.
    #     must have these functions:
    #     1) increase
    #     2) decrease
    #     3) toggleMute
    #     '''
    #     btns = [self.volumeUpBtn, self.volumeDownBtn, self.volumeMuteBtn]
    #     method_api = ["increase", "decrease", "toggleMute"]
    #     for btn, method in zip(btns, method_api):
    #         if method not in methods: continue
    #         btn.setCallback(methods[method])
    def connectTabs(self, tabs):
        self.tabs = tabs
        self.imagesBtn.connectTabs(tabs)
        self.videosBtn.connectTabs(tabs)
        self.newsBtn.connectTabs(tabs)
        self.booksBtn.connectTabs(tabs)
        self.mapsBtn.connectTabs(tabs)
        self.shoppingBtn.connectTabs(tabs)
        self.travelBtn.connectTabs(tabs)
        self.flightsBtn.connectTabs(tabs)
        self.financeBtn.connectTabs(tabs)
        # connect social media functionalities
        self.twitchBtn.connectTabs(tabs)
        self.twitterBtn.connectTabs(tabs)
        self.youtubeBtn.connectTabs(tabs)
        self.whatsappBtn.connectTabs(tabs)
        self.instagramBtn.connectTabs(tabs)
        self.facebookBtn.connectTabs(tabs)
        self.redditBtn.connectTabs(tabs)
        self.linkedinBtn.connectTabs(tabs)
        # connect the more button.
        self.moreSystemBtn.connectTabs(tabs)
        self.moreSocialBtn.connectTabs(tabs)
        self.morePagesBtn.connectTabs(tabs)
        self.moreMediaBtn.connectTabs(tabs)