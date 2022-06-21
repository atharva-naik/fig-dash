#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::system::clipboard")

import sys
import jinja2
import datetime
from typing import Union
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
from fig_dash.ui import FigDAppContainer, FigDShortcut, FigDMainWidget, styleContextMenu, styleTextEditMenuIcons, wrapFigDWindow, extractFromAccentColor, setAccentColorAlpha
# PyQt5 imports
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QImage, QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget, QScrollArea, QSplitter, QMenu, QTabWidget, QToolBar, QLabel, QPushButton, QToolButton, QSizePolicy, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QAction, QCalendarWidget, QGraphicsDropShadowEffect, QApplication, QMainWindow


CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD = False
# Clipboard SearchBar.
class DashClipboardSearchBar(QLineEdit):
    def __init__(self, accent_color: str="purple", 
                 parent: Union[QWidget, None]=None):
        super(DashClipboardSearchBar, self).__init__(parent=parent)
        self.contextMenu = self.createStandardContextMenu()
        self.accent_color = accent_color
        self.setPlaceholderText("Search Clipboard!")
        self.setObjectName("DashClipboardSearchBar")
        self.setStyleSheet("""
        QLineEdit#DashClipboardSearchBar {
            color: #fff;
            padding-top: 8px;
            padding-bottom: 8px;
            background: #292929;
            font-size: 18px;
            padding-left: 5px;
            padding-right: 5px;
            border-radius: 5px;
            border: none;
            margin-left: 20px;
            margin-right: 20px;
            selection-background-color: """+self.accent_color+""";
        }""")

    def contextMenuEvent(self, event):
        self.contextMenu = self.createStandardContextMenu()
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
        self.contextMenu.popup(event.globalPos())

# Clipboard Item editing text area.
class DashClipboardEditArea(QTextEdit):
    def __init__(self, accent_color: str="purple", 
                 parent: Union[None, QWidget]=None):
        super(DashClipboardEditArea, self).__init__(parent)
        self.accent_color = accent_color
        color = extractFromAccentColor(
            accent_color, where="back"
        )
        self.setStyleSheet("""
        QTextEdit {
            color: #aaa;
            font-size: 18px;
            background: #292929;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            border: 7px solid """+color+""";
            border-top: none;
            font-family: "Be Vietnam Pro";
            selection-background-color: """+self.accent_color+""";
        }""")
        self.setText("Use this area to edit clipboard items/copy sections of the text.")
        
    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def contextMenuEvent(self, event):
        self.contextMenu = self.createStandardContextMenu()
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
        self.contextMenu.popup(event.globalPos())

# Clipboard Item.
class DashClipboardItem(QWidget):
    editItem = pyqtSignal()
    selected = pyqtSignal(int)
    def __init__(self, i: int, content: Union[str, QIcon],
                 timestamp: int=0, accent_color: str="purple",  
                 parent: Union[None, QWidget]=None, **fields):
        super(DashClipboardItem, self).__init__(parent)
        self.setStyleSheet("""
        QWidget {
            color: #fff;
            padding: 10px;
            border-radius: 10px;
            background: transparent;
            border: 2px solid #949494;
            font-family: "Be Vietnam Pro";
        }""")
        self.i = i
        self.content = content
        self.timestamp = timestamp
        self.accent_color = accent_color
        # create hbox layout.
        self.hboxlayout = QVBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(5, 5, 5, 5)
        # content area.
        self.contentArea = self.initContentArea(content)
        self.hboxlayout.addWidget(self.contentArea)
        self.setLayout(self.hboxlayout)

    def select(self):
        color = setAccentColorAlpha(self.accent_color)
        fontColor = extractFromAccentColor(
            self.accent_color, 
            where="back"
        )
        self.contentArea.setStyleSheet("""
        QLabel {
            color: """+fontColor+""";
            border: 2px solid """+fontColor+""";
            font-family: "Be Vietnam Pro";
        }""")  

    def deselect(self):
        self.contentArea.setStyleSheet("""
        QLabel {
            color: #fff;
            border: 2px solid #949494;
            font-family: "Be Vietnam Pro";
        }""")   

    def mousePressEvent(self, event):
        self.selected.emit(self.i)
        super(DashClipboardItem, self).mousePressEvent(event)
    # def createDropShadow(self, accent_color: str, where: str="back"):
    #     drop_shadow_color = extractFromAccentColor(accent_color, where=where)
    #     drop_shadow = QGraphicsDropShadowEffect()
    #     drop_shadow.setColor(QColor(drop_shadow_color))
    #     drop_shadow.setBlurRadius(10)
    #     drop_shadow.setOffset(0, 0)

    #     return drop_shadow
    def initContextMenu(self) -> QMenu:
        menu = QMenu()
        menu.addAction(FigD.Icon("system/clipboard/delete.svg"), 
                       "Delete", self.deleteItem, QKeySequence("Del"))
        menu.addSeparator()
        menu.addAction(FigD.Icon("system/clipboard/copy_text.svg"), 
                       "Copy", self.copyItemContent, QKeySequence.Copy)
        menu.addAction(FigD.Icon("system/clipboard/copy_json.svg"), 
                       "Copy JSON", self.copyItemJSON)
        menu.addSeparator()
        menu.addAction(FigD.Icon("system/clipboard/edit_item.svg"), 
                       "Edit item", self.signalEditItem)

        return menu

    def signalEditItem(self):
        self.selected.emit(self.i)
        self.editItem.emit()

    def contextMenuEvent(self, event):
        self.contextMenu = self.initContextMenu()
        self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu.popup(event.globalPos())

    def initContentArea(self, content) -> Union[QLabel, QTextEdit, QLabel]:
        if isinstance(content, QImage):
            contentArea = QLabel()
            contentArea.setPixmap(content.pixmap(100, 100))
            contentArea.setAlignment(Qt.AlignCenter)
        elif isinstance(content, QPixmap):
            contentArea = QLabel()
            contentArea.setPixmap(content)
            contentArea.setAlignment(Qt.AlignCenter)
        # elif isinstance(content, HTML):
        #     contentArea = QTextEdit()
        #     contentArea.setHtml(content)
        #     contentArea.setReadOnly(True)
        #     contentArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        elif isinstance(content, str):
            if len(content) > 500: 
                content = content[:500-5]+" ...."
            contentArea = QLabel()
            contentArea.setText(content)
        if isinstance(contentArea, QLabel):
            contentArea.setWordWrap(True)
        contentArea.setStyleSheet("background: transparent; padding: 10px;")

        return contentArea
    # def initCtrlBtn(self, icon: str) -> QToolButton:
    #     btn = QToolButton()
    #     btn.setStyleSheet("""
    #     QToolButton {
    #         color: #fff;
    #         border-radius: 2px;
    #         background: transparent;
    #     }
    #     QToolButton:hover {
    #         background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #390b56, stop : 0.091 #420d64, stop : 0.182 #4c0f72, stop : 0.273 #561181, stop : 0.364 #601390, stop : 0.455 #6a169f, stop : 0.545 #7418ae, stop : 0.636 #7f1abe, stop : 0.727 #891cce, stop : 0.818 #941ede, stop : 0.909 #9f20ee, stop : 1.0 #aa22ff);
    #     }""")
    #     btn.setIcon(FigD.Icon(icon))
    #     btn.setIconSize(QSize(40,40))

    #     return btn
    def deleteItem(self):
        self.hide()

    def copyItemJSON(self):
        """copy JSON corresponding to clipboard item to the clipboard."""
        pass

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
class DashClipboardUI(FigDMainWidget):
    def __init__(self, accent_color: str="purple"):
        super(DashClipboardUI, self).__init__()
        QApplication.clipboard().dataChanged.connect(
            self.onDataChanged
        )
        self.items = []
        self._sel_index = -1
        self._item_count = 0
        self._hidden_item_count = 0
        self.accent_color = accent_color
        # text edit for editing clipboard content.
        self.editor = DashClipboardEditArea(accent_color)
        self.editor.hide()
        # layout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")
        self.vboxlayout.setContentsMargins(10, 0, 10, 0)
        self.vboxlayout.setSpacing(0)
        # search bar.
        self.searchbar = self.initSearchBar(accent_color)
        self.searchbar.setObjectName("searchbar")
        # add control panel.
        self.ctrlPanel = self.initCtrlPanel()
        # spacers.
        spacer1 = QWidget()
        spacer2 = QWidget()
        spacer1.setFixedHeight(10)
        spacer2.setFixedHeight(10)
        # build layout.
        self.vboxlayout.addWidget(spacer1)
        self.vboxlayout.addWidget(self.ctrlPanel)
        self.vboxlayout.addWidget(self.searchbar)
        # central display stack.
        self.stack = self.initStack()
        self.stackArea = self.wrapInScrollArea(self.stack)        
        color = extractFromAccentColor(
            self.accent_color, 
            where="back"
        )
        self.stackArea.setStyleSheet("""
        QScrollArea {
            border: 7px solid """+color+""";
            border-top: none;
            border-bottom: none;
            background: transparent;
        }""")
        # self.stackArea.setMinimumHeight(150)
        self._se_splitter = QSplitter(Qt.Vertical)
        self._se_splitter.addWidget(self.stackArea)
        self._se_splitter.addWidget(self.editor)
        self._se_splitter.setSizes([200, 200])
        self.vboxlayout.addWidget(self._se_splitter)
        self.vboxlayout.addWidget(spacer2)
        # shortcuts.
        self.CtrlDel = FigDShortcut(QKeySequence("Ctrl+Del"), self, 
                                    "Clear all clipboard items (histroy)")
        self.CtrlDel.activated.connect(self.deleteAllItems)
        self.CtrlShiftS = FigDShortcut(QKeySequence("Ctrl+Shift+S"), self, 
                                       "Export clipboard history")
        self.CtrlShiftS.activated.connect(self.deleteAllItems)
        # set layout.
        self.setObjectName("DashClipboardUI")
        self.setLayout(self.vboxlayout)
        self.history = []
        # self.setStyleSheet("""
        # QWidget#DashClipboardUI {
        #     border-radius: 20px;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
        # }""")
    def __len__(self) -> int:
        """get length of visible clipboard items.
        Returns:
            int: number of visible clipboard items.
        """
        return self._item_count

    def count(self) -> int:
        """get count of number of items on the clipboard viewer.
        This includes invisible/hidden/deleted items too.
        Returns:
            int: number of total items (visible/invisible)
        """
        return self._item_count

    def initCtrlBtn(self, icon: str, text: Union[str, None]=None) -> QToolButton:
        btn = QToolButton()
        btn.setStyleSheet("""
        QToolButton {
            color: #fff;
            border-radius: 2px;
            font-size: 15px;
            padding-right: 0px;
            background: transparent;
            text-align: center;
        }
        QToolButton:hover {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #390b56, stop : 0.091 #420d64, stop : 0.182 #4c0f72, stop : 0.273 #561181, stop : 0.364 #601390, stop : 0.455 #6a169f, stop : 0.545 #7418ae, stop : 0.636 #7f1abe, stop : 0.727 #891cce, stop : 0.818 #941ede, stop : 0.909 #9f20ee, stop : 1.0 #aa22ff);
        }""")
        btn.setIcon(FigD.Icon(icon))
        btn.setIconSize(QSize(27,27))
        if text:
            btn.setText(text)
            btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        return btn

    def initCtrlPanel(self):
        ctrlPanel = QWidget()
        ctrlPanel.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            padding: 5px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            background: """+self.accent_color+""";
            font-family: "Be Vietnam Pro";
        }""")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # create control buttons.
        self.copyBtn = self.initCtrlBtn("textedit/copy.svg", "COPY")
        self.copyTextBtn = self.initCtrlBtn("system/clipboard/copy_text.svg", "COPY TEXT") 
        self.copyImageBtn = self.initCtrlBtn("system/clipboard/copy_image.svg", "COPY IMAGE")
        self.copyBase64Btn = self.initCtrlBtn("system/clipboard/copy_base64.png", "COPY BASE64")  
        self.copyAsHTMLBtn = self.initCtrlBtn("system/clipboard/copy_as_html.svg", "COPY HTML")
        self.editItemBtn = self.initCtrlBtn("system/clipboard/edit_item.svg", "EDIT ITEM")
        self.saveBtn = self.initCtrlBtn("system/clipboard/save.svg", "EXPORT")
        self.deleteBtn = self.initCtrlBtn("system/clipboard/delete.svg", "DELETE")
        # connect to slots.
        self.copyBtn.clicked.connect(self.copySelectedItemContent)
        self.deleteBtn.clicked.connect(self.deleteSelectedItem)
        self.editItemBtn.clicked.connect(self.editor.toggle)
        # build control panel layout.
        layout.addWidget(self.copyBtn, 0, 0, Qt.AlignCenter)
        layout.addWidget(self.copyTextBtn, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.copyImageBtn, 0, 2, Qt.AlignCenter)
        layout.addWidget(self.copyBase64Btn, 0, 3, Qt.AlignCenter)
        layout.addWidget(self.copyAsHTMLBtn, 1, 0, Qt.AlignCenter)
        layout.addWidget(self.editItemBtn, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.saveBtn, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.deleteBtn, 1, 3, Qt.AlignCenter)
        # set layout
        ctrlPanel.setLayout(layout)
        ctrlPanel.setFixedHeight(70)

        return ctrlPanel

    def copySelectedItemContent(self):
        pass

    def deleteSelectedItem(self):
        pass

    def deleteAllItems(self):
        pass

    def contextMenuEvent(self, event):
        self.contextMenu = QMenu()
        self.contextMenu.addAction("Clear all items", self.deleteAllItems, QKeySequence("Ctrl+Del"))
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(FigD.Icon("system/clipboard/export.svg"), "Export",
                            self.exportHistory, QKeySequence("Ctrl+Shift+S"))
        self.exportAsMenu = self.contextMenu.addMenu("Export As")
        self.contextMenu.addAction(FigD.Icon("system/clipboard/urls.svg"), "Export all URLs   ",
                                   self.exportAllUrls, QKeySequence("Ctrl+Shift+U"))
        self.exportAsMenu = self.initExportAsMenu(self.exportAsMenu)
        self.exportAsMenu = styleContextMenu(self.exportAsMenu, accent_color=self.accent_color)
        self.contextMenu = styleContextMenu(self.contextMenu, accent_color=self.accent_color)
        self.contextMenu.popup(event.globalPos())

    def initExportAsMenu(self, menu: QMenu) -> QMenu:
        menu.addAction(FigD.Icon("mimetypes/text-plain.svg"), "Plain Text    ",
                       partial(self.exportHistoryAs, "text/plain"), 
                       QKeySequence("Ctrl+Shift+S"))
        menu.addAction(FigD.Icon("mimetypes/application-vnd.ms-excel.svg"), "Excel")
        menu.addAction(FigD.Icon("mimetypes/text-csv.svg"), "CSV")
        menu.addAction("TSV")
        menu.addAction(FigD.Icon("mimetypes/text-html.svg"), "HTML")
        menu.addAction(FigD.Icon("mimetypes/application-pdf.svg"), "PDF")

        return menu

    def exportHistoryAs(self, filetype: str):
        pass

    def exportAllUrls(self):
        pass

    def exportHistory(self):
        pass

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

    def initSearchBar(self, accent_color: str="purple"):
        color = extractFromAccentColor(
            accent_color, where="back"
        )
        searcharea = QWidget()
        searcharea.setStyleSheet("""
        QWidget {
            border: 7px solid """+color+""";
            border-top: none;
            border-bottom: none;
        }""")
        layout = QHBoxLayout()
        # layout.addWidget(blank_left)
        layout.setContentsMargins(0, 10, 0, 10)
        # layout.addWidget(blank_right)
        searcharea.setLayout(layout)
        searchbar = DashClipboardSearchBar(
            accent_color=self.accent_color,
        )
        # layout.addStretch(1)
        layout.addWidget(searchbar)
        # layout.addStretch(1)

        return searcharea

    def onSelectionChanged(self, i: int):
        self.items[self._sel_index].deselect()
        self.editor.setText("")
        self.items[i].select()
        self._sel_index = i
        self.editor.setText(self.items[i].content)

    def onDataChanged(self):
        """When clipboard data is changed"""
        clipboard = QApplication.clipboard()
        mimedata = clipboard.mimeData()
        formats = mimedata.formats()
        if mimedata.hasImage():
            pixmap = clipboard.pixmap()
            text = clipboard.text()
            clipboard_item = self.append(self._item_count, pixmap, base64_str=text)
        else: 
            text = clipboard.text()
            clipboard_item = self.append(self._item_count, text)
        # print(f"clipboard_item: {clipboard_item}")
        if self._sel_index != -1:
            self.items[self._sel_index].deselect()
        if clipboard_item is not None:
            clipboard_item.select() # select a clipboard item.
            self._sel_index = self._item_count # change selected index 
            self.items.append(clipboard_item) # add to clipboard items array.
            if isinstance(clipboard_item.content, str):
                self.editor.setText(clipboard_item.content)
            else:
                self.editor.setText(f"can't edit clipboard content of type '{type(clipboard_item.content)}'")
            clipboard_item.selected.connect(self.onSelectionChanged)
            clipboard_item.editItem.connect(self.editor.show)
        self._item_count += 1
        # print("mimedata text:", mimedata.text())
        print("mimedata formats:", mimedata.formats())
        print("mimedata has text:", mimedata.hasText())
        print("mimedata has urls:", mimedata.hasUrls())
        print("mimedata has html:", mimedata.hasHtml())
        print("mimedata has color:", mimedata.hasColor())
        print("mimedata has image:", mimedata.hasImage())

    def initClipboardItem(self, i: int, item: Union[str, QImage]):
        item = DashClipboardItem(i, item, accent_color=self.accent_color)
        
        return item

    def append(self, i: int, text_or_pixmap: Union[str, QImage, QPixmap], base64_str=None):
        global CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD
        clipboard_item = None
        if isinstance(text_or_pixmap, str):
            text = text_or_pixmap
        elif isinstance(text_or_pixmap, (QPixmap, QImage)):
            text = base64_str
            text_or_pixmap = text_or_pixmap.scaled(
                300, 300, Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        # print(f"\x1b[31;1mui.system.clipboard::DashClipboardUI::append\x1b[0m({text})")
        self.history.append(text)
        if CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD:
            CLIPBOARD_COPY_ITEM_BUT_DONT_RECORD = False
        else:
            clipboard_item = self.initClipboardItem(i, text_or_pixmap)
            self.stackLayout.insertWidget(0, clipboard_item)
        # print([c.objectName() for c in self.children()])
        return clipboard_item

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
                            title="Clipboard Manager", width=550,
                            height=700, accent_color=accent_color,
                            add_tabs=False, app_name="Clipboard Manager")
    # show the app window.
    window.show()
    # run the application!
    app.exec()

def launch_clipboard():
    icon = FigDSystemAppIconMap["clipboard"]
    accent_color = FigDAccentColorMap["clipboard"]
    clipboard = DashClipboardUI(accent_color=accent_color)
    window = wrapFigDWindow(clipboard, size=(25,25), width=550,
                            title="Clipboard Manager", height=400,
                            icon=icon, accent_color=accent_color,
                            add_tabs=False, app_name="Clipboard Manager")
    window.show()


if __name__ == "__main__":
    test_clipboard()
    # def initCtrlPanel(self):
    #     ctrlPanel = QWidget()
    #     ctrlPanel.setStyleSheet("""
    #     QWidget {
    #         color: #fff;
    #         border: 0px;
    #         padding: 10px;
    #         border-top-left-radius: 15px;
    #         border-top-right-radius: 15px;
    #         background: """+self.accent_color+""";
    #         font-family: "Be Vietnam Pro";
    #     }""")
    #     layout = QHBoxLayout()
    #     layout.setContentsMargins(0, 0, 0, 0)
    #     layout.setSpacing(2)
    #     # create control buttons.
    #     self.copyBtn = self.initCtrlBtn("textedit/copy.svg")
    #     self.copyTextBtn = self.initCtrlBtn("system/clipboard/copy_text.svg") 
    #     self.copyAsHTMLBtn = self.initCtrlBtn("system/clipboard/copy_as_html.svg")
    #     self.editItemBtn = self.initCtrlBtn("system/clipboard/edit_item.svg")
    #     self.saveBtn = self.initCtrlBtn("system/clipboard/save.svg")
    #     self.deleteBtn = self.initCtrlBtn("system/clipboard/delete.svg")
    #     # connect to slots.
    #     self.copyBtn.clicked.connect(self.copyItemContent)
    #     self.deleteBtn.clicked.connect(self.deleteItem)
    #     # build control panel layout.
    #     layout.addStretch(1)
    #     layout.addWidget(self.copyBtn)
    #     layout.addWidget(self.copyTextBtn)
    #     layout.addWidget(self.copyAsHTMLBtn)
    #     layout.addWidget(self.editItemBtn)
    #     layout.addWidget(self.saveBtn)
    #     layout.addWidget(self.deleteBtn)
    #     # add stretch to control panel.
    #     layout.addStretch(1)
    #     # set layout
    #     ctrlPanel.setLayout(layout)
    #     ctrlPanel.setFixedHeight(40)

    #     return ctrlPanel