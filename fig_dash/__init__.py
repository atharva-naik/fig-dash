#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class FigDImportGuard:
    def __init__(self):
        import time
        self.import_ctr = 0
        # loading time accounting
        self.start_time = time.time()
        self.load_times = []
        self.load_timestamps = []

    def __call__(self, scope: str):
        import time
        # from PyQt5.QtWidgets import QApplication
        load_timestamp = time.time()
        self.import_ctr += 1 # update import statement counter.
        self.load_timestamps.append(load_timestamp) # update load time accounting variables.
        if len(self.load_timestamps) == 1:
            load_time = load_timestamp-self.start_time
        else:
            load_time = load_timestamp-self.load_timestamps[-2]
        # app = QApplication.instance()
        # if app:
        #     if not hasattr(self, "splash"):
        #         print("\x1b[33;1mcreating splash screen\x1b[0m")
        #         # create splash screen.
        #         from PyQt5.QtGui import QPixmap
        #         from PyQt5.QtWidgets import QSplashScreen
        #         self.splash_pixmap = QPixmap(
        #             "/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png"
        #         )
        #         self.splash = QSplashScreen()
        #         self.splash.show() 
        #     self.splash.showMessage(f"loaded {scope}")
        #     app.processEvents()
        total_time = load_timestamp-self.start_time
        self.load_times.append(load_time)         
        if len(self.load_timestamps) != 1:                                        
            print(f"\x1b[32;1mload_time={load_time:.2f}s\x1b[0m")
        print(f"{self.import_ctr}) \x1b[34;1m{scope}\x1b[0m \x1b[33;1mt={total_time:.2f}\x1b[0m") 

FigDLoad = FigDImportGuard()
FigDLoad("fig_dash::__init__")
# # Qt imports.
# from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QKeySequence, QGuiApplication
# from PyQt5.QtCore import QSize, Qt, QT_VERSION_STR, QEvent
# from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow, QGraphicsBlurEffect
from fig_dash.config import *
from fig_dash.assets import FigD

def welcomeUser(tray_icon):
    '''
    welcome the user.
    This should be cross platform.
    '''
    import getpass
    import platform
    if platform.system() == "Linux":
        # this code gets higher resolution image for linux.
        utils.notify(msg=f"Welcome to fig dashboard {getpass.getuser()}!", icon=FigD.icon("logo.svg"), title="")
    else:
        tray_icon.showMessage("Fig Dashboard", f"Welcome to fig dashboard {getpass.getuser()}!", FigD.Icon("tray_icon.png"), 1000)

# class DashUI(QApplication):
#     def __init__(self, argv, **kwargs):
#         FigD(kwargs.get("resources", "resources"))
#         if hasattr(Qt, 'AA_EnableHighDpiScaling'):
#             # print("high resolution")
#             QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
#         if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
#             QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
#         super(DashUI, self).__init__(argv)
#         self.setStyleSheet("""
#         QToolTip {
#             color: #fff;
#             border: 0px;
#             padding-top: -1px;
#             padding-left: 5px;
#             padding-right: 5px;
#             padding-bottom: -1px;
#             font-size:  17px;
#             background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.7), stop : 0.143 rgba(22, 22, 22, 0.7), stop : 0.286 rgba(27, 27, 27, 0.7), stop : 0.429 rgba(32, 32, 32, 0.7), stop : 0.571 rgba(37, 37, 37, 0.7), stop : 0.714 rgba(41, 41, 41, 0.7), stop : 0.857 rgba(46, 46, 46, 0.7), stop : 1.0 rgba(51, 51, 51, 0.7));
#             font-family: 'Be Vietnam Pro', sans-serif;
#         }""")
#         ID = QFontDatabase.addApplicationFont(
#             FigD.font("datetime/digital-7.ttf")
#         )
#         print(QFontDatabase.applicationFontFamilies(ID))
#         ID = QFontDatabase.addApplicationFont(
#             FigD.font("BeVietnamPro-Regular.ttf")
#         )
#         print(QFontDatabase.applicationFontFamilies(ID))
#         # self.desktop = self.desktop()
#         self.window = DashWindow(**kwargs)
#         self.window_args = kwargs
#         # actions for tray icon context menu.
#         self.showAction = QAction("Open")
#         self.quitAction = QAction("Quit")
#         self.logsAction = QAction("Get logs")
#         self.supportAction = QAction("Collect support files")
#         self.settingsAction = QAction("Settings")
#         # add icons.
#         self.showAction.setIcon(FigD.Icon("tray/open.svg"))
#         self.quitAction.setIcon(FigD.Icon("tray/close.svg"))
#         self.logsAction.setIcon(FigD.Icon("tray/logs.svg"))
#         self.supportAction.setIcon(FigD.Icon("tray/logs.svg"))
#         self.settingsAction.setIcon(FigD.Icon("tray/settings.svg"))
#         # connect functions to actions.
#         self.showAction.triggered.connect(self.window.show)
#         self.quitAction.triggered.connect(self.quit)
#         # tray icon menu.
#         self.trayMenu = QMenu()
#         self.trayMenu.addAction(self.logsAction)
#         self.trayMenu.addAction(self.supportAction)
#         self.trayMenu.addSeparator()
#         self.trayMenu.addAction(self.settingsAction)
#         self.trayMenu.addSeparator()
#         self.trayMenu.addAction(self.showAction)
#         self.trayMenu.addAction(self.quitAction)
#         # tray icon button.
#         self.trayIcon = QSystemTrayIcon(FigD.Icon("tray_icon.svg"), self)
#         self.trayIcon.setContextMenu(self.trayMenu)
#         self.trayIcon.show()
#         # welcomeUser(self.trayIcon)
#         windowFlags = kwargs.get("windowFlags", ["frameless", "ontop"])
#         self.setWindowFlags(*windowFlags)
#         # print("\x1b[32;1mapp icon:\x1b[0m", FigD.icon("logo.png"))
#         self.setWindowIcon(FigD.Icon("logo.svg"))
#         self.window.setWindowIcon(FigD.Icon("logo.svg"))
#         # self.window.windowIcon().pixmap(QSize(128,128)).save("WOWOWOWOWOWO.png")
#         self.setCursor()
#         print(f"using Qt {QT_VERSION_STR}")
#         # self.window.setWindowIcon(QIcon(kwargs.get("icon")))
#     def setWindowFlags(self, *flags):
#         self.window.setFlags(*flags)
    
#     def notify(self, obj, event):
#         if event.type() == QEvent.WindowDeactivate:
#             self.window.titlebar.deactivate()
#             # currentWidget = self.window.tabs.currentWidget()
#             # currentWidget.setGraphicsEffect(QGraphicsBlurEffect(blurRadius=5))
#             # print("bluring background")
#         if event.type() == QEvent.WindowActivate:
#             self.window.titlebar.activate()
#             # currentWidget = self.window.tabs.currentWidget()
#             # currentWidget.setGraphicsEffect(None)
#             # print("unbluring background")
#         return super().notify(obj, event)

#     def newMainWindow(self, **kwargs) -> QMainWindow:
#         window = DashWindow(open_home=False, **self.window_args)
#         windowFlags = kwargs.get("windowFlags", ["frameless", "ontop"])
#         window.setFlags(*windowFlags)
#         window.setWindowIcon(FigD.Icon("logo.svg"))
#         window.show()
#         url = kwargs.get("url")
#         if url: window.tabs.loadUrl(url)

#         return window 

#     def launch(self, maximized=True):
#         '''
#         launch app ui.
#         show QMainWindow and then run QApplication
#         '''
#         if maximized:
#             self.window.showMaximized()
#         else:
#             self.window.show()
#         self.window.notifsPanel.hide()
#         sys.exit(self.run())

#     def Exit(self, flag):
#         sys.exit(flag)

#     def run(self):
#         '''execute app ui.'''
#         self.exec_()

#     def setCursor(self):
#         '''setup cursor image.'''
#         self.setCursorFlashTime(1000)
#         # pixmap = QPixmap(__icon__("cursor.svg")).scaledToWidth(32).scaledToWidth(32)
#         # cursor = QCursor(pixmap, 32, 32)