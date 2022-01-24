#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from PyQt5.QtGui import QIcon, QFontMetrics
import os
from pprint import pprint
from token import AT
from typing import Union, Tuple
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt, QUrl, QSize, QPoint
from PyQt5.QtWidgets import QToolBar, QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
# fig_dash
from fig_dash.assets import FigD


class SocialMediaBtn(QToolButton):
    def __init__(self, site, **args) -> None:
        super(SocialMediaBtn, self).__init__(None)
        self.site = site
        self.url = args.get("url")
        self.inactive_icon_path = os.path.join(
            "shortcut_sidebar", 
            self.site+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcut_sidebar", 
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


class GShortcutBtn(QToolButton):
    '''
    shortcut button for google utilities: images, videos, news, shopping, travel, maps, books, flights, finance
    '''
    def __init__(self, parent: Union[QWidget, None]=None, **args) -> None:
        super(GShortcutBtn, self).__init__(parent)
        self.type = args.get("type")
        self.inactive_icon_path = os.path.join(
            "shortcut_sidebar", 
            self.type+".svg"
        )
        self.active_icon_path = os.path.join(
            "shortcut_sidebar", 
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
class ShortcutSidebar(QToolBar):
    '''
    Shortcut sidebar to jump to well known sites:
    famous social media sites: whatsapp, twitch, twitter, linkedin, reddit
    google utilities: images, videos, news, shopping, travel, maps, books, flights, finance
    '''
    def __init__(self, parent: Union[QWidget, None]=None) -> None:
        super(ShortcutSidebar, self).__init__(parent)
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
        self.moreBtn = GShortcutBtn(type="more", tip="more options")
        self.twitchBtn = SocialMediaBtn("twitch", url="https://twitch.com")
        self.twitterBtn = SocialMediaBtn("twitter", url="https://twitter.com")
        self.youtubeBtn = SocialMediaBtn("youtube", url="https://youtube.com")
        self.whatsappBtn = SocialMediaBtn("whatsapp", url="https://web.whatsapp.com/")
        self.instagramBtn = SocialMediaBtn("instagram", url="https://instagram.com")
        self.facebookBtn = SocialMediaBtn("facebook", url="https://facebook.com")
        self.redditBtn = SocialMediaBtn("reddit", url="https://reddit.com")
        self.linkedinBtn = SocialMediaBtn("linkedin", url="https://linkedin.com")
        # add all widgets to layout.
        self.addWidget(self.imagesBtn)
        self.addWidget(self.videosBtn)
        self.addWidget(self.newsBtn)
        self.addWidget(self.booksBtn)
        self.addWidget(self.mapsBtn)
        self.addWidget(self.shoppingBtn)
        self.addWidget(self.travelBtn)
        self.addWidget(self.flightsBtn)
        self.addWidget(self.financeBtn)
        self.addSpacer()
        self.addWidget(self.youtubeBtn)
        self.addWidget(self.twitchBtn)
        self.addWidget(self.instagramBtn)
        self.addWidget(self.facebookBtn)
        self.addWidget(self.twitterBtn)
        self.addWidget(self.redditBtn)
        self.addWidget(self.linkedinBtn)
        self.addWidget(self.whatsappBtn)
        self.addSpacer()
        self.addWidget(self.moreBtn)
        self.addSpacer()
        self.setStyleSheet("""background-color: qlineargradient(x1 : 0.7, y1 : 1, x2 : 0, y2 : 0, stop : 0.3 rgba(32, 32, 32, 1), stop : 0.6 rgba(16, 16, 16, 1)); color: #fff; border: 0px;""")
        # set icon size.
        self.setIconSize(QSize(35,35))
        # make unmovable.
        self.setMovable(False)

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