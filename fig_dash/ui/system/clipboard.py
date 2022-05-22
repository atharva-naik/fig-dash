#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import jinja2
import datetime
from typing import Union
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import FigDAppContainer, styleContextMenu, styleTextEditMenuIcons, wrapFigDWindow
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
# PyQt5 imports
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QImage
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QScrollArea, QSplitter, QMenu, QTabWidget, QToolBar, QLabel, QPushButton, QToolButton, QSizePolicy, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QAction, QCalendarWidget, QGraphicsDropShadowEffect, QApplication, QMainWindow


CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD = False
# Clipboard SearchBar.
class DashClipboardSearchBar(QLineEdit):
    def __init__(self, accent_color: str="purple", 
                 parent: Union[QWidget, None]=None):
        super(DashClipboardSearchBar, self).__init__(parent=parent)
        self.menu = self.createStandardContextMenu()
        self.accent_color = accent_color
        self.setPlaceholderText("Search Clipboard!")
        self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            background: #292929;
        }""")

    def contextMenuEvent(self, event):
        self.menu = self.createStandardContextMenu()
        self.menu = styleContextMenu(self.menu, self.accent_color)
        self.menu = styleTextEditMenuIcons(self.menu)
        self.menu.popup(event.globalPos())

# Clipboard Item editing text area.
class DashClipboardEditArea(QTextEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashClipboardEditArea, self).__init__(parent)
        self.setStyleSheet("""
        QTextEdit {
            color: #aaa;
            margin: 10px;
            font-size: 17px;
            background: #292929;
            border-radius: 10px;
            border: 1px solid gray;
            font-family: "Be Vietnam Pro";
            selection-background-color: purple;
        }""")
        self.setText("Use this area to edit clipboard items/copy sections of the text.")

# Clipboard Item.
class DashClipboardItem(QWidget):
    def __init__(self, content: Union[str, QIcon], 
                 accent_color: str="purple", 
                 parent: Union[None, QWidget]=None):
        super(DashClipboardItem, self).__init__(parent)
        self.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            padding: 10px;
            border-radius: 5px;
            background: #484848;
            font-family: "Be Vietnam Pro";
        }""")
        self.content = content
        self.accent_color = accent_color
        # create hbox layout.
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(5, 5, 5, 5)
        # create content area and control panel.
        self.ctrlPanel = self.initCtrlPanel()
        self.contentArea = self.initContentArea(content)
        self.hboxlayout.addWidget(self.ctrlPanel)
        self.hboxlayout.addWidget(self.contentArea)
        self.setLayout(self.hboxlayout)

    def initContentArea(self, content) -> Union[QLabel, QTextEdit, QLabel]:
        if isinstance(content, QImage):
            contentArea = QLabel()
            contentArea.setPixmap(content.pixmap(100, 100))
        elif isinstance(content, str):
            contentArea = QLabel()
            contentArea.setText(content)
        else:
            contentArea = QTextEdit()
            contentArea.setHtml(content)
            contentArea.setReadOnly(True)
            contentArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        contentArea.setStyleSheet("background: #292929; padding: 10px; border-top-right-radius: 10px; border-bottom-right-radius: 10px;")

        return contentArea

    def initCtrlBtn(self, icon: str) -> QToolButton:
        btn = QToolButton()
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            border-radius: 2px;
            background: transparent;
        }
        QToolButton:hover {
            background: """+self.accent_color+""";
        }""")
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(40,40))

        return btn

    def initCtrlPanel(self):
        ctrlPanel = QWidget()
        ctrlPanel.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            padding: 10px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            background: """+self.accent_color+""";
            font-family: "Be Vietnam Pro";
        }""")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        # create control buttons.
        self.copyBtn = self.initCtrlBtn("textedit/copy.svg")
        self.copyTextBtn = self.initCtrlBtn("system/clipboard/copy_text.svg") 
        self.copyAsHTMLBtn = self.initCtrlBtn("system/clipboard/copy_as_html.svg")
        self.copyToTextareaBtn = self.initCtrlBtn("system/clipboard/copy_to_textarea.svg")
        self.saveBtn = self.initCtrlBtn("system/clipboard/save.svg")
        self.deleteBtn = self.initCtrlBtn("system/clipboard/delete.svg")
        # connect to slots.
        self.copyBtn.clicked.connect(self.copyItemContent)
        # build control panel layout.
        layout.addWidget(self.copyBtn)
        layout.addWidget(self.copyTextBtn)
        layout.addWidget(self.copyAsHTMLBtn)
        layout.addWidget(self.copyToTextareaBtn)
        layout.addWidget(self.saveBtn)
        layout.addWidget(self.deleteBtn)
        # add stretch to control panel.
        layout.addStretch(1)
        # set layout
        ctrlPanel.setLayout(layout)
        ctrlPanel.setFixedWidth(40)

        return ctrlPanel

    def copyItemContent(self):
        """
        copy item content as it is, (text, image or html) as it is. 
        TODO: Find a way to not put it on the clipboard UI.
        """
        global CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD
        CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD = True
        if isinstance(self.content, str):
            QApplication.clipboard().setText(self.content)

# Clipboard UI.
class DashClipboardUI(QWidget):
    def __init__(self, accent_color: str="purple"):
        super(DashClipboardUI, self).__init__()
        QApplication.clipboard().dataChanged.connect(
            self.onDataChanged
        )
        self.accent_color = accent_color
        # layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        # search bar.
        self.searchbar = self.initSearchBar()
        self.searchbar.setObjectName("searchbar")
        self.vboxlayout.addWidget(self.searchbar)
        # central display stack.
        self.stack = self.initStack()
        self.stackArea = self.wrapInScrollArea(self.stack)
        self.stackArea.setStyleSheet("""
        QScrollArea {
            background: transparent;
        }""")
        # self.stackArea.setMinimumHeight(150)
        self.editor = DashClipboardEditArea()
        # self.editor.setMinimumHeight(100)
        self.stack_editor_splitter = QSplitter(Qt.Vertical)
        self.stack_editor_splitter.addWidget(self.stackArea)
        self.stack_editor_splitter.addWidget(self.editor)
        self.stack_editor_splitter.setSizes([200,200])
        self.vboxlayout.addWidget(self.stack_editor_splitter)
        # self.vboxlayout.addWidget(self.editor)
        # self.vboxlayout.addStretch(1)
        # set layout.
        self.setObjectName("DashClipboardUI")
        self.setLayout(self.vboxlayout)
        self.history = []

        # self.setStyleSheet("""
        # QWidget#DashClipboardUI {
        #     border-radius: 20px;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        # }""")
    def contextMenuEvent(self, event):
        self.menu = QMenu()
        self.menu.addAction(FigD.Icon("system/clipboard/clear.svg"), "Clear")
        self.menu.addAction(FigD.Icon("system/clipboard/export.svg"), "Export")
        self.menu = styleContextMenu(self.menu, accent_color=self.accent_color)
        self.menu.popup(event.globalPos())

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("wrapInScrollArea("+widget.objectName()+")")
        scrollArea.setWidget(widget)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scrollArea.setAttribute(Qt.WA_TranslucentBackground)
        scrollArea.setStyleSheet("""
        QScrollArea {
            background-position: center;
            background: transparent;
            border: 0px;
        }
        QScrollBar:vertical {
            border: 0px solid #999999;
            width: 15px;    
            margin: 0px 0px 0px 0px;
            background-color: rgba(255, 255, 255, 0);
        }
        QScrollBar::handle:vertical {         
            min-height: 0px;
            border: 0px solid red;
            border-radius: 0px;
            background-color: transparent;
        }
        QScrollBar::handle:vertical:hover {         
            background-color: rgba(255, 255, 255, 0.5);
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }""")

        return scrollArea

    def initStack(self):
        stack = QWidget()
        stack.setStyleSheet("""
        QWidget {
            border: 0px;
            background: transparent;
        }""")
        stack.setObjectName("Stack")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.stackLayout = layout
        self.stackLayout.addStretch(1)
        stack.setLayout(layout)

        return stack

    def initSearchBar(self):
        searcharea = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        searcharea.setLayout(layout)
        searchbar = DashClipboardSearchBar(
            accent_color=self.accent_color,
        )
        layout.addWidget(searchbar)

        return searcharea

    def onDataChanged(self):
        # print(i)
        text = QApplication.clipboard().text()
        self.append(text)

    def initClipboardItem(self, item: Union[str, QImage]):
        item = DashClipboardItem(item, accent_color=self.accent_color)
        self.history.append(item)
        # item.setFixedHeight(100)
        return item

    def append(self, text: str):
        global CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD
        # print(f"\x1b[31;1mui.system.clipboard::DashClipboardUI::append\x1b[0m({text})")
        self.history.append(text)
        if CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD:
            CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD = False
        else:
            clipboard_item = self.initClipboardItem(text)
            self.stackLayout.insertWidget(0, clipboard_item)
        # print([c.objectName() for c in self.children()])
def test_clipboard():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    # create the clipboard UI widget.
    accent_color = FigDAccentColorMap["clipboard"]
    app = FigDAppContainer(sys.argv)
    clipboard = DashClipboardUI(accent_color=accent_color)
    # wrap it in a FigDWindow
    window = wrapFigDWindow(clipboard, size=(25,25), 
                            icon="system/clipboard/logo.png", 
                            title="Clipboard Viewer", width=900,
                            height=400, accent_color=accent_color,
                            add_tabs=False)
    # show the app window.
    window.show()
    # run the application!
    app.exec()

def launch_clipboard():
    icon = FigDSystemAppIconMap["clipboard"]
    accent_color = FigDAccentColorMap["clipboard"]
    clipboard = DashClipboardUI(accent_color=accent_color)
    window = wrapFigDWindow(clipboard, size=(25,25), width=900,
                            title="Clipboard Viewer", height=400,
                            icon=icon, accent_color=accent_color,
                            name="clipboard", add_tabs=False)
    window.show()


if __name__ == "__main__":
    test_clipboard()