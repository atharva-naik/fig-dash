#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-

# combined app launcher and store.

import os
import json
from typing import *
from dataclasses import dataclass
# from fig_dash.api.system.file.applications import FigDIconMap
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.apps import AccentColorMap, AppTitleMap, AppIconMap
from fig_dash.ui import styleContextMenu, wrapFigDWindow, FigDAppContainer
# all app imports
from fig_dash.ui.apps.screenshot.screenshot import launch_screenshot_ui
# PyQt5 imports.
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QKeySequence, QColor, QPalette, QDrag
from PyQt5.QtCore import Qt, QSize, QStringListModel, QPoint, QRectF, QTimer, QUrl, QDir, QMimeDatabase, QMimeData
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QScrollArea, QShortcut, QMainWindow, QApplication, QSplitter, QLabel, QToolBar, QToolButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QCompleter, QTabWidget, QGraphicsDropShadowEffect

def blank(): pass
AppLauncherMap = {
    "gradient_creator": blank,
    "colorpicker": blank,    
    "screenshot": launch_screenshot_ui,
    "paint": blank,
    "citationhelper": blank,
    "library": blank,
}
AppLauncherLayout = {
    "Creative Tools": [
        "gradient_creator",
        "paint",
        "colorpicker",    
    ],
    "screenshot": None,
    "Reading Tools": [
        "citationhelper",
        "library",
    ]
}
APPS_LAUNCHED = []
APPS_LAUNCHER_ROW_SIZE = 3
APPS_LAUNCHER_ACCENT_COLOR = "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #3e23f9, stop : 0.091 #322cfc, stop : 0.182 #003fff, stop : 0.273 #0054ff, stop : 0.364 #0068ff, stop : 0.455 #007bff, stop : 0.545 #008dff, stop : 0.636 #009dff, stop : 0.727 #00a9ff, stop : 0.818 #00b3ff, stop : 0.909 #00baff, stop : 1.0 #00bcff)"

@dataclass
class DashAppInfo:
    name: str
    size: int # width and height dimension.
    icon_size: int # size of the icon.
    isgrouped: bool # is the app inside a group?

    @classmethod
    def fromjsonstr(cls, jsonstr):
        jsonobj = json.loads(jsonstr)
        return cls(
            name=jsonobj["name"],
            size=jsonobj["size"],
            icon_size=jsonobj["icon_size"],
            isgrouped=jsonobj["isgrouped"],
        )

    def tojsonstr(self):
        return json.dumps({
            "name": self.name, 
            "size": self.size,
            "icon_size": self.icon_size,
            "isgrouped": self.isgrouped,
        })

class DashAppBtn(QToolButton):
    def __init__(self, info: DashAppInfo, 
                 parent: Union[QWidget, None]=None):
        super(DashAppBtn, self).__init__(parent)
        self.__mouseMovePos = None
        self.__mousePressPos = None
        self.info = info
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setText(AppTitleMap[info.name])
        self.setIcon(FigD.Icon(AppIconMap[info.name]))
        accent_color = AccentColorMap.get(info.name, "gray")
        if "qlineargradient" in accent_color or "qconicalgradient" in accent_color:
            border_color = accent_color.split(":")[-1].strip()
            border_color = border_color.split()[-1].split(")")[0]
            border_color = border_color.strip()
        else: border_color = "gray"
        if info.isgrouped:
            self.setStyleSheet("""
            QToolButton {
                color: #fff; 
                padding: 5px;
                font-size: 16px;
                border-radius: 10px;
                background: transparent;
                font-family: 'Be Vietnam Pro', sans-serif;
            }
            QToolButton:hover {
                border: 1px solid """+border_color+""";
                color: #292929;
                font-weight: bold;
                background: """+accent_color+""";
            }""")
        else:
            self.setStyleSheet("""
            QToolButton {
                color: #fff; 
                padding: 15px;
                font-size: 20px;
                background: #484848;
                border-radius: 10px;
                font-family: 'Be Vietnam Pro', sans-serif;
            }
            QToolButton:hover {
                border: 1px solid """+border_color+""";
                color: #292929;
                font-weight: bold;
                background: """+accent_color+""";
            }""")
        self.setFixedWidth(info.size)
        self.setFixedHeight(info.size)
        self.setIconSize(QSize(
            info.icon_size, 
            info.icon_size
        ))
        self.launch_fn = AppLauncherMap[info.name]
        self.clicked.connect(self.launchApp)
        self.menu = QMenu()
        self.menu.addAction(FigD.Icon("tray/open.svg"), "Open")
        self.menu.addAction(FigD.Icon("menu/file.svg"), "Open file or directory")
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("apps/info.svg"), "Open app info page")
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("apps/pin.svg"), "Pin to shortcuts")
        self.menu.addSeparator()
        if info.isgrouped:
            self.menu.addAction(FigD.Icon("apps/group.svg"), "Remove from group")
        else:
            self.menu.addAction(FigD.Icon("apps/group.svg"), "Add to group")
        self.menu.addSeparator()
        self.menu = styleContextMenu(self.menu, accent_color)

    def mousePressEvent(self, event):
        self.__mouseMovePos = None
        self.__mousePressPos = None
        if event.button() == Qt.LeftButton:
            self.__mouseMovePos = event.globalPos()
            self.__mousePressPos = event.globalPos()
        super(DashAppBtn, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.__mouseMovePos = globalPos
            print("dragging started")
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(self.info.tojsonstr())
            drag.setMimeData(mimeData)
            drag.setPixmap(self.icon().pixmap(
                self.info.icon_size, 
                self.info.icon_size,
            ))
            dropAction = drag.exec()
        super(DashAppBtn, self).mouseMoveEvent(event)
    # def mousePressEvent(self, event):
        # if event.button() == Qt.LeftButton and self.icon().geometry().contains(event.pos()):
        #     print("dragging started")
        #     drag = QDrag(self)
        #     mimeData = QMimeData()
        #     mimeData.setText(self.info.tojsonstr())
        #     drag.setMimeData(mimeData)
        #     drag.setPixmap(self.icon().pixmap(
        #         self.info.icon_size, 
        #         self.info.icon_size,
        #     ))
        #     dropAction = drag.exec()
            # print(dropAction)
        # super(DashAppBtn, self).mousePressEvent(event)

    def launchApp(self):
        window = self.launch_fn()
        APPS_LAUNCHED.append(window)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())


class DashAppGroup(QWidget):
    def __init__(self, info_list: List[DashAppInfo], 
                 parent: Union[QWidget, None]=None,
                 group_name: str="Group"):
        super(DashAppGroup, self).__init__(parent)
        self.setAcceptDrops(True)
        self.gridlayout = QGridLayout()
        self.gridlayout.setContentsMargins(0, 0, 0, 0)
        self.gridlayout.setSpacing(0)
        self.gridwidget = QWidget()
        # self.gridwidget.setStyleSheet("""
        # QWidget {
        #     background: transparent;
        # }""")
        self.gridwidget.setLayout(self.gridlayout)
        # vertical layout (for the entire group: grid + label).
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        # the name of the group as shown by a QLabel.
        self.label = QLabel(group_name)
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setStyleSheet("""
        # QLabel {
        #     color: #fff;
        #     font-size: 19px;
        #     background: transparent;
        #     font-family: 'Be Vietnam Pro', sans-serif;
        # }""")
        for i, info in enumerate(info_list):
            self.gridlayout.addWidget(
                DashAppBtn(info=info),
                i//2, i%2, 
            )
        self.gridlayout.addWidget(self.label, 2, 0, 1, 2)
        self.vboxlayout.addWidget(self.gridwidget)
        self.setFixedHeight(230)
        self.setFixedWidth(230)
        # self.setObjectName("DashAppGroup")
        self.setLayout(self.vboxlayout)
        self.setStyleSheet("""
        QWidget {
            color: #fff; 
            padding: 2px;
            font-size: 18px;
            background: rgba(72, 72, 72, 0.8);
            border-radius: 10px;
            font-family: 'Be Vietnam Pro', sans-serif;            
        }""")
        self.label.setStyleSheet("""
        QLabel {
            padding-bottom: 5px;
            background: transparent;
        }""")
        self.menu = QMenu()
        self.menu.addAction(FigD.Icon("apps/add.svg"), "Add app to group")
        self.menu.addAction(FigD.Icon("apps/edit.svg"), "Edit group")
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("apps/pin.svg"), "Pin to shortcuts")
        self.menu.addSeparator()
        self.menu.addAction(FigD.Icon("apps/rename.svg"), "Rename group")
        self.menu.addAction(FigD.Icon("apps/delete.svg"), "Dissolve group")
        self.menu = styleContextMenu(self.menu, APPS_LAUNCHER_ACCENT_COLOR)

    def dragEnterEvent(self, event):
        # try: 
        # print("count:", self.gridlayout.count())
        item = self.gridlayout.itemAt(3)
        print("item:", item)
        if self.gridlayout.count() < 5 and item is None: 
            event.accept()
            return
        widget = item.widget()
        print("widget:", widget)
        if self.gridlayout.count() < 5 and not isinstance(widget, DashAppBtn):
            event.accept()
        else: event.ignore()
        # except Exception as e:
        #     print(e)
    def dropEvent(self, event):
        # get button info from mimedata.
        app_info_jsonstr = event.mimeData().text()
        # get row and column.
        row = (self.gridlayout.count()-1) // 2
        col = (self.gridlayout.count()-1) % 2
        # get dahs app info
        info = DashAppInfo.fromjsonstr(app_info_jsonstr)
        info.size = 100
        info.icon_size = 50
        info.isgrouped = True
        btn = DashAppBtn(info)
        self.gridlayout.addWidget(btn, row, col)
        event.source().setParent(None)

    def contextMenuEvent(self, event):
        self.menu.popup(event.globalPos())
    # def dragEvent(self):
    #     pass
class AppLauncherSearchBar(QLineEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(AppLauncherSearchBar, self).__init__(parent)
        # create actions.
        caseAction = self.addAction(
            FigD.Icon("apps/case.svg"), 
            QLineEdit.TrailingPosition
        )
        micAction = self.addAction(
            FigD.Icon("apps/mic.svg"),
            QLineEdit.TrailingPosition,
        )
        searchAction = self.addAction(
            FigD.Icon("browser/search.svg"), 
            QLineEdit.LeadingPosition
        )
        self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            padding: 5px;
            background: #292929;
            border-radius: 5px;
        }""")
        self.setPlaceholderText("Search apps")
        self.qcompleter = QCompleter()
        stringModel = QStringListModel()
        completion_prompts = [" ".join(title.split()) for title in AppTitleMap.values()]
        stringModel.setStringList(completion_prompts)
        self.qcompleter.setModel(stringModel)
        self.qcompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.qcompleter)
        self.setMinimumWidth(600)


class DashAppLauncher(QWidget): 
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashAppLauncher, self).__init__(parent)
        # vertical layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(10, 10, 10, 10)
        self.vboxlayout.setSpacing(10)
        # initialize scroll area (with buttons to launch apps.)
        self.searchbar = AppLauncherSearchBar()
        self.scroll_area = self.initScrollArea()
        # build layout.
        self.vboxlayout.addWidget(self.searchbar, 0, Qt.AlignCenter | Qt.AlignTop)
        self.vboxlayout.addWidget(self.scroll_area, 0, Qt.AlignCenter | Qt.AlignTop)
        self.vboxlayout.addStretch(1)
        # set layout.
        self.setLayout(self.vboxlayout)

    def initScrollArea(self):
        scroll_area = QScrollArea()
        launcher_widget = QWidget()
        launcher_widget.setStyleSheet("""
        QWidget {
            border-radius: 20px;
            /* background: #292929; */
        }""")
        launcher_layout = QGridLayout()
        for i, name in enumerate(AppLauncherLayout):
            if isinstance(AppLauncherLayout[name], list):
                info_list = []
                for j, app_name in enumerate(AppLauncherLayout[name]):
                    info_list.append(DashAppInfo(
                        name=app_name, size=100,
                        icon_size=50, isgrouped=True,
                    ))
                group = DashAppGroup(
                    info_list=info_list,
                    group_name=name,
                )
                launcher_layout.addWidget(group, i//APPS_LAUNCHER_ROW_SIZE, i%APPS_LAUNCHER_ROW_SIZE)
            else:
                btn = DashAppBtn(info=DashAppInfo(
                    name=name, size=230,
                    icon_size=140, isgrouped=False,
                ))
                launcher_layout.addWidget(btn, i//APPS_LAUNCHER_ROW_SIZE, i%APPS_LAUNCHER_ROW_SIZE)
        launcher_widget.setLayout(launcher_layout)
        scroll_area.setWidget(launcher_widget)
        scroll_area.setStyleSheet("""
        QScrollArea {
            background: transparent;
        }""")

        return scroll_area

def start_system_app_launcher():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    # create the clipboard UI widget.
    app = FigDAppContainer(sys.argv)
    app_launcher = DashAppLauncher()
    # wrap it in a FigDWindow
    icon = "apps/launcher.png"
    window = wrapFigDWindow(app_launcher, title="App Launcher and Store", 
                            accent_color=APPS_LAUNCHER_ACCENT_COLOR, 
                            icon=icon, name="app_launcher")
    # show the app window.
    window.show()
    # run the application!
    app.exec()


if __name__ == "__main__":
    start_system_app_launcher()