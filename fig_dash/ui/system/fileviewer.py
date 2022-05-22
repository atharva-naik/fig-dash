#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# the fig-dash fileviewer is known as the "orchard".
import os
import time
import jinja2
import socket
import getpass
from typing import *
from pathlib import Path
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.utils import h_format_mem
from fig_dash.ui.browser import DebugWebView
from fig_dash.api.js.system import SystemHandler
from fig_dash.ui.js.webchannel import QWebChannelJS
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
from fig_dash.ui import wrapFigDWindow, styleContextMenu, FigDAppContainer, FigDShortcut
from fig_dash.api.system.file.applications import MimeTypeDefaults, DesktopFile
# PyQt5 imports
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence, QPalette
from PyQt5.QtCore import Qt, QSize, QFileInfo, QUrl, QMimeDatabase, pyqtSlot, pyqtSignal, QObject, QThread, QFileSystemWatcher
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QErrorMessage, QLabel, QLineEdit, QToolBar, QMenu, QToolButton, QSizePolicy, QFrame, QAction, QActionGroup, QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsDropShadowEffect, QFileIconProvider, QSlider, QComboBox, QCompleter, QDirModel, QScrollArea
# filweviewer widget.

# IMPORTANT: URL to share page on 
# twitter
# https://twitter.com/intent/tweet?url={enc_page_url}&text=#{enc_page_title}
# facebook
# https://www.facebook.com/sharer/sharer.php?u={enc_url}
# linkedin
# https://www.linkedin.com/sharing/share-offsite/?url={enc_url}
FILE_VIEWER_CACHE_PATH = os.path.expanduser("~/.cache/fig_dash/fileviewer/thumbnails")
class EventHandler(QObject):
    def __init__(self, fileviewer):
        super(EventHandler, self).__init__()
        self.fileviewer = fileviewer

    @pyqtSlot(str)
    def sendClickedItem(self, path: str):
        # print(f"selected path {path}")
        self.fileviewer.updateSelection(path)

    @pyqtSlot(str)
    def sendOpenRequest(self, path: str):
        # print(f"opened path {path}")
        self.fileviewer.open(path)

    @pyqtSlot(str)
    def triggerContextMenu(self, path: str):
        # self.fileviewer.webview.menu = self.fileviewer.webview.itemMenu
        print(f"context menu triggered for {path}")

    @pyqtSlot(str, str)
    def triggerRename(self, id: str, new_name: str):
        new_name = new_name.strip()
        self.fileviewer.renameItem(id, new_name)
        

fileviewer_searchbar_style = jinja2.Template('''
QLineEdit {
    border: 0px;
    font-size: 17px;
    font-family: 'Be Vietnam Pro', sans-serif;
    padding-top: 3px;
    padding-bottom: 3px;
    color: #fff; /* #ad3700; */
    /* background: qlineargradient(x1 : 1, y1 : 0, x2 : 0, y2: 0, stop: 0 #828282, stop: 0.5 #eee, stop: 1 #828282); */
    background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
    border-radius: {{ BORDER_RADIUS }};
}
QLabel {
    font-size: 16px;
}''')
class FileViewerFolderSearchBar(QLineEdit):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(FileViewerFolderSearchBar, self).__init__(parent)
        # search action.
        self.searchAction = QAction()
        self.searchAction.setIcon(FigD.Icon("system/fileviewer/folder_search.svg"))
        self.addAction(self.searchAction, self.LeadingPosition)
        # match case.
        self.caseAction = QAction()
        self.caseAction.setIcon(
            FigD.Icon("system/fileviewer/case.svg")
        )
        self.addAction(self.caseAction, self.TrailingPosition)
        # self.matchWholeAction.setIcon(
        #     FigD.Icon("system/fileviewer/match_whole.svg")
        # )
        # match prefix.
        self.prefixAction = QAction()
        self.prefixAction.setIcon(
            FigD.Icon("system/fileviewer/prefix.svg")
        )
        self.addAction(self.prefixAction, self.TrailingPosition)
        # match suffix.
        self.suffixAction = QAction()
        self.suffixAction.setIcon(
            FigD.Icon("system/fileviewer/suffix.svg")
        )
        self.addAction(self.suffixAction, self.TrailingPosition)
        # # match contains.
        # self.containsAction = QAction()
        # self.containsAction.setIcon(
        #     FigD.Icon("system/fileviewer/match_contains.svg")
        # )
        # self.addAction(self.containsAction, self.TrailingPosition)
        self.setStyleSheet(fileviewer_searchbar_style.render(
            BORDER_RADIUS=16,
        ))
        self.setFixedHeight(28)
        self.setClearButtonEnabled(True)
        self.returnPressed.connect(self.search)
        # completion for search.
        self.completer = QCompleter()
        self.completer.setModel(QDirModel(self.completer))
        self.completer.popup().setStyleSheet("""font-family: 'Be Vietnam Pro', sans-serif; color: #fff; background: #000; border: 0px;""")
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # self.completer.setFilterMode(Qt.MatchContains)
        self.setCompleter(self.completer)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def search(self):
        pass
        # print("searched")

# Thumbnailer for files,
class PyMuPdfThumbnailer:
    """
    uses PyMuPdf or "fitz" to generate thumbnails for pdfs.
    """
    def __init__(self):
        pass

    def saveThumbnail(self, path: str, save_path: str):
        import fitz
        import fitz.fitz
        try:
            doc = fitz.open(path)
            thumbnail_page = doc.load_page(0)
            pixmap = thumbnail_page.get_pixmap()
            pixmap.save(save_path)
        except fitz.fitz.EmptyFileError as e:
            print(f"\x1b[31;1mui::system::fileviewer::PyMuPdfThumbnailer.getThumbnail raised fitz.fitz.EmptyFileError\x1b[0m", e)
        except fitz.fitz.FileNotFoundError as e:
            print(f"\x1b[31;1mui::system::fileviewer::PyMuPdfThumbnailer.getThumbnail raised fitz.fitz.FileNotFoundError\x1b[0m", e)

# File viewer thumbnailing backend worker.
class FileViewerThumbnailer(QObject):
    """generate thumbnails for video files, 3D objects and pdfs."""
    finished = pyqtSignal()
    progress = pyqtSignal(str, str)
    def __init__(self, cache_path: str=FILE_VIEWER_CACHE_PATH):
        super(FileViewerThumbnailer, self).__init__()
        self.__thumbnailers = {
            "application/pdf": PyMuPdfThumbnailer(),
        }
        self.__cache_path = os.path.expanduser(cache_path)
        # create caching folder in case it doesn't exist.
        os.makedirs(self.__cache_path, exist_ok=True)
        self.__file_path = None

    def setBackend(self, backend, thumb_types: List[str]=[]):
        for thumb_type in thumb_types:
            self.__thumbnailers[thumb_type] = backend

    def queueFile(self, path: str, thumb_type: str="application/pdf", icon_size: int=50):
        self.__file_path = path
        self.__icon_size = icon_size
        self.__thumb_type = thumb_type

    def generateThumbnail(self) -> None:
        """
        Generate thumbnail for a pdf/3d object or video file given the absolute path, cache it at the folder pointed to by `cache_path`.
        """
        import fitz
        import fitz.fitz
        if self.__file_path is None:
            print("file path not set")
            return
        path = self.__file_path
        path = os.path.expanduser(path)
        # check if file is already cached.
        filename = path.replace("/", "|")
        cached_file_path = os.path.join(
            self.__cache_path, 
            filename + ".png",
        )
        # check if thumbnail for a particular file has been cached, just fecth it's path if it is cached.
        if os.path.exists(cached_file_path):
            self.progress.emit(path, cached_file_path)
            self.finished.emit()
            return
        # fetch backend for a particular mimetype.
        backend = self.__thumbnailers.get(self.__thumb_type)
        if backend: 
            # NOTE: this is a blocking call by design
            # save and cache the image object as generated by the backend.
            backend.saveThumbnail(path, cached_file_path)
            self.progress.emit(path, cached_file_path)
        else: 
            # if no backend is available for this thumbnail mimetype, then give up.
            self.progress.emit(path, "None")
        self.finished.emit()
        

# statusbar for file viewer.
class FileViewerStatus(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 webview: Union[DebugWebView, None]=None):
        super(FileViewerStatus, self).__init__(parent)    
        self.webview = webview
        # horizontal layout.
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)    
        # thumbnailer workers and threads.

        self.selected = self.initBtn(icon="file.svg", text=" selected: None") # name of seelcted item.
        self.num_items = self.initBtn(icon="item.png", text="(contains 0 items)") # number of items in selected item 
        self.file_size = self.initBtn(icon="storage.svg", text=" 0kB") # size of selected item
        self.breakdown = QLabel("0 items (0 files, 0 folders, 0 hidden)")
        # self.user = self.initBtn(icon="user.svg", text=" "+getpass.getuser())
        self.hostname = self.initBtn(icon="server.svg", text=f" {socket.gethostname()}@{getpass.getuser()}")
        self.owner = self.initBtn(icon="owner.svg", text=" <user>")
        self.group = self.initBtn(icon="group.svg", text=" <group>")
        self.permissions = self.initBtn(icon="permissions.svg", text="[RWX]")
        self.symlink = self.initBtn(icon=None, text=None)
        self.shortcut = self.initBtn(icon=None, text=None)
        # add widgets.
        self.layout.addWidget(self.breakdown)
        # self.layout.addWidget(self.user)
        self.layout.addWidget(self.hostname)
        self.layout.addStretch(1)
        self.layout.addWidget(self.selected)
        self.layout.addWidget(self.num_items)
        self.layout.addWidget(self.file_size)
        self.layout.addWidget(self.owner)
        self.layout.addWidget(self.group)
        self.layout.addWidget(self.permissions)
        self.layout.addWidget(self.symlink)
        self.layout.addWidget(self.shortcut)
        # set layout and style
        self.setLayout(self.layout)
        self.setObjectName("CodeMirrorStatus")
        self.setStyleSheet('''
        QWidget#CodeMirrorStatus {
            color: #fff;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QLabel {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }''')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def updateSelected(self, **data):
        size = data.get("size", 0)
        icon = data.get("icon", "")
        name = data.get("name", "")
        items = data.get("items", 0)
        
        owner = data.get("owner")
        group = data.get("group")
        last_read = data.get("last_read")
        permissions = data.get("permissions")
        last_modified = data.get("last_modified")
        meta_change_time = data.get("meta_change_time")
        
        shortcut = data.get("shortcut", False)
        symbolic = data.get("symbolic", False)
        if symbolic:
            print("is a symlink")
            self.symlink.setIcon(FigD.Icon("system/fileviewer/symlink.svg"))
        if shortcut:
            print("is a shortcut")
            self.shortcut.setIcon(FigD.Icon("system/fileviewer/shortcut.png"))

        self.selected.setText(f" selected: {name}")
        self.file_size.setText(f" {size}")
        self.permissions.setText(f" {permissions}")
        self.owner.setText(f" {owner}")
        self.group.setText(f" {group}")
        # self.last_read.setText()
        # self.last_modified.setText()
        # self.

        if icon != "":
            self.selected.setIcon(QIcon(icon))
        if items != 0:
            self.num_items.setText(f"(contains {items} items)")
        else:
            self.num_items.setText("")

    def updateBreakdown(self, **data):
        items = data.get("items", 0)
        files = data.get("files", 0)
        hidden = data.get("hidden", 0)
        folders = data.get("folders", 0)
        self.breakdown.setText(f"{items} items ({files} files, {folders} folders, {hidden} hidden)")

    def initBtn(self, icon=None, text=None):
        btn = QToolButton(self)
        if icon: 
            icon = os.path.join("system/fileviewer", icon)
            btn.setIcon(FigD.Icon(icon))
        if text: btn.setText(text)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setStyleSheet("background: #292929; color: #fff;")
        btn.setStyleSheet('''
        QToolButton {
            color: #6e6e6e;
            border: 0px;
            font-family: 'Be Vietnam Pro', sans-serif;
            font-size: 16px;
            background: transparent;
        }
        QToolButton:hover {
            border: 0px;
            background: rgba(0, 0, 0, 0.5);
        }''')

        return btn


class FileViewerWebView(DebugWebView):
    '''fileviewer web view'''
    def __init__(self, accent_color="yellow"):
        super(FileViewerWebView, self).__init__()
        self.orchardMenu = QMenu()
        self.orchardMenu.addAction("New Folder")
        self.orchardMenu.addAction("New File")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Restore Missing Files...")
        self.orchardMenu.addAction("Open in Terminal")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Paste")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Properties")

        self.accent_color = accent_color
        self.orchardMenu = styleContextMenu(
            self.orchardMenu, 
            accent_color=accent_color
        )

    def initItemMenu(self, mimetype="folder"):
        self.itemMenu = QMenu()
        self.itemMenu.addAction(FigD.Icon("tray/open.svg"), "Open With default")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(FigD.Icon("tray/open.svg"), "Open With")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction("Cut")
        self.itemMenu.addAction(FigD.Icon("browser/copy.svg"), "Copy")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction("Move To...")
        self.itemMenu.addAction("Copy To...")
        self.itemMenu.addAction(FigD.Icon("system/fileviewer/link.svg"), "Make Link")
        self.itemMenu.addAction("Rename...")
        # if mimetype == ""
            # self.itemMenu.addAction("Set as Wallpaper")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(FigD.Icon("tabbar/trash.svg"), "Move to Trash")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction("Revert to Previous Version...")
        self.itemMenu.addAction("Compress...")
        self.itemMenu.addAction("Email...")
        self.itemMenu.addSeparator()
        self.itemMenu.addAction("Properties") 
        self.itemMenu = styleContextMenu(
            self.itemMenu, 
            accent_color=self.accent_color
        )

        return self.itemMenu       

    def dragEnterEvent(self, e):
        e.ignore()
    # def itemContextMenuEvent(self, event):
    #     '''show item specific context menu (for the selected item)'''
    #     self.itemMenu.popup(event.globalPos())
    def contextMenuEvent(self, event):
        '''show the orchared context menu (not specific to a selected item)'''
        data = self.page().contextMenuData()
        print(data)
        # print(dir(event))
        if data.mediaType() == 0:
            self.orchardMenu.popup(event.globalPos())
        elif data.mediaType() == 1:
            # print(self.widget.selected_item)
            self.itemMenu = self.initItemMenu()
            self.itemMenu.popup(event.globalPos())

    def connectWidget(self, widget):
        self.widget = widget
        # New folder action.
        self.orchardMenu.actions()[0].triggered.connect(
            lambda: widget.createDialogue(item_type="folder")
        )
        # New file action.
        self.orchardMenu.actions()[1].triggered.connect(
            lambda: widget.createDialogue(item_type="file")
        )

    def initiateRenameForId(self, id: str):
        '''make the span displaying the item_name editanle for the selected item'''
        code = f'''selectedItemElement = document.getElementById('{id}');
selectedItemSpan = selectedItemElement.getElementsByClassName('item_name')[0];
// selectedItemSpan
selectedItemSpan.setAttribute('contenteditable', 'true');
selectedItemSpan.style.backgroundColor = "white";
selectedItemSpan.style.color = "black";
selectedItemSpan.focus()
document.execCommand('selectAll', false, null);
document.getSelection().collapseToEnd();
selectedItemSpan.addEventListener('keypress', handleItemRename);
'''        
        # print(code)
        self.page().runJavaScript(code)

    def createItem(self, path: str, name: str, 
                  icon: str, hidden: bool=False):
        '''
        Create a file item from arguments:
        path (or id of the div): the exact file location.
        name: the displayed file name.
        icon: the icon for the file item.
        hidden: whether the file is hidden or displayed.
        '''
        hidden = 1 if hidden else 0
        code = f'''
        var newItemDivElement = createItem('{path}', '{name}', '{icon}', {hidden}); // create the new file item.
        orchard.prepend(newItemDivElement); // add the new file item to the green boxes section which is marked by the 'orchard' id.
        '''
        self.page().runJavaScript(code)

#eb5f34
file_viewer_btn_style = jinja2.Template('''
QToolButton {
    color: #fff;
    border: 0px;
    font-size: 14px;
    text-align: center;
    background: {{ background }};
}
QToolButton:hover {
    color: #292929;
    border: 1px solid #0a4c70;
    border-radius: 2px;
    background: rgba(105, 191, 238, 150);
    /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0); */
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}''')
file_viewer_responsive_btn_style = '''
QToolButton {
    color: #fff;
    border: 0px;
    font-size: 14px;
    background: transparent;
}
QToolButton:hover {
    color: #69bfee;
}
QToolTip {
    color: #fff;
    border: 0px;
    background: #000;
}'''
class FileViewerBtn(QToolButton):
    '''File viewer button'''
    def __init__(self, parent: Union[None, QWidget]=None, **args):
        super(FileViewerBtn, self).__init__(parent)
        tip = args.get("tip", "a tip")
        size = args.get("size", (23,23))
        icon = args.get("icon")
        text = args.get("text")
        style = args.get("style")
        self.hover_response = "background"
        if icon:
            self.inactive_icon = os.path.join("system/fileviewer", args["icon"])
            stem, ext = os.path.splitext(Path(args["icon"]))
            active_icon = f"{stem}_active{ext}"
            self.active_icon = os.path.join("system/fileviewer", active_icon)
            if os.path.exists(FigD.icon(self.active_icon)):
                self.hover_response = "foreground"
            self.setIcon(FigD.Icon(self.inactive_icon))
        if text: self.setText(args["text"])
        if style: self.setToolButtonStyle(style)
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStatusTip(tip)
        # stylesheet attributes.
        background = args.get("background", "transparent")
        # print(font_size)
        if self.hover_response == "background":
            self.setStyleSheet(
                file_viewer_btn_style.render(
                    background=background,
                )
            )
        else:
            self.setStyleSheet(file_viewer_responsive_btn_style)

    def leaveEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.inactive_icon))
        super(FileViewerBtn, self).leaveEvent(event)

    def enterEvent(self, event):
        if self.hover_response == "foreground":
            self.setIcon(FigD.Icon(self.active_icon))
        super(FileViewerBtn, self).enterEvent(event)


class FileViewerGroup(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None,
                 name: str="Widget Group"):
        super(FileViewerGroup, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.group = QWidget()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(2)
        self.group.setLayout(self.layout)
        self.setStyleSheet("""
        QWidget#FileViewerGroup {
            border: 0px;
            margin-left: 5px;
            margin-right: 5px;
            background: transparent;
        }""")
        self.setObjectName("FileViewerGroup")
        layout.addStretch(1)
        layout.addWidget(self.group)
        layout.addWidget(self.Label(name))
        self.setLayout(layout)

    def initLabel(self, text: str):
        lbl = QLabel(text)
        lbl.setStyleSheet("""
        QLabel {
            color: #fff;
            border: 0px;
            font-size: 14px;
            background: transparent;
        }""")

        return lbl

    def Label(self, name):
        name = QLabel(name)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet('''
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e;
            /* color: #69bfee; */
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
            padding-bottom: 0px;
        }''')
        self.groupNameLabel = name

        return name

    def initBtnGrid(self, btn_args, spacing=None, 
                    alignment_flag=None):
        btnGrid = QWidget()
        btnGrid.btns = []
        layout = QGridLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        if spacing:
            layout.setSpacing(spacing)
        else: layout.setSpacing(0)
        btnGrid.setLayout(layout)
        btnGrid.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }""")
        
        for i, btn_row_args in enumerate(btn_args):
            for j, args in enumerate(btn_row_args):
                islabel = args.get("label", False)
                stretch = args.get("stretch", False)
                
                if stretch: layout.addStretch(1)
                elif islabel:
                    text = args.get("text", "text not set")
                    label = QLabel(text)
                    label.setStyleSheet("""
                    QLabel {
                        color: #fff;
                        border: 0px;
                        font-size: 14px;
                        background: transparent;
                    }""")
                    layout.addWidget(label)
                else:
                    btn = self.initBtn(**args)
                    btnGrid.btns.append(btn)
                    if alignment_flag is None:
                        layout.addWidget(
                            btn, i, j,
                            alignment=Qt.AlignCenter
                        )
                    else:
                        layout.addWidget(
                            btn, i, j,
                            alignment=alignment_flag
                        )
        scrollArea = self.wrapInScrollArea(btnGrid)
        scrollArea.grid = btnGrid

        return scrollArea

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        # scrollArea.setAttribute(Qt.WA_TranslucentBackground)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("border: 2px solid gray;")
        # scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scrollArea.setStyleSheet("""
        # QScrollArea {
        #     border: 0px;
        #     background: blue;
        # }""")
        return scrollArea

    def initBtnGroup(self, btn_args, orient="horizontal", 
                     alignment_flag=None, spacing=None):
        btnGroup = QWidget()
        btnGroup.btns = []
        if orient == "horizontal":
            layout = QHBoxLayout()
        elif orient == "vertical":
            layout = QVBoxLayout()
        if spacing is not None:
            # print("setting spacing")
            layout.setSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)
        btnGroup.layout = layout
        btnGroup.setLayout(layout)
        btnGroup.setStyleSheet('''
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }''')
        layout.addStretch(1)
        for args in btn_args:
            stretch = args.get("stretch", False)
            islabel = args.get("label", False)
            if stretch:
                layout.addStretch(1)
            elif islabel:
                text = args.get("text", "text not set")
                label = QLabel(text)
                label.setStyleSheet("""
                QLabel {
                    color: #fff;
                    border: 0px;
                    font-size: 14px;
                    background: transparent;
                }""")
                layout.addWidget(label)
            else:
                btn = self.initBtn(**args)
                btnGroup.btns.append(btn)
                if alignment_flag is None:
                    layout.addWidget(btn, 0, Qt.AlignCenter)
                else:
                    layout.addWidget(btn, 0, alignment_flag)
        layout.addStretch(1)
        btnGroup.setLayout(layout)

        return btnGroup

    def setBackgroundColor(self, color):
        palette = self.palette()
        if isinstance(color, str): 
            color = QColor(color)
        elif isinstance(color, tuple): 
            color = QColor(*color)
        palette.setColor(QPalette.Window, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def enterEvent(self, event):
        """on entering highlight the group's background and it's name"""
        # print("\x1b[34;1menterEvent\x1b[0m")
        self.setBackgroundColor((255,255,255,50))
        self.groupNameLabel.setStyleSheet("""
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #69bfee;
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
            padding-bottom: 0px;
        }""")
        super(FileViewerGroup, self).enterEvent(event)

    def leaveEvent(self, event):
        """on exiting restore the group's default styling"""
        # print("\x1b[34;1mleaveEvent\x1b[0m")
        self.setBackgroundColor((255,255,255,0))
        self.groupNameLabel.setStyleSheet("""
        QLabel {
            border: 0px;
            border-right: 1px;
            padding: 6px;
            color: #6e6e6e;
            font-size: 16px;
            font-family: 'Be Vietnam Pro', sans-serif;
            background: transparent;
            padding-bottom: 0px;
        }""")
        super(FileViewerGroup, self).leaveEvent(event)

    def initBtn(self, **args):
        return FileViewerBtn(self, **args)
        # btn = QToolButton(self)
        # tip = args.get("tip", "a tip")
        # size = args.get("size", (23,23))
        # if "icon" in args:
        #     icon = os.path.join("system/fileviewer", args["icon"])
        #     btn.setIcon(FigD.Icon(icon))
        # elif "text" in args:
        #     btn.setText(args["text"])
        # btn.setIconSize(QSize(*size))
        # btn.setToolTip(tip)
        # btn.setStatusTip(tip)
        # btn.setStyleSheet('''
        # QToolButton {
        #     color: #fff;
        #     border: 0px;
        #     font-size: 14px;
        #     background: transparent;
        # }
        # QToolButton:hover {
        #     color: #292929;
        #     background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34);
        # }
        # QToolTip {
        #     color: #fff;
        #     border: 0px;
        #     background: #000;
        # }''')

        # return btn 
# backdrop-filter: drop-shadow(4px 4px 10px blue);
# backdrop-filter: hue-rotate(120deg);
class FileViewerFileGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerFileGroup, self).__init__(parent, "File")
        # file creation widget.
        self.creationWidget = QWidget()
        self.creationLayout = QVBoxLayout()
        self.creationLayout.setContentsMargins(0, 0, 0, 0)
        self.creationWidget.setLayout(self.creationLayout)
        self.newFileBtn =  self.initBtn(
            icon="file.ico",#"new_file.svg",
            size=(30,30),
            text="New\nFile",
            tip="create a new file",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.newFolderBtn =  self.initBtn(
            icon="folder.ico",#"new_folder.svg",
            size=(30,30),
            text="New\nFolder",
            tip="create a new folder",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.creationLayout.addWidget(self.newFileBtn, 0, Qt.AlignLeft)
        self.creationLayout.addWidget(self.newFolderBtn, 0, Qt.AlignLeft)
        self.creationLayout.addStretch(1)
        # connect to server.
        self.connectToServerBtn = self.initBtn(
            icon="connect_to_server.ico",
            text="connect\nto server",
            size=(40,40),
            tip="connect to a server",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.linkGroup = self.initBtnGroup([
            {"icon": "link.svg", "size": (20,20), "text": "link", "style": Qt.ToolButtonTextBesideIcon},
            {"icon": "unlink.svg", "size": (20,20), "text": "unlink", "tip": "move selected item(s) to trash", "style": Qt.ToolButtonTextBesideIcon},
        ], spacing=0)
        
        # copied from path widget.
        # path copying tools.
        self.pathWidget = QWidget()
        self.pathLayout = QVBoxLayout()
        self.pathLayout.setContentsMargins(0, 0, 0, 0)
        self.pathLayout.setSpacing(0)
        self.pathWidget.setLayout(self.pathLayout)
        # path navigation tools.
        self.navWidget = QWidget()
        self.navLayout = QVBoxLayout()
        self.navLayout.setContentsMargins(0, 0, 0, 0)
        self.navLayout.setSpacing(0)
        self.navWidget.setLayout(self.navLayout)
        # buttons.
        self.backPathBtn = self.initBtn(
            icon="back.ico",
            size=(25,25),
            tip="go back to parent folder",
        )
        self.copyPathBtn =  self.initBtn(
            icon="copy_filepath.png",
            size=(25,25),
            text="copy path",
            tip="copy filepath",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.copyNameBtn = self.initBtn(
            icon="copy_filename.svg",
            size=(25,25),
            text="copy name",
            tip="copy filename",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.copyUrlBtn =  self.initBtn(
            icon="copy_as_url.svg",
            text="copy as url",
            size=(25,25),
            tip="copy file path as url",
            style=Qt.ToolButtonTextBesideIcon,
        )
        self.stemBtn = self.initBtn(
            text="stem", size=(25,25),
            tip="copy file name without extension",
        )
        self.extBtn = self.initBtn(
            text=".ext", size=(25,25),
            tip="copy extension of file",
        )
        self.pathLayout.addWidget(self.copyPathBtn)
        self.pathLayout.addWidget(self.copyNameBtn)
        self.pathLayout.addWidget(self.copyUrlBtn)
        self.pathLayout.addStretch(1)

        self.navLayout.addStretch(1)
        self.navLayout.addWidget(self.backPathBtn)
        self.navLayout.addWidget(self.stemBtn)
        self.navLayout.addWidget(self.extBtn)

        self.linkNServer = QWidget()
        self.linkNServerLayout = QVBoxLayout()
        self.linkNServerLayout.setContentsMargins(0, 0, 0, 0)
        self.linkNServer.setLayout(self.linkNServerLayout)
        self.linkNServerLayout.addWidget(self.connectToServerBtn)
        self.linkNServerLayout.addWidget(self.linkGroup)
        self.layout.addWidget(self.creationWidget)
        self.layout.addWidget(self.linkNServer)
        self.layout.addWidget(self.pathWidget)
        self.layout.addWidget(self.navWidget)

    def updateExt(self, ext: str):
        '''update extension layout.'''
        self.extBtn.setText(ext)

    def connectWidget(self, widget):
        self.widget = widget
        # self.newFileBtn.clicked.connect(widget.createFile)
        self.newFolderBtn.clicked.connect(
            lambda: widget.createDialogue(item_type="folder")
        )
        self.newFileBtn.clicked.connect(
            lambda: widget.createDialogue(item_type="file")
        )
        self.backPathBtn.clicked.connect(widget.openParent)
        self.stemBtn.clicked.connect(widget.copyStemToClipboard)
        self.copyUrlBtn.clicked.connect(widget.copyUrlToClipboard)
        self.copyNameBtn.clicked.connect(widget.copyNameToClipboard)
        self.copyPathBtn.clicked.connect(widget.copyPathToClipboard)
        self.extBtn.clicked.connect(
            lambda: widget.copyToClipboard(self.extBtn.text())
        )
# class FileViewerPathGroup(FileViewerGroup):
#     def __init__(self, parent: Union[None, QWidget]=None):
#         super(FileViewerPathGroup, self).__init__(parent, "Path")
#         # just to convert to VBox Layout.
#         # path copying tools.
#         self.pathWidget = QWidget()
#         self.pathLayout = QVBoxLayout()
#         self.pathLayout.setContentsMargins(0, 0, 0, 0)
#         self.pathLayout.setSpacing(0)
#         self.pathWidget.setLayout(self.pathLayout)
#         # path navigation tools.
#         self.navWidget = QWidget()
#         self.navLayout = QVBoxLayout()
#         self.navLayout.setContentsMargins(0, 0, 0, 0)
#         self.navLayout.setSpacing(0)
#         self.navWidget.setLayout(self.navLayout)
#         # buttons.
#         self.backPathBtn = self.initBtn(
#             icon="back.svg",
#             size=(25,25),
#             tip="go back to parent folder",
#         )
#         self.copyPathBtn =  self.initBtn(
#             icon="copy_filepath.png",
#             size=(25,25),
#             tip="copy filepath",
#         )
#         self.copyNameBtn = self.initBtn(
#             icon="copy_filename.svg",
#             size=(25,25),
#             tip="copy filename",
#         )
#         self.copyUrlBtn =  self.initBtn(
#             icon="copy_as_url.svg",
#             size=(25,25),
#             tip="copy file path as url",
#         )
#         self.stemBtn = self.initBtn(
#             text="stem", size=(25,25),
#             tip="copy file name without extension",
#         )
#         self.extBtn = self.initBtn(
#             text=".ext", size=(25,25),
#             tip="copy extension of file",
#         )
#         self.pathLayout.addWidget(self.copyPathBtn)
#         self.pathLayout.addWidget(self.copyNameBtn)
#         self.pathLayout.addWidget(self.copyUrlBtn)
#         self.pathLayout.addStretch(1)

#         self.navLayout.addStretch(1)
#         self.navLayout.addWidget(self.backPathBtn)
#         self.navLayout.addWidget(self.stemBtn)
#         self.navLayout.addWidget(self.extBtn)
        
#         self.layout.addStretch(1)
#         self.layout.addWidget(self.pathWidget)
#         self.layout.addWidget(self.navWidget)
#         self.layout.addStretch(1)

#     def updateExt(self, ext: str):
#         '''update extension layout.'''
#         self.extBtn.setText(ext)

#     def connectWidget(self, widget):
#         self.backPathBtn.clicked.connect(widget.openParent)
#         self.copyUrlBtn.clicked.connect(widget.copyUrlToClipboard)
#         self.copyNameBtn.clicked.connect(widget.copyNameToClipboard)
#         self.copyPathBtn.clicked.connect(widget.copyPathToClipboard)
#         self.extBtn.clicked.connect(
#             lambda: widget.copyToClipboard(self.extBtn.text())
#         )
class FileViewerEditGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerEditGroup, self).__init__(parent, "Edit")
        self.editWidget = QWidget()
        self.editWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding) 
        self.editLayout = QVBoxLayout()
        self.editLayout.setSpacing(0)
        self.editLayout.setContentsMargins(0, 0, 0, 0)
        # undo, redo, rename
        self.renameGroup = self.initBtnGroup([
            {"icon": "undo.svg", "size": (23,23), "tip": "undo rename", "text": "undo", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "rename.ico", "size": (23,23), "tip": "rename file/folder", "text": "rename", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "redo.svg", "size": (23,23) , "tip": "redo rename", "text": "redo", "style": Qt.ToolButtonTextUnderIcon},
        ], spacing=0)
        self.undoBtn = self.renameGroup.btns[0]
        self.renameBtn = self.renameGroup.btns[1]
        self.redoBtn = self.renameGroup.btns[2]
        # cut, copy, paste
        self.moveGroup = self.initBtnGroup([
            {"icon": "cut.png", "size": (23,23), "tip": "cut selected item", "text": "cut", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "copy.svg", "size": (30,30), "tip": "copy selected items",  "text": "copy", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "paste.png", "size": (32,32), "tip": "paste selected items from the clipboard", "text": "paste", "style": Qt.ToolButtonTextUnderIcon},
        ], spacing=0, alignment_flag=Qt.AlignCenter | Qt.AlignBottom)
        # make link, release link, move to trash
        self.linkGroup = self.initBtnGroup([
            {"stretch": True},
            {"icon": "trash.svg", "size": (40,40), "tip": "move selected item(s) to trash", "text": "trash", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "invert_selection.ico", "size": (30,30), "tip": "invert selected items", "icon_size": (30,30)},
        ], orient="vertical", spacing=0)

        self.selectionGroup1 = self.initBtnGroup([
            {"icon": "clear_selection.ico", "size": (30,30), "tip": "clear current selection", "icon_size": (30,30)},
            {"icon": "select_all.ico", "size": (30,30), "tip": "select all items", "icon_size": (30,30)},
        ], orient="vertical", spacing=0)
        self.invertBtn = self.linkGroup.btns[1]
        self.clearBtn = self.selectionGroup1.btns[0]
        self.selectAllBtn = self.selectionGroup1.btns[1]
        # self.layout.addWidget(self.invertBtn, 0, Qt.AlignBottom)
        # self.sortWidget = QWidget()
        # self.editLayout.addStretch(1)
        self.editLayout.addWidget(self.renameGroup)
        self.editLayout.addWidget(self.moveGroup)
        # self.editLayout.addStretch(1)
        self.editWidget.setLayout(self.editLayout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.editWidget)
        self.layout.addWidget(self.linkGroup, 0, Qt.AlignBottom)
        self.layout.addWidget(self.selectionGroup1, 0, Qt.AlignBottom)
        self.layout.addStretch(1)    

    def connectWidget(self, widget):
        self.widget = widget
        self.renameBtn.clicked.connect(widget.renameDialog)
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)


class FileViewerViewGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerViewGroup, self).__init__(parent, "View")
        self.viewWidget = QWidget() 
        self.viewLayout = QVBoxLayout()
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        # layout of file items
        self.layoutGroup = self.initBtnGroup([
            {"icon": "gridview.svg", "size": (20,20), "tip": "tile view", "text": "grid", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "list_view.svg", "size": (20,20), "tip": "list view", "text": "list", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "treelistview.svg", "size": (20,20), "tip": "tree view", "text": "tree", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "toggle_hidden_files.ico", "size": (23,23), "tip": "toggle visibility of hidden files"},
        ], spacing=0)
        # sort by / show options.
        self.sortOptionsGroup = self.initBtnGroup([
            {"icon": "options.ico", "size": (40,40), "tip": "show options in file list"},
            {"icon": "sort_by.ico", "size": (30,30), "tip": "sort by attribute", "text": "sort by", "style": Qt.ToolButtonTextUnderIcon},
        ], spacing=0, orient="vertical")
        # column add/fit
        self.columnsGroup = self.initBtnGroup([
            {"icon": "add_columns.ico", "size": (35,35), "tip": "add columns to file list", "text": "add", "style": Qt.ToolButtonTextBesideIcon},
            {"icon": "fit_columns.ico", "size": (35,35), "tip": "fit columns into view", "text": " fit", "style": Qt.ToolButtonTextBesideIcon},
        ], spacing=0, orient="vertical", alignment_flag=Qt.AlignLeft)
        # hidden files, folder bar visibility, side bar visibility, search bar visibility.
        self.visibilityGroup = self.initBtnGroup([
            {"icon": "toggle_folderbar.svg", "size": (35,35), "tip": "toggle visibility of folder bar"},
            {"icon": "toggle_searchbar.ico", "size": (27,27), "tip": "toggle visibility of search bar"},
            {"icon": "toggle_sidebar.svg", "size": (27,27), "tip": "toggle visibility of sidebar"},
        ], spacing=0)
        self.hiddenFilesBtn = self.layoutGroup.btns[-1]
        self.folderbarBtn = self.visibilityGroup.btns[0]
        self.searchbarBtn = self.visibilityGroup.btns[1]
        self.sidebarBtn = self.visibilityGroup.btns[2]
        self.arrangeGroup = self.initBtnGroup([
            {"icon": "sidebar_left.ico", "size": (25,25), "tip": "sidebar to the left", "text": " left", "style": Qt.ToolButtonTextBesideIcon, "font_size": 10},
            {"icon": "sidebar_right.png", "size": (25,25), "tip": "sidebar to the right", "text": " right", "style": Qt.ToolButtonTextBesideIcon, "font_size": 10},
        ], orient="vertical", spacing=0, alignment_flag=Qt.AlignLeft)     
        self.viewLayout.addStretch(1)
        self.viewLayout.addWidget(self.layoutGroup)
        self.viewLayout.addWidget(self.visibilityGroup)
        # self.viewLayout.addWidget(self.arrangeGroup)
        self.viewWidget.setLayout(self.viewLayout)
        # self.layout.addStretch(1)
        self.layout.addWidget(self.viewWidget)
        self.layout.addWidget(self.sortOptionsGroup)
        self.layout.addWidget(self.columnsGroup)
        self.layout.addWidget(self.arrangeGroup)
        # self.layout.addStretch(1)    
    def connectWidget(self, widget):
        self.widget = widget
        self.folderbarBtn.clicked.connect(
            widget.folderbar.toggle
        )
        self.sidebarBtn.clicked.connect(
            widget.sideArea.toggle
        )

        self.hiddenFilesBtn.clicked.connect(
            widget.toggleHiddenFiles
        )
        self.searchbarBtn.clicked.connect(
            widget.foldersearchbar.toggle
        )


class FileViewerSelectGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerSelectGroup, self).__init__(parent, "Select")
        self.selectionGroup1 = self.initBtnGroup([
            {"icon": "clear_selection.ico", "size": (30,30), "tip": "clear current selection", "icon_size": (30,30)},
            {"icon": "select_all.ico", "size": (30,30), "tip": "select all items", "icon_size": (30,30)},
        ], orient="vertical", spacing=0)
        self.invertBtn = self.initBtn(
            icon="invert_selection.ico", size=(30,30), 
            tip="invert selected items", icon_size=(30,30)
        )
        self.clearBtn = self.selectionGroup1.btns[0]
        self.selectAllBtn = self.selectionGroup1.btns[1]
        self.layout.addWidget(self.selectionGroup1, 0, Qt.AlignBottom)
        self.layout.addWidget(self.invertBtn, 0, Qt.AlignBottom)
 
    def connectWidget(self, widget):
        self.widget = widget
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)


class XdgOpenDropdown(QComboBox):
    '''Dropdown of available applications for opening file of particular type.'''
    def __init__(self, mimetype: str):
        super(XdgOpenDropdown, self).__init__()
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.lineEdit().textChanged.connect(self.adjustCursor)
        self.mime_to_apps = MimeTypeDefaults()
        self.populate(mimetype)
        self.currentIndexChanged.connect(self.selChanged)
        # self.setStyleSheet("")
        self.setStyleSheet("background: #292929; color: #69bfee; font-size: 15px; text-align: left;")

    def adjustCursor(self):
        '''adjust cursor to the starting position.'''
        self.lineEdit().setCursorPosition(0)

    def connectWidget(self, widget: QWidget):
        self.widget = widget
        self.clearBtn.clicked.connect(widget.clearSelection)
        self.selectAllBtn.clicked.connect(widget.selectAll)
        self.invertBtn.clicked.connect(widget.invertSelection)

    def getAppsList(self, mimetype: str):
        '''get list of apps available for a given mimetype.'''
        apps = self.mime_to_apps(mimetype)
        # print(mimetype)
        self.desktop_files = []
        app_names = []
        for app in apps:
            desktop_file = DesktopFile(app)
            # desktop_file.read()
            self.desktop_files.append(desktop_file)
            # print(desktop_file)
            app_names.append(desktop_file.app_name)

        return app_names

    def xdgOpen(self, file: str):
        '''use xdg-open on a specific file'''
        os.system(f'xdg-open "{file}"')

    def gtkLaunch(self, app: str, file: str=""):
        '''do a gtk launch of a specific application with or without a specific file.'''
        # os.system(f"gtk-launch {app} '{file}'")
        # print(f"gtk-launch {app} '{file}'")
    def open(self, file):
        i = self.currentIndex()
        self.gtkLaunch(self.apps[i], file)

    def populate(self, mimetype: str):
        # clear combox box.
        # get list of available apps.
        self.clear()
        self.apps = self.getAppsList(mimetype)
        for app in self.apps:
            self.addItem(app)

    def selChanged(self, index: int):
        '''selected application (for xdg-open) is changed.'''
        # print(index, self.apps)
        appSelected = self.apps[index]
        # print(appSelected)

class FileViewerOpenGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerOpenGroup, self).__init__(parent, "Open")
        self.xdgOpenWidget = self.initXdgOpenWidget()
        # opener widget.
        self.openerGroup = self.initBtnGroup([
            {"icon": "terminal.svg", "size":(40,40),
            'tip': "open in terminal"},
            {"icon": "browser.svg", "size":(40,40),
            'tip': "open in browser"},
        ], orient="vertical", spacing=0)
        self.terminalBtn = self.openerGroup.btns[0]
        self.browserBtn = self.openerGroup.btns[1]

        self.layout.addStretch(1)
        self.layout.addWidget(self.xdgOpenWidget)
        self.layout.addWidget(self.openerGroup)
        self.layout.addStretch(1)   

    def updateMimeBtn(self, mimetype: str, 
                      icon: QIcon, path: str):
        self.mimeBtn.setText(mimetype)
        # self.mimeBtn.setToolTip(tip)
        # self.mimeBtn.setStatusTip(tip)
        self.mimeBtn.setIcon(QIcon(icon))
        self.mimeBtn.setIconSize(QSize(35,35))
        self.appDropdown.populate(mimetype)
        self.mimeBtn.clicked.connect(lambda: self.appDropdown.open(path))

    def initXdgOpenWidget(self):
        '''change xdg-open settings.'''
        xdgOpenWidget = QWidget() 
        xdgOpenLayout = QVBoxLayout()
        xdgOpenLayout.setContentsMargins(0, 0, 0, 0)
        xdgOpenLayout.setSpacing(0)
        # # open with label.
        # label = QLabel("Open With")
        # label.setStyleSheet('''
        # QLabel {
        #     color: #ccc;
        #     border: 0px;
        #     padding: 2px;
        #     font-size: 13px;
        #     font-weight: bold;
        #     font-family: 'Be Vietnam Pro', sans-serif;
        #     background: transparent;
        # }''')
        tip = "open selected file with selected app"
        icon = os.path.join(
            "system/fileviewer", 
            "file.svg"
        )
        self.mimeBtn = QToolButton()
        self.mimeBtn.setToolTip(tip)
        self.mimeBtn.setStatusTip(tip)
        self.mimeBtn.setText("text/plain")
        self.mimeBtn.setIcon(FigD.Icon(icon))
        self.mimeBtn.setIconSize(QSize(35,35))
        self.mimeBtn.setStyleSheet(file_viewer_btn_style.render(
            background="transparent"
        ))
        self.mimeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # app selection dropdown.
        self.appDropdown = XdgOpenDropdown("text/plain")
        self.appDropdown.setFixedWidth(130)
        self.appDropdown.setFixedHeight(24)
        # self.mimeBtn.clicked.connect(
        #     lambda: os.system(f"gtk-launch {} {self.selected_item}")
        # )
        xdgOpenLayout.addWidget(self.mimeBtn, 0, Qt.AlignCenter)
        # xdgOpenLayout.addWidget(label, 0, Qt.AlignCenter)
        xdgOpenLayout.addWidget(self.appDropdown)
        xdgOpenWidget.setLayout(xdgOpenLayout)

        return xdgOpenWidget

class FileViewerShareGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerShareGroup, self).__init__(parent, "Share")
        # QR, devices, bluetooth, email, copy to clipboard (contents)
        # twitter, reddit, facebook, youtube, instagram
        self.nativeGroup1 = self.initBtnGroup([
            {"icon": "devices.svg", "size":(18,18),
            'tip': "share to linked devices"},
            {"icon": "qr.svg", "size":(18,18),
            'tip': "create qr code for file"},
            {"icon": "bluetooth.svg", "size":(18,18),
            'tip': "share using bluetooth"},
        ], spacing=0, alignment_flag=Qt.AlignLeft)
        self.nativeGroup2 = self.initBtnGroup([
            {"icon": "email.ico", "size":(36,30),
            'tip': "share file as email attachment", "text": "email", "style": Qt.ToolButtonTextUnderIcon},
            {"icon": "copy_content.svg", "size":(18,18),
            'tip': "copy file contents to clipboard", "text": "content", "style": Qt.ToolButtonTextUnderIcon}
        ], orient="vertical", spacing=0)
        self.shareGroup = self.initBtnGrid([
            [
                {"icon": "youtube.png", "size":(35,35),
                'tip': "share video on youtube"},
                {"icon": "twitter.png", "size":(35,35),
                'tip': "share on twitter"},
                {"icon": "reddit.png", "size":(35,35),
                'tip': "share on reddit"},                
            ],
            [
                {"icon": "facebook.png", "size":(35,35),
                'tip': "share on facebook"},
                {"icon": "instagram.png", "size":(35,35),
                'tip': "share image on instagram"},
                {"icon": "whatsapp.png", "size":(35,35),
                'tip': "share on whatsapp"},  
            ],
        ])
        shareGrid = self.shareGroup.grid
        shareGrid.setStyleSheet("""
        QWidget {
            color: #fff;
            border: 0px;
            font-size: 10px;
            background: transparent;
        }""")
        self.shareGroup.setFixedHeight(65)
        self.shareGroup.setFixedWidth(135)
        # self.appsGroup1 = self.initBtnGroup([
        #     {"icon": "facebook.png", "size":(28,28),
        #     'tip': "share on facebook"},
        #     {"icon": "instagram.png", "size":(28,28),
        #     'tip': "share image on instagram"},
        #     {"icon": "whatsapp.png", "size":(28,28),
        #     'tip': "share on whatsapp"},
        # ], spacing=0, alignment_flag=Qt.AlignBottom)
        # self.appsGroup2 = self.initBtnGroup([
        #     {"icon": "facebook.png", "size":(28,28),
        #     'tip': "share on facebook"},
        #     {"icon": "instagram.png", "size":(28,28),
        #     'tip': "share image on instagram"},
        #     {"icon": "whatsapp.png", "size":(28,28),
        #     'tip': "share on whatsapp"},
        # ], spacing=0, alignment_flag=Qt.AlignBottom)
        self.shareWidget = QWidget()
        self.shareLayout = QVBoxLayout()
        self.shareLayout.setSpacing(0)
        self.shareLayout.setContentsMargins(0, 0, 0, 0)
        
        self.shareLabel = QLabel()
        self.shareLabel.setText("share online")
        self.shareLabel.setStyleSheet("""
        QLabel {
            color: #fff;
            font-size: 14px;
            background: transparent;
        }""")
        self.shareLayout.addStretch(1)
        # self.shareLayout.addWidget(self.appsGroup1, 0, Qt.AlignLeft)
        # self.shareLayout.addWidget(self.appsGroup2, 0, Qt.AlignLeft)
        # self.shareLayout.addWidget(self.shareLabel, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.shareLayout.addWidget(self.shareGroup, 0, Qt.AlignVCenter | Qt.AlignCenter)
        self.shareLayout.addWidget(self.nativeGroup1, 0, Qt.AlignLeft | Qt.AlignVCenter)
        # self.shareLayout.addStretch(1)
        self.shareWidget.setLayout(self.shareLayout)

        self.layout.addStretch(1)
        # self.layout.addWidget(self.nativeGroup1)
        self.layout.addWidget(self.nativeGroup2)
        self.layout.addWidget(self.shareWidget)
        self.layout.addStretch(1)   
# class FileViewerPropGroup(QWidget): # change permissions, owner, group, thumbnailer
# class FileViewerFilterGroup(QWidget):
class FileViewerBackupGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerBackupGroup, self).__init__(parent, "Backup") # backup, VCS


class FileViewerMiscGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerMiscGroup, self).__init__(parent, "Misc")
        # self.tagsGroup = self.initBtnGroup()
        # self.notesGroup = self.initBtnGroup()
        # self.ratingsGroup = self.initBtnGroup()
        # self.favoritesGroup = self.initBtnGroup()
        # self.bookmarksGroup = self.initBtnGroup()
        # self.fileconvertGroup = self.initBtnGroup()
        self.cloudStorageGroup = self.initBtnGroup([
            {"icon": "gdrive.png", "size": (30,30), "tip": "open google drive UI"},
            {"icon": "dropbox.png", "size": (30,30), "tip": "open dropbox UI"},
            # {"label": True, "text": "cloud"},
        ], orient="horizontal", spacing=0)
        self.ratingsGroup = self.initBtnGroup([
            {"icon": "rate.ico", "size": (30,30), "tip": "open ratings panel for selected item"},
            {"icon": "show_rating.ico", "size": (30,30), "tip": "show ratings for all items"},

        ], spacing=0)
        self.encryptionGroup = self.initBtnGroup([
            {"icon": "key.png", "size": (30,30), "tip": "decrypt file"},
            {"icon": "lock.ico", "size": (30,30), "tip": "encrypt file"},
        ], orient="horizontal", spacing=0)
        self.compressionGroup = self.initBtnGroup([
            {"icon": "zip.ico", "size": (30,30), "tip": "zip file"},
            {"icon": "compress.svg", "size": (30,30), "tip": "compression tools", "text": "archive", "style": Qt.ToolButtonTextUnderIcon},
        ], orient="vertical", spacing=0)
        self.miscWidget1 = QWidget()
        self.miscLayout1 = QVBoxLayout()
        self.miscLayout1.setSpacing(0)
        self.miscLayout1.setContentsMargins(0, 0, 0, 0)

        self.miscWidget2 = QWidget()
        self.miscLayout2 = QVBoxLayout()
        self.miscLayout2.setSpacing(0)
        self.miscLayout2.setContentsMargins(0, 0, 0, 0)
        
        self.miscLayout1.addStretch(1)
        self.miscLayout1.addWidget(self.encryptionGroup, 0, Qt.AlignLeft)
        self.miscLayout1.addWidget(self.initLabel("encrypt"), 0, Qt.AlignCenter)
        self.miscLayout1.addWidget(self.ratingsGroup, 0, Qt.AlignLeft)
        self.miscLayout1.addWidget(self.initLabel("rate"), 0, Qt.AlignCenter)
        self.miscWidget1.setLayout(self.miscLayout1)

        self.miscLayout2.addStretch(1)
        self.miscLayout2.addWidget(self.cloudStorageGroup, 0, Qt.AlignLeft)
        self.miscLayout2.addWidget(self.initLabel("cloud"), 0, Qt.AlignCenter)
        # self.miscLayout2.addWidget(self.ratingsGroup, 0, Qt.AlignLeft)
        # self.miscLayout2.addWidget(self.initLabel("rate"), 0, Qt.AlignCenter)
        self.miscWidget2.setLayout(self.miscLayout2)
        # add widgets to layout.
        self.layout.addWidget(self.compressionGroup)
        self.layout.addWidget(self.miscWidget1)
        self.layout.addWidget(self.miscWidget2)
        # self.coversionGroup # file conversion (for images, videos, document formats etc.)
    def connectWidget(self, widget):
        self.widget = widget


class AppearanceSlider(QWidget):
    def __init__(self, icon: str="", orient: str="horizontal", 
                 initial_value: float=1, tip: str=""):
        super(AppearanceSlider, self).__init__()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLineEdit()
        self.label.setText(str(initial_value))
        self.label.returnPressed.connect(self.setSliderByLabel)
        self.slider = QSlider()
        if orient == "vertical":
            self.slider.setOrientation(Qt.Vertical)
        else:
            self.slider.setOrientation(Qt.Horizontal)
        self.icon = QLabel()
        path = FigD.icon(
            os.path.join("system/fileviewer", icon)
        )
        self.slider.setMaximumWidth(50)
        self.slider.valueChanged.connect(self.sliderAction)
        pixmap = QPixmap(path)
        if icon.endswith(".png"):
            pixmap = pixmap.scaled(
                QSize(20,20), 
                aspectRatioMode=Qt.KeepAspectRatio,
                transformMode=Qt.SmoothTransformation,
            )
        # pixmap = pixmap.scaled(QSize(20,20))
        self.icon.setPixmap(pixmap)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.label.setMaximumWidth(30)
        self.label.setStyleSheet('''
        QLineEdit {
            color: #eb5f34;
            font-size: 14px;
        }''')
        self.js_func  = None
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.setLayout(self.layout)

    def connectWidget(self, js_func):
        '''connect JS functionality'''
        self.js_func = js_func

    def sliderAction(self, value):
        self.label.setText(f"{1+value:.0f}")
        if self.js_func:
            self.js_func()

    def setSliderByLabel(self):
        '''set slider value when return is pressed in the line edit.'''
        try: value = int(self.label.text())
        except ValueError: value = 0
        self.slider.setValue(value)
# oa.set('backdrop-filter', 'brightness(0.3) sepia(0.7)')
# oa.setBrightness(0.5)
class FileViewerBlankGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerBlankGroup, self).__init__(parent,  "")
        self.layout.addStretch(1)
        self.setFixedWidth(400)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
class FileViewerAppearanceGroup(FileViewerGroup):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerAppearanceGroup, self).__init__(parent, "Appearance")
        VBox = QWidget()
        HBox = QWidget()
        Box3 = QWidget()
        VBox.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        HBox.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        Box3.setStyleSheet("background: rgba(29, 29, 29, 0.7); border: 0px;")
        HLayout = QVBoxLayout()
        HLayout.setContentsMargins(0, 0, 0, 0)
        VLayout = QVBoxLayout()
        VLayout.setContentsMargins(0, 0, 0, 0)
        Layout3 = QVBoxLayout()
        Layout3.setContentsMargins(0, 0, 0, 0)
        self.brightnessSlider = AppearanceSlider(
            icon="brightness.svg",
            tip="set background brightness",
        )
        self.blurRadiusSlider = AppearanceSlider(
            icon="blur.svg",
            tip="set background blur radius",
        )
        self.contrastSlider = AppearanceSlider(
            icon="contrast.svg",
            tip="set background contrast",
        )
        self.hueRotateSlider = AppearanceSlider(
            icon="hue.png",
            tip="set hue rotation",
        )
        self.grayScaleSlider = AppearanceSlider(
            icon="grayscale.png",
            tip="set gray scale amount",
        )
        self.saturateSlider = AppearanceSlider(
            icon="saturation.png",
            tip="set background saturation",
        )
        self.invertSlider = AppearanceSlider(
            icon="invert.svg",
            tip="invert background image color scheme",
        )
        self.opacitySlider = AppearanceSlider(
            icon="opacity.svg",
            tip="set background opacity",
        )
        self.sepiaSlider = AppearanceSlider(
            icon="sepia.png",
            tip="apply sepia filter",
        )
        self.backgroundImageBtn = self.initBtn(
            icon="background-image.png",
            tip="change background image"
        )
        # horizontal sliders box.
        VLayout.addWidget(self.brightnessSlider)
        VLayout.addWidget(self.blurRadiusSlider)
        VLayout.addWidget(self.contrastSlider)
        VLayout.addWidget(self.invertSlider)
        VBox.setLayout(VLayout)
        # vertical sliders box.
        HLayout.addWidget(self.hueRotateSlider)
        HLayout.addWidget(self.grayScaleSlider)
        HLayout.addWidget(self.opacitySlider)
        HLayout.addWidget(self.sepiaSlider)
        HBox.setLayout(HLayout)
        # 3rd vertical box.
        Layout3.addWidget(self.backgroundImageBtn, 0, Qt.AlignCenter)
        Layout3.addWidget(self.saturateSlider)
        Box3.setLayout(Layout3)

        self.layout.addStretch(1)
        self.layout.addWidget(VBox)
        self.layout.addWidget(HBox)
        self.layout.addWidget(Box3)
        self.layout.addStretch(1)

    def initBtn(self, icon: str, tip: str=""):
        btn = QToolButton(self)
        btn.setIconSize(QSize(30,30))
        path = os.path.join(
            "system/fileviewer", icon
        )
        btn.setIcon(FigD.Icon(path))
        # btn.setText("background\nimage")
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 12px;
            text-align: center;
            background: transparent;
        }
        QToolButton:hover {
            border: 1px solid #bf3636;
            background: #a11f53aa;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
        }''')
        # btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setToolTip(tip)
        btn.setStatusTip(tip)

        return btn

    def connectWidget(self, widget):
        self.widget = widget

# don't need class FileViewerMoveGroup(QWidget):
class FileViewerMenu(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerMenu, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # direct access to mime database and icon provider.
        self.mime_database = QMimeDatabase()
        self.icon_provider = QFileIconProvider()
        self.scroll_area_ptr = None

        self.filegroup = FileViewerFileGroup()
        # self.pathgroup = FileViewerPathGroup()
        self.editgroup = FileViewerEditGroup()
        self.viewgroup = FileViewerViewGroup()
        self.opengroup = FileViewerOpenGroup()
        self.miscgroup = FileViewerMiscGroup()
        self.sharegroup = FileViewerShareGroup()
        self.blankgroup = FileViewerBlankGroup()
        # self.appearancegroup = FileViewerAppearanceGroup()
        self.layout.addWidget(self.filegroup)
        # self.layout.addWidget(self.addSeparator())
        # self.layout.addWidget(self.pathgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.editgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.viewgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.opengroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.sharegroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.miscgroup)
        self.layout.addWidget(self.addSeparator())
        self.layout.addWidget(self.blankgroup)

        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)
    # def addSeparator(self, width: Union[None, int]=None):
    #     sep = QFrame()
    #     sep.setFrameShape(QFrame.VLine)
    #     sep.setFrameShadow(QFrame.Sunken)
    #     sep.setStyleSheet('''background: #292929;''')
    #     sep.setLineWidth(1)
    #     # sep.setMaximumHeight(90)
    #     if width: 
    #         sep.setFixedWidth(width)
    #     return sep
    def addSeparator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet(f'''background: #292929;''')
        sep.setLineWidth(1)
        sep.setMaximumHeight(110)

        return sep

    def toggle(self):
        print("\x1b[34;1mtoggling menu\x1b[0m")
        if self.scroll_area_ptr:
            self.scroll_area_ptr.toggle()

    def connectWidget(self, widget):
        self.filegroup.connectWidget(widget)
        self.editgroup.connectWidget(widget)
        self.viewgroup.connectWidget(widget)
        self.miscgroup.connectWidget(widget)
        # self.pathgroup.connectWidget(widget)
        # self.opengroup.connectWidget(widget)
        # self.appearancegroup.connectWidget(widget)
class ToggleScrollArea(QScrollArea):
    def __init__(self):
        super(ToggleScrollArea, self).__init__()

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

def wrapInScrollArea(widget):
    scrollArea = ToggleScrollArea()
    scrollArea.setWidget(widget)
    scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    widget.scroll_area_ptr = scrollArea

    return scrollArea

class FileViewerFolderBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerFolderBar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.path = ""
        
        self.setLayout(self.layout)
        self.setObjectName("FileViewerFolderBar")
        self.selectedIndex = 0 
        self.folderBtns = []
        self.folderBtnStyle = '''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 17px;
            font-weight: bold;
            font-family: 'Be Vietnam Pro', sans-serif;
            padding-top: 2px;
            padding-bottom: 2px;
            border-radius: 3px;
            background: #484848;
            margin-left: 1px;
            margin-right: 1px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
        }
        QToolButton:hover {
            color: #292929;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''
        self.folderBtnSelStyle = '''
        QToolButton {
            border: 0px;
            color: #292929;
            font-size: 17px;
            font-weight: bold;
            font-family: 'Be Vietnam Pro', sans-serif;
            padding-top: 2px;
            padding-bottom: 2px;
            border-radius: 3px;
            margin-left: 1px;
            margin-right: 1px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''
        self.backBtn = self.initFolderNavBtn(
            icon="prev.svg",
            tip="go back (tied to webview.back)",
        )
        self.forwardBtn = self.initFolderNavBtn(
            icon="next.svg",
            tip="go forward (tied to webview.forward)",
        )
        self.backBtn.setFixedHeight(24)
        self.forwardBtn.setFixedHeight(24)

    def toggle(self):
        print("toggling folderbar visibility")
        if self.isVisible():
            self.hide()
        else: self.show()

    def __len__(self):
        return len(self.folderBtns)+3

    def addSpacer(self):
        widget = QWidget()
        # widget.setAttribute(Qt.WA_TranslucentBackground)
        widget.setStyleSheet("background: transparent;")
        # widget.setStyleSheet("background: red;")
        widget.setFixedWidth(10)
        self.layout.insertWidget(0, widget)

    def clear(self):
        '''clear all the folder buttons on the folder bar.'''
        for i in reversed(range(len(self))): # print(i)
            try: self.layout.itemAt(i).widget().setParent(None)
            except AttributeError as e: 
                print(f"fileviewer.FileViewerFolderBar.clear({i}):", e)

    def getSubPaths(self, path):
        sub_paths = []
        path = Path(path)
        while str(path) != "/":
            sub_paths.append((str(path)))
            path = path.parent

        return ["/"]+sub_paths[::-1]

    def setPath(self, path):
        if self.path.startswith(path):
            for i, sub_path in enumerate(self.getSubPaths(path)):
                if sub_path == path: break
            self.folderBtns[self.selectedIndex].setStyleSheet(self.folderBtnStyle)
            self.folderBtns[i].setStyleSheet(self.folderBtnSelStyle)
            self.selectedIndex = i
            return
        # clear layout
        self.clear()
        # change the recorded deepest path till now.
        self.path = path
        path = Path(path)
        self.folderBtns = []

        items = []
        while str(path) != "/":
            items.append((str(path.name), str(path)))
            path = path.parent
        items.append(("/", "/"))
        # items = items[::-1]
        self.selectedIndex = len(items)-1
        for name, path in items:
            btn = self.initFolderBtn(name, path)
            self.layout.insertWidget(0, btn)
            self.folderBtns.append(btn)
        
        self.folderBtns = self.folderBtns[::-1]
        self.folderBtns[-1].setStyleSheet(self.folderBtnSelStyle)
        self.layout.addStretch(1)
        self.addSpacer()
        self.layout.insertWidget(0, self.forwardBtn)
        self.layout.insertWidget(0, self.backBtn)

    def connectWidget(self, widget):
        self.widget = widget
        self.backBtn.clicked.connect(
            widget.webview.back
        )
        self.forwardBtn.clicked.connect(
            widget.webview.forward
        )

    def initFolderNavBtn(self, icon: str, 
                         tip: str="some tip"):
        btn = QToolButton(self)
        tip = tip
        btn.setToolTip(tip)
        icon = os.path.join("system/fileviewer", icon)
        btn.setIcon(FigD.Icon(icon))
        btn.setStyleSheet(self.folderBtnStyle)
        btn.setFixedHeight(24)

        return btn 

    def initFolderBtn(self, name, full_path):
        btn = QToolButton(self)
        tip = f"got to {full_path}"
        btn.setToolTip(tip)
        if name == "/":
            btn.setIcon(FigD.Icon(
                "system/fileviewer/harddrive.png"
            ))
        else: btn.setText(name)
        if self.widget:
            btn.clicked.connect(
                lambda: self.widget.open(full_path)
            )
        btn.setStyleSheet(self.folderBtnStyle)
        btn.setFixedHeight(24)

        return btn 


class FileViewerShortcutBtn(QToolButton):
    '''File viewer shortcut button.'''
    def __init__(self, parent: Union[None, QWidget]=None, 
                 text: str="", icon: str="", path: str="",
                 size: Tuple[int, int]=(25,25),
                 tip: str=""):
        super(FileViewerShortcutBtn, self).__init__(parent)
        self.btnStyle = '''
        QToolButton {
            color: #fff;
            border: 0px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            padding-top: 5px;
            padding-left: 10px;
            padding-bottom: 5px;
            background: transparent;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1)); */
        }
        QToolButton:hover {
            color: #292929;
            border: 1px solid #0a4c70;
            background: rgba(105, 191, 238, 180);
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #147eb8, stop : 0.3 #69bfee, stop: 0.9 #338fc0);
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0.5, y2 : 1, stop : 0.1 #a11f53, stop : 0.3 #bf3636, stop: 0.9 #eb5f34); */
        }
        QToolTip {
            color: #fff;
            border: 0px;
            background: #000;
        }'''
        if text is None:
            text = Path(path).name
        self.setStyleSheet(self.btnStyle)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIcon(FigD.Icon(
            os.path.join("system/fileviewer", icon)
        ))
        self.setIconSize(QSize(*size))
        self.setText(3*" "+text)
        self.setToolTip(tip)
        self.setStatusTip(tip)
        self.path = path
        self.setFixedWidth(300)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    def connectWidget(self, widget):
        self.widget = widget
        self.clicked.connect(self.onClick)

    def onClick(self):
        self.widget.open(self.path)


class FileViewerSideBar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(FileViewerSideBar, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # shortcuts.
        self.shortcutBtns = []
        # bookmarks.
        self.bookmarkBtns = []
        home = os.path.expanduser("~")
        self.layout.setSpacing(0)
        self.recentBtn = self.initShortcutBtn(
            path=os.path.join(home, "Recent"),
            icon="recent.svg",
            tip=f"recently opened files",
            text="Recent",
        )
        self.homeBtn = self.initShortcutBtn(
            path=home,
            icon="home.svg",
            tip=f"open home folder ({home})",
            text="Home",
        )
        self.desktopBtn = self.initShortcutBtn(
            path=os.path.join(home, "Desktop"),
            icon="desktop.svg",
            tip="open desktop",
        )
        self.downloadsBtn = self.initShortcutBtn(
            path=os.path.join(home, "Downloads"),
            icon="downloads.svg",
            tip="open downloads",
        )
        self.documentsBtn = self.initShortcutBtn(
            path=os.path.join(home, "Documents"),
            icon="document.svg",
            tip="open documents folder",
        )
        self.musicBtn = self.initShortcutBtn(
            path=os.path.join(home, "Music"),
            icon="music.svg",
            tip="open music folder",
        )
        self.picturesBtn = self.initShortcutBtn(
            path=os.path.join(home, "Pictures"),
            icon="pictures.svg",
            tip="open pictures folder",
        )
        self.templatesBtn = self.initShortcutBtn(
            path=os.path.join(home, "Templates"),
            icon="templates.svg",
            tip="open templates folder",
        )
        # add buttons to layout.
        self.layout.addWidget(self.recentBtn)
        self.layout.addWidget(self.homeBtn)
        self.layout.addWidget(self.desktopBtn)
        self.layout.addWidget(self.documentsBtn)
        self.layout.addWidget(self.downloadsBtn)
        self.layout.addWidget(self.musicBtn)
        self.layout.addWidget(self.picturesBtn)
        self.layout.addWidget(self.templatesBtn)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def toggle(self):
        print("toggling folderbar visibility")
        if self.isVisible():
            self.hide()
        else: self.show()

    def addSeparator(self):
        pass

    def initShortcutBtn(self, path: str, 
                        icon: str, tip: str, 
                        text: Union[None, str]=None,
                        size: Tuple[int, int]=(25,25)):
        btn = FileViewerShortcutBtn(
            self, path=path, icon=icon,
            text=text, size=size, tip=tip,
        )
        self.shortcutBtns.append(btn)

        return btn
    # def initFavBtn(self, *args):
    #     pass
    # def initBookmarkBtn(self, path):
    #     name = Path(path).name
    #     btn = QToolButton(self)
    #     btn.setText(name)
    #     btn.setIcon(FigD.Icon("system/fileviewer/folder.svg"))
    #     btn.setToolTip(f"{path}")
    #     btn.setStyleSheet(self.btnStyle)
    #     btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    #     btn.path = path
    #     self.bookmarkBtns.append(btn)

    #     return btn
    def connectWidget(self, widget):
        self.widget = widget
        for btn in self.shortcutBtns:
            btn.connectWidget(widget)


class FileViewerOverviewPanel(QWidget):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(FileViewerOverviewPanel, self).__init__(parent)


class FileViewerKeyPressSearch(QLineEdit):
    def __init__(self):
        super(FileViewerKeyPressSearch, self).__init__()
        self.setStyleSheet("""
        QLineEdit {
            color: #000;
            background: #fff;
        }""")
        self.h, self.w = 30, 100
        self.setFixedWidth(self.w)
        self.setFixedHeight(self.h)

    def showPanel(self, parent, w: int, h: int):
        self.setParent(parent)
        self.move(w-self.w, h-self.h)
        self.setFocus()
        self.show()

    def connectWidget(self, widget):
        self.widget = widget
        self.textChanged.connect(self.widget.searchByFileName)


class FileViewerWidget(QMainWindow):
    def __init__(self, parent: Union[None, QWidget]=None, 
                 logo: Union[None, str, QIcon]=None, 
                 dangle_folderbar: bool=False,
                 zoom_factor: float=1.35, **args):
        super(FileViewerWidget, self).__init__(parent)
        self.thumbnail_thread_pool = []
        self.thumbnail_workers = []
        accent_color = args.get("accent_color", "blue")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.webview = FileViewerWebView(accent_color=accent_color)
        self.browser = self.webview
        self.zoom_factor = zoom_factor
        self.menu = FileViewerMenu()
        self.font_color = args.get("font_color", '#fff')
        # data
        # set logo.
        if isinstance(logo, QIcon):
            self.setWindowIcon(logo)
        elif isinstance(logo, str):
            print("FileViewerWidget logo:", logo)
            self.setWindowIcon(
                FigD.Icon("system/fileviewer/logo.svg")
            )
        self.background_image = QUrl.fromLocalFile(
            args.get("background")
        ).toString()
        self.file_watcher = QFileSystemWatcher()
        self.icon_provider = QFileIconProvider()
        self.mime_database = QMimeDatabase()
        self.showItemContextMenu = False
        self.loaded_file_items = []
        self.browsing_history = []
        self.selected_item = None
        self.hidden_visible = False
        self.file_watcher.directoryChanged.connect(self.reOpen)
        # handle click events (using click handler)
        self.channel = QWebChannel()
        self.eventHandler = EventHandler(fileviewer=self)
        self.channel.registerObject("eventHandler", self.eventHandler)
        self.systemHandler = SystemHandler()
        self.systemHandler.connectChannel(self.channel)
        self.webview.page().setWebChannel(self.channel)
        
        self.folderbar = FileViewerFolderBar()
        self.folderbar.setFixedHeight(30)
        # self.folderbar.hide()
        self.sidebar = FileViewerSideBar()
        self.sideArea = wrapInScrollArea(self.sidebar)
        self.sideArea.hide()
        self.overviewPanel = FileViewerOverviewPanel()
        self.overviewArea = wrapInScrollArea(self.overviewPanel)
        self.overviewArea
        # searchbar.
        self.foldersearchbar = FileViewerFolderSearchBar()
        self.foldersearchbar.hide()
        # self.searchbar.setParent(self.webview)
        self.foldersearchbar.setMinimumWidth(800)
        self.foldersearchbar.setFixedHeight(34)
        self.foldersearchbar.move(0,0)
        # statusbar.
        self.statusbar = FileViewerStatus(self, self.webview)
        # clipboard access.
        self.clipboard = args.get("clipboard")
        # connect to browser buttom.
        browserBtn = self.menu.opengroup.browserBtn
        browserBtn.clicked.connect(self.openFileInWebView)
        # # shortcuts.
        self.SelectAll = FigDShortcut(
            QKeySequence.SelectAll, self, 
            "Select all files/folders"
        )
        self.SelectAll.activated.connect(self.selectAll)
        self.BackSpace = FigDShortcut(
            QKeySequence("Backspace"), self,
            "Go back to parent folder"
        )
        self.BackSpace.activated.connect(self.openParent)
        self.CtrlH = FigDShortcut(
            QKeySequence("Ctrl+H"), self,
            "Toggle hidden files/folders"
        )
        self.CtrlH.activated.connect(self.toggleHiddenFiles)
        self.CtrlShiftF = FigDShortcut(
            QKeySequence("Ctrl+Shift+F"), self,
            "Open file explorer search bar"
        )
        self.CtrlShiftF.activated.connect(self.foldersearchbar.show)
        # self.SelectAll.setEnabled(False)
    
        # add the dev tools button to the view group.
        self.webview.devToolsBtn.setText("dev\ntools")
        self.webview.devToolsBtn.setIconSize(QSize(25,25))
        self.webview.devToolsBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.menu.viewgroup.arrangeGroup.layout.insertWidget(1, self.webview.devToolsBtn)
        # self.menu.viewgroup.arrangeGroup.layout.insertWidget(1, self.webview.pyDevToolsBtn)
        # self.layout.addWidget(self.webview.devToolsBtn)
        # add widgets to layout.
        self.layout.insertWidget(0, self.webview.splitter, 0)
        self.layout.insertWidget(0, self.foldersearchbar, 0, Qt.AlignCenter)
        if not dangle_folderbar:
            self.layout.insertWidget(0, self.folderbar, 0)
        # if args.get("parentless", False):
        #     self.menuArea = self.wrapInScrollArea(self.menu)
        #     self.menuArea.setFixedHeight(130)
        #     self.layout.insertWidget(0, self.menuArea)
        # else:
        #     self.layout.insertWidget(0, self.menu)
        self.menuArea = wrapInScrollArea(self.menu)
        self.menuArea.setFixedHeight(130)
        self.menuArea.hide()
        self.layout.insertWidget(0, self.menuArea)
        # self.layout.addStretch(1)

        self.webview.splitter.insertWidget(0, self.sideArea)
        self.webview.splitter.setSizes([200, 600, 200])
        self.webview.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.keypress_search = FileViewerKeyPressSearch()
        self.keypress_search.connectWidget(self)
        self.keypress_search.hide()

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet('''background: transparent; border: 0px; color: #fff;''')        
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.webview.urlChanged.connect(self.onUrlChange)
        
        self.menu.connectWidget(self)
        self.folderbar.connectWidget(self)
        self.webview.connectWidget(self)
        self.sidebar.connectWidget(self)
        # connect Esc key shortcut to Esc handler.
        self.webview.Esc.setEnabled(False)
        self.EscKey = FigDShortcut(
            QKeySequence("Esc"), self,
            "Unselect selected files/folders"
        )
        self.EscKey.activated.connect(self.EscHandler)

    def EscHandler(self):
        '''handle ESC key'''
        if self.webview.searchPanel.isVisible():
            self.webview.searchPanel.closePanel()
        elif self.keypress_search.isVisible():
            self.keypress_search.hide()
        else: 
            self.selected_item = None
            self.clearSelection()

    def toggleHiddenFiles(self):
        if self.hidden_visible:
            self.hidden_visible = False
            self.webview.page().runJavaScript('hideHiddenFiles();')
        else:
            self.hidden_visible = True
            self.webview.page().runJavaScript('showHiddenFiles();')
        
    def searchByFileName(self):
        '''search by top level filenames in the currently opened folder only, and scroll it into view. (this search is case insensitive)'''
        query = self.keypress_search.text().lower()
        selIndex = None
        for i, filename in enumerate(self.listed_filenames):
            filename = filename.lower()
            if filename.startswith(query): selIndex = i
        if selIndex is not None:
            id = self.listed_full_paths[selIndex]
            self.highlightItem(id)
            self.scrollToItem(id)

    def openParent(self):
        path = str(self.folder.parent)
        self.open(path)

    def reOpen(self):
        path = str(self.folder)
        self.open(path)

    def openFileInWebView(self):
        """opens selected file in webview."""
        if self.selected_item:
            self.webview.load(
                QUrl.fromLocalFile(
                    self.selected_item
                )    
            )
        else:
            self.webview.load(
                QUrl.fromLocalFile(
                    str(self.folder)
                )    
            )

    def openFileInTerminal(self):
        """opens selected file in terminal."""
        pass

    def callXdgOpen(self, path: str):
        '''call xdg-open for the appropriate mimetype.'''
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        print(f"{path}: calling xdg-open for {mimetype} files")
        url = QUrl.fromLocalFile(path).toString()
        os.system(f'xdg-open "{url}"')

    def listFiles(self, path: str, **args):
        listed_and_full_paths_files = []
        listed_and_full_paths_folders = []
        # hidden files are marked by a 0
        # sort in reverse order or not
        reverse = args.get("reverse", False)
        for file in os.listdir(path):
            # if hidden == False and file.startswith("."):
            #     continue
            full_path = os.path.join(path, file) 
            if os.path.isdir(full_path):
                listed_and_full_paths_folders.append((
                    file, 1 if file.startswith(".") else 0, 
                    os.path.join(path, file)
                ))
            else:
                listed_and_full_paths_files.append((
                    file, 1 if file.startswith(".") else 0, 
                    os.path.join(path, file)
                ))
        listed_and_full_paths_folders = sorted(
            listed_and_full_paths_folders, 
            key=lambda x: x[0].lower(), 
            reverse=reverse,
        )
        listed_and_full_paths_files = sorted(
            listed_and_full_paths_files, 
            key=lambda x: x[0].lower(), 
            reverse=reverse,
        )
        listed_and_full_paths = listed_and_full_paths_folders + listed_and_full_paths_files
        listed = [i for i,_,_ in listed_and_full_paths]
        full_paths = [i for _,_,i in listed_and_full_paths]
        hidden_flag_list = [i for _,i,_ in listed_and_full_paths]

        return listed, full_paths, hidden_flag_list

    def getIcon(self, path):
        name = self.icon_provider.icon(QFileInfo(path)).name()
        # print(name)
        # paths where mimetype icons may be found.
        icon_theme_devices_path = "/usr/share/icons/breeze/devices/48"
        icon_theme_places_path = "/usr/share/icons/breeze/places/64"
        icon_theme_mimes_path = "/usr/share/icons/breeze/mimetypes/32"
        Path = os.path.join(icon_theme_devices_path, name+".svg")
        if os.path.exists(Path): return Path
        Path = os.path.join(icon_theme_places_path, name+".svg")
        if os.path.exists(Path): return Path
        Path = os.path.join(icon_theme_mimes_path, name+".svg")
        if os.path.exists(Path): return Path

        return path

    def errorDialog(self, msg):
        self.error_dialog = QErrorMessage()
        self.error_dialog.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.error_dialog.showMessage(msg)
        # print(msg)
    def createDialogue(self, item_type="file"):
        if item_type == "folder": 
            path = self.createFolder()
            icon = "file:///usr/share/icons/breeze/places/64/inode-directory.svg"
            # file icon: file:///usr/share/icons/Humanity/mimes/48/text-plain.svg
        elif item_type == "file": 
            path = self.createFile()
            icon = "file:///usr/share/icons/breeze/mimetypes/32/text-plain.svg"
            # folder icon: file:///usr/share/icons/Humanity/places/64/inode-directory.svg
        name = Path(path).name
        self.webview.createItem(path, name, icon, hidden=False) 

    def renameDialog(self, path: Union[str, None]=None):
        '''rename file item, by creating an editable field.'''
        if path is None: path = self.selected_item
        if self.selected_item:
            self.webview.initiateRenameForId(self.selected_item)

    def renameItem(self, id: str, new_name: str):
        parent = Path(id).parent
        new_name = os.path.join(parent, new_name)
        print(f"renaming {id} to {new_name}")
        os.rename(id, new_name)

    def createFile(self):
        '''create a new empty file'''
        i = 1
        while True:
            path = os.path.join(self.folder, f"Untitled File {i}")
            if not os.path.exists(path): break
            else: i += 1
        print(f"\x1b[32;1mcreated new file: {path}\x1b[0m")
        open(path, "w")

        return path

    def createFolder(self):
        '''create a new empty folder'''
        i = 1
        while True:
            try:
                path = os.  path.join(
                    self.folder, 
                    f"Untitled Folder {i}"
                )
                os.mkdir(path)
                break
            except FileExistsError:
                i += 1
        print(f"\x1b[32;1mcreated new folder: {path}\x1b[0m")

        return path

    def viewSource(self):
        """view source of the current view."""
        try: 
            self.webview.page().triggerAction(
                QWebEnginePage.ViewSource
            )
        except Exception as e: 
            print("\x1b[33;1mui::system::fileviewer::FileViewerWidget.viewSource\x1b[0m", e)

    def createThumbnailWorker(self, path: str, thumb_size: int) -> QThread:
        s = time.time()
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        if mimetype not in ["application/pdf"]: return
        # create thumbnailing thread.
        thumbnail_thread = QThread()
        thumbnail_worker = FileViewerThumbnailer()
        thumbnail_worker.queueFile(path, mimetype, thumb_size)
        # add worker and thread to thread pool and worker list.
        self.thumbnail_workers.append(thumbnail_worker)
        self.thumbnail_thread_pool.append(thumbnail_thread)
        # create weather API fetching worker.
        thumbnail_worker.moveToThread(thumbnail_thread)
        # connect to slots
        thumbnail_thread.started.connect(thumbnail_worker.generateThumbnail)
        thumbnail_thread.finished.connect(thumbnail_thread.deleteLater)

        # thumbnail_worker.progress.connect(self.setThumbnail)
        thumbnail_worker.finished.connect(thumbnail_thread.quit)
        thumbnail_worker.finished.connect(thumbnail_worker.deleteLater)
        # start updation thread.
        thumbnail_thread.start()
        # print(f"thumbnail requested for {path} in {time.time()-s}s")
    # def setThumbnail(self, path: str, thumb_path: str):
    #     if thumb_path == "None":
    #         print(f"\x1b[31;1mthumbnail can't be generated for {path}\x1b[0m")
    #         return
    #     self.webview.page().runJavaScript(f"""
    #     document.getElementById("thumbnail_{path}").src = {QUrl.fromLocalFile(thumb_path).toString()};
    #     """)
    #     # print(f"thumbnail for {path} @ {thumb_path}")
    def open(self, folder: str="~"):
        from fig_dash.ui.js.fileviewer import FileViewerHtml, FileViewerStyle, FileViewerCustomJS, FileViewerMJS, ViSelectJS
        '''open a file/folder location.'''
        try:
            print(self.dash_window)
            i = self.dash_window.tabs.currentIndex()
            self.dash_window.tabs.setTabText(i, folder)
        except AttributeError:
            print("FileViewerWidget: \x1b[31;1mnot connected to a DashWindow\x1b[0m")
        # expand user.
        folder = os.path.expanduser(folder) 
        self.file_watcher.addPath(folder)
        # call xdg-open if a file is clicked instead of a folder.
        if os.path.isfile(folder): 
            self.callXdgOpen(folder)
            return
        # might be a device or something.
        if not os.path.isdir(folder): return
        # check if the user has permission to view folder
        try:
            os.scandir(folder)
        except PermissionError as e:
            print("\x1b[31;1mfileviewer.open\x1b[0m", e)
            self.errorDialog(str(e))
            return
        self.folder = Path(folder)
        self.folderbar.setPath(folder)  
        self.browsing_history.append(folder)
        listed, full_paths, hidden_flag_list = self.listFiles(folder)
        # populate content for searching.
        self.listed_filenames = listed
        self.listed_full_paths = full_paths
        self.listed_hidden_files = hidden_flag_list
        file_count = 0
        folder_count = 0 
        hidden_count = 0
        for path in full_paths:
            if os.path.isdir(path):
                folder_count += 1
            elif os.path.isfile(path):
                file_count += 1
        for value in hidden_flag_list:
            if value == False: continue
            hidden_count += 1
        # get number of items, folder, files and hidden
        self.statusbar.updateBreakdown(
            files=file_count,
            items=len(self.listed_filenames),
            hidden=hidden_count,
            folders=folder_count,
        )

        for path in full_paths:
            self.loaded_file_items.append({
                "path": path, 
                "mimetype": self.mime_database.mimeTypeForFile(path).name(),
                "info": QFileInfo(path),
            }) 
        humanity_to_breeze_map = {
            "video": "video-mp4",
        }  
        icons = []
        for path in full_paths:
            iconPath = humanity_to_breeze_map.get(
                self.icon_provider.icon(
                    QFileInfo(path)
                ).name(),
                self.icon_provider.icon(
                    QFileInfo(path)
                ).name()
            ) 
            icons.append((
                iconPath,
                self.mime_database.mimeTypeForFile(path).name(),
                path
            ))
        # icons = [
        #     (iconPath, 
        #      self.mime_database.mimeTypeForFile(path).name(),
        #      path) for path in full_paths
        # ]
        icon_theme_devices_path = "/usr/share/icons/breeze/devices/48"
        icon_theme_places_path = "/usr/share/icons/breeze/places/64"
        icon_theme_mimes_path = "/usr/share/icons/breeze/mimetypes/32"
        # if os.path.exists(icon_theme_places_path):
        icon_paths = []
        for name, mimetype, full_path in icons:
            if name == "":
                name = "text-plain"
            elif mimetype.startswith("image/"):
                path = full_path
                icon_paths.append(QUrl.fromLocalFile(path).toString())
            elif mimetype in ["application/pdf"]:
                # check if file is already cached.
                filename = full_path.replace("/", "|")
                cached_file_path = os.path.join(
                    FILE_VIEWER_CACHE_PATH, 
                    filename + ".png",
                )
                # print(cached_file_path)
                if os.path.exists(cached_file_path):
                    icon_paths.append(QUrl.fromLocalFile(cached_file_path).toString())
                else: 
                    path = os.path.join(
                        icon_theme_mimes_path, 
                        name+".svg"
                    )
                    if os.path.exists(path): 
                        icon_paths.append(QUrl.fromLocalFile(path).toString())
                        continue
                    path = os.path.join(
                        icon_theme_places_path, 
                        name+".svg"
                    )
                    if os.path.exists(path): 
                        icon_paths.append(QUrl.fromLocalFile(path).toString())
                        continue
                    path = os.path.join(
                        icon_theme_devices_path, 
                        name+".svg"
                    )    
                    if os.path.exists(path): 
                        icon_paths.append(QUrl.fromLocalFile(path).toString())
                        continue
                    path = "/usr/share/icons/breeze/mimetypes/32/text-plain.svg"
                    icon_paths.append(QUrl.fromLocalFile(path).toString())                    
            else:
                path = os.path.join(
                    icon_theme_mimes_path, 
                    name+".svg"
                )
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = os.path.join(
                    icon_theme_places_path, 
                    name+".svg"
                )
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = os.path.join(
                    icon_theme_devices_path, 
                    name+".svg"
                )    
                if os.path.exists(path): 
                    icon_paths.append(QUrl.fromLocalFile(path).toString())
                    continue
                path = "/usr/share/icons/breeze/mimetypes/32/text-plain.svg"
                icon_paths.append(QUrl.fromLocalFile(path).toString())    
        print(self.webview.url()) 
        # def chunk_string(string, k=12):
        #     result = []
        #     for i in range(0, len(string), k):
        #         result.append(string[i:i+k])

        #     return result
        def format_listed(prelisted):
            listed = []
            for rec in prelisted:
                # rec = "_<br>".join(rec.split("_"))
                # rec = "<br>".join(chunk_string(rec))
                listed.append(rec)

            return listed         
        # print(icons)
        self.params = {
            "FOLDER": self.folder.name,
            "FONT_COLOR": self.font_color,
            "WEBCHANNEL_JS": QWebChannelJS,
            "FILEVIEWER_JS": ViSelectJS,
            "FILEVIEWER_MJS": FileViewerMJS,
            "FILEVIEWER_CSS": FileViewerStyle,
            "FILEVIEWER_CJS": FileViewerCustomJS,
            "PARENT_FOLDER": self.folder.parent.name,
            "FILEVIEWER_ICONS": icon_paths,
            "FILEVIEWER_PATHS": full_paths,
            "FILEVIEWER_ITEMS": format_listed(listed),
            "BACKGROUND_IMAGE": self.background_image,
            "HIDDEN_FLAG_LIST": hidden_flag_list,
            "NUM_ITEMS": len(listed),
        }
        self.params.update(self.systemHandler.js_sources)
        self.viewer_html = jinja2.Template(
            FileViewerHtml.render(**self.params)
        ).render(**self.params)
        render_url = FigD.createTempUrl(self.viewer_html)
        self.webview.load(render_url)
        s = time.time()
        for path in full_paths: 
            self.createThumbnailWorker(path=path, thumb_size=240)
        print(f"\x1b[33;1m**created thumbnail workers in {time.time()-s}s**\x1b[0m")

    def updateSelection(self, item):
        '''update widget state when currently selected item is changed'''
        self.selected_item = item
        # print(os.path.splitext(item))
        _, file_ext = os.path.splitext(item)
        if file_ext == "":
            file_ext = ".ext"
        # print(file_ext)
        icon = self.getIcon(item)
        mimetype = self.mime_database.mimeTypeForFile(item).name()
        self.menu.filegroup.updateExt(file_ext)
        self.menu.opengroup.updateMimeBtn(
            mimetype=mimetype, 
            icon=icon, path=item
        )
        file_info = QFileInfo(item)
        name = file_info.fileName()
        if file_info.isDir():
            items = len(os.listdir(item)) 
        else: items = 0
        size = h_format_mem(file_info.size())
        # .strftime("%b, %m %d %Y %H:%M:%S")
        group = file_info.group()
        owner = file_info.owner()
        shortcut = file_info.isShortcut()
        symbolic = file_info.isSymbolicLink()
        r_permission = file_info.isReadable()
        w_permission = file_info.isWritable()
        x_permission = file_info.isExecutable()
        permissions = "["
        if r_permission:
            permissions += "R"
        if w_permission:
            permissions += "W"
        if x_permission:
            permissions += "X"
        permissions += "]"

        last_read = file_info.lastRead().toPyDateTime()
        last_modified = file_info.lastModified().toPyDateTime()
        meta_change_time = file_info.metadataChangeTime().toPyDateTime()
        # print(last_read, last_modified, group, owner, 
        #       meta_change_time, permissions)
        self.statusbar.updateSelected(
            shortcut=shortcut, symbolic=symbolic,
            items=items, name=name, icon=icon, 
            size=size, permissions=permissions,
            meta_change_time=meta_change_time,
            last_read=last_read, owner=owner,
            last_modified=last_modified,
            group=group,
        )

    def keyPressEvent(self, event):
        # print(event.key()) # print("opened keypress search")
        try:
            letter = chr(event.key())
            self.keypress_search.showPanel(
                parent=self, 
                w=self.width(),
                h=self.height(),
            )
            self.keypress_search.setText(letter.lower())
            # print("changed focus")
        except (TypeError, ValueError) as e:
            print("\x1b[31;1mfileviewer.keyPressEvent\x1b[0m", e)
            # fail silently.
        super(FileViewerWidget, self).keyPressEvent(event)

    def onUrlChange(self):
        self.selected_item = None
        self.webview.setZoomFactor(self.zoom_factor)
        self.webview.loadFinished.connect(self.webview.loadDevTools)

    def copyUrlToClipboard(self):
        if self.clipboard and self.selected_item:
            url = QUrl.fromLocalFile(self.selected_item).toString()
            self.clipboard.setText(url)
            print(f"copied {url} to clipboard")  

    def copyStemToClipboard(self):
        if self.clipboard and self.selected_item:
            stem = Path(self.selected_item).stem
            self.clipboard.setText(stem)
            print(f"copied {stem} to clipboard")    

    def copyPathToClipboard(self):
        if self.clipboard and self.selected_item:
            self.clipboard.setText(self.selected_item)
            print(f"copied {self.selected_item} to clipboard")

    def copyNameToClipboard(self):
        if self.clipboard and self.selected_item:
            name = Path(self.selected_item).name
            self.clipboard.setText(name)
            print(f"copied {name} to clipboard")            

    @pyqtSlot()
    def selectAll(self):
        '''select all items.'''
        # print("selected all items")
        self.webview.page().runJavaScript('selectAllItems();')

    def reload(self):
        '''refresh the webview'''
        self.webview.reload()

    def scrollToItem(self, id: str):
        '''scroll item into view by id.'''
        code = f"document.getElementById('{id}').scrollIntoView()"
        self.webview.page().runJavaScript(code)

    def invertSelection(self):
        '''invert selected items.'''
        self.webview.page().runJavaScript('invertSelectedItems();')

    def highlightItem(self, id: str):
        '''select a specific item by id'''
        self.clearSelection()
        self.webview.page().runJavaScript(f"selectItemById('{id}')")

    def clearSelection(self):
        '''clear selected items.'''
        self.webview.page().runJavaScript('clearSelectedItems();')

    def copyToClipboard(self, text):
        if self.clipboard:
            self.clipboard.setText(text)
            print(f"copied {text} to clipboard")

    def saveScreenshot(self, path):
        with open(path, "w") as f:
            f.write(self.viewer_html)

    def connectWindow(self, window):
        print("FileViewerWidget: \x1b[32;1mconnected to DashWindow\x1b[0m")
        self.dash_window = window

    def wrapInScrollArea(self, widget):
        scrollArea = QScrollArea()
        scrollArea.setWidget(widget)
        scrollArea.setAttribute(Qt.WA_TranslucentBackground)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setStyleSheet("""
        QScrollArea {
            border: 0px;
            background: transparent;
        }""")

        return scrollArea


def test_fileviewer():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    # fileviewer = FileViewerWidget(
    #     clipboard=app.clipboard(),
    #     background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
    #     logo="system/fileviewer/logo.svg",
    #     font_color="#fff", parentless=True,
    # )
    # fileviewer.setStyleSheet("background: tranparent; border: 0px;")
    # QFontDatabase.addApplicationFont(
    #     FigD.font("BeVietnamPro-Regular.ttf")
    # )
    # fileviewer.setGeometry(200, 200, 800, 600)
    # fileviewer.setWindowFlags(Qt.WindowStaysOnTopHint)
    # fileviewer.statusBar().addWidget(
    #     fileviewer.statusbar
    # )
    # app.setWindowIcon(FigD.Icon("system/fileviewer/logo.svg"))
    # try: 
    #     path = os.path.expanduser(sys.argv[1])
    # except IndexError: 
    #     path = os.path.expanduser("~")
    # fileviewer.open(path)
    # fileviewer.show()
    # app.exec()
    # get accent color & icon.
    icon = FigDSystemAppIconMap["fileviewer"]
    accent_color = FigDAccentColorMap["fileviewer"]
    fileviewer = FileViewerWidget(
        clipboard=QApplication.instance().clipboard(),
        background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        font_color="#fff", parentless=True, dangle_folderbar=True,
        accent_color=accent_color,
    )
    # open path.
    try: 
        path = os.path.expanduser(sys.argv[1])
    except IndexError: 
        path = os.path.expanduser("~")
    fileviewer.open(path)
    window = wrapFigDWindow(fileviewer, icon=icon, width=800,
                            height=600, accent_color=accent_color,
                            name="fileviewer", titlebar_callbacks={
                                "viewSourceBtn": fileviewer.viewSource,
                            }, title_widget=fileviewer.folderbar)
                            #, title=f"fileviewer: {path}")
    spacer1 = QWidget()
    spacer1.setStyleSheet("background: transparent")
    spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    spacer2 = QWidget()
    spacer2.setStyleSheet("background: transparent")
    spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    window.statusBar().addWidget(spacer1)
    window.statusBar().addWidget(fileviewer.statusbar)
    window.statusBar().addWidget(spacer2)
    window.statusBar().setStyleSheet("""
    QStatusBar {
        color: #4293d5;
        border-radius: 20px;
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    }""")
    window.show()
    app.exec()
    # fileviewer.saveScreenshot("fileviewer.html")
def launch_fileviewer(app, path: Union[str, None]=None):
    # get accent color & icon.
    icon = FigDSystemAppIconMap["fileviewer"]
    accent_color = FigDAccentColorMap["fileviewer"]
    fileviewer = FileViewerWidget(
        clipboard=QApplication.instance().clipboard(),
        background="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        font_color="#fff", parentless=True, accent_color=accent_color
    )
    # open path.
    if path is not None: 
        fileviewer.open(path)
    else: fileviewer.open("~")

    window = wrapFigDWindow(fileviewer, accent_color=accent_color, 
                            icon=icon, width=800, height=600, 
                            name="fileviewer")
    spacer1 = QWidget()
    spacer1.setStyleSheet("background: transparent")
    spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    spacer2 = QWidget()
    spacer2.setStyleSheet("background: transparent")
    spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    window.statusBar().addWidget(spacer1)
    window.statusBar().addWidget(fileviewer.statusbar)
    window.statusBar().addWidget(spacer2)
    window.statusBar().setStyleSheet("""
    QStatusBar {
        color: #4293d5;
        border-radius: 20px;
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
    }""")
    window.show()


if __name__ == '__main__':
    test_fileviewer()
#a33817 (dark) #323150
#eb5f34 (deep) #4d4c78
#bd5f42 (medium) #64639c
#db8b72 (dull) #8a87b2
#e0a494 (light) #c8c2e9
#f2e3df (very light) #dfdafd
# https://towardsdatascience.com/a-friendly-introduction-to-siamese-networks-85ab17522942#:~:text=A%20Siamese%20Neural%20Network%20is%20a%20class%20of%20neural%20network%20architectures%20that%20contain
# https://towardsdatascience.com/case-study-2-an-unsupervised-neural-attention-model-for-aspect-extraction-1c2c97b1380a#:~:text=All%20reviews-,are,-available%20as%20a


# class DashClipboardUI(QMainWindow):
#     def __init__(self):
#         super(DashClipboardUI, self).__init__()
#         QApplication.clipboard().dataChanged.connect(
#             self.onDataChanged
#         )
#         self.clipboard_ui = self.initCentralWidget()
#         self.setCentralWidget(self.clipboard_ui)
#         self.history = []

#     def wrapInScrollArea(self, widget):
#         scrollArea = QScrollArea()
#         scrollArea.setWidget(widget)
#         scrollArea.setAttribute(Qt.WA_TranslucentBackground)
#         scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         # scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         scrollArea.setStyleSheet("""
#         QScrollArea {
#             background-position: center;
#             background: transparent;
#             border: 0px;
#         }
#         QScrollBar:vertical {
#             border: 0px solid #999999;
#             width: 15px;    
#             margin: 0px 0px 0px 0px;
#             background-color: rgba(255, 255, 255, 0);
#         }
#         QScrollBar::handle:vertical {         
#             min-height: 0px;
#             border: 0px solid red;
#             border-radius: 0px;
#             background-color: transparent;
#         }
#         QScrollBar::handle:vertical:hover {         
#             background-color: rgba(255, 255, 255, 0.5);
#         }
#         QScrollBar::add-line:vertical {       
#             height: 0px;
#             subcontrol-position: bottom;
#             subcontrol-origin: margin;
#         }
#         QScrollBar::sub-line:vertical {
#             height: 0 px;
#             subcontrol-position: top;
#             subcontrol-origin: margin;
#         }""")

#         return scrollArea

#     def initStack(self):
#         stack = QWidget()
#         stack.setStyleSheet("""
#         QWidget {
#             border: 0px;
#             background: transparent;
#         }""")
#         layout = QVBoxLayout()
#         layout.setContentsMargins(10, 10, 10, 10)
#         layout.setSpacing(10)
#         stack.setLayout(layout)
#         stack.setStyleSheet("""
#         QWidget {
#             border: 0px;
#             background: transparent;
#         }""")

#         return self.wrapInScrollArea(stack)

#     def initSearchBar(self):
#         searcharea = QWidget()
#         layout = QVBoxLayout()
#         layout.setContentsMargins(10, 10, 10, 10)
#         searcharea.setLayout(layout)

#         searchbar = QLineEdit()
#         searchbar.setPlaceholderText("Search Clipboard!")
#         searchbar.setStyleSheet(
#         """QLineEdit {
#             color: #fff;
#             background: #292929;
#         }""")
#         layout.addWidget(searchbar)

#         return searcharea

#     def initCentralWidget(self):
#         centralWidget = QWidget()
#         # layout.
#         self.layout = QVBoxLayout()
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         self.layout.setSpacing(0)
#         # search bar.
#         self.searchbar = self.initSearchBar()
#         self.layout.addWidget(self.searchbar)
#         # central display stack.
#         self.stack = self.initStack()
#         self.stackLayout = self.stack.widget().layout()
#         print(self.stackLayout)
#         self.layout.addWidget(self.stack)
#         self.layout.addStretch(1)

#         centralWidget.setLayout(self.layout)
#         centralWidget.setObjectName("ClipboardViewerWidget")
#         centralWidget.setStyleSheet("""
#         QWidget#ClipboardViewerWidget {
#             border-radius: 20px;
#             background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 rgba(17, 17, 17, 0.9), stop : 0.143 rgba(22, 22, 22, 0.9), stop : 0.286 rgba(27, 27, 27, 0.9), stop : 0.429 rgba(32, 32, 32, 0.9), stop : 0.571 rgba(37, 37, 37, 0.9), stop : 0.714 rgba(41, 41, 41, 0.9), stop : 0.857 rgba(46, 46, 46, 0.9), stop : 1.0 rgba(51, 51, 51, 0.9));
#         }""")

#         return centralWidget

#     def onDataChanged(self):
#         # print(i)
#         text = QApplication.clipboard().text()
#         self.append(text)

#     def connectTitlebar(self, titlebar: WindowTitleBar):
#         self.titlebar = titlebar
#         self.titlebar.connectWindow(self)

#     def initClipboardItem(self, text: str):
#         item = QTextEdit()
#         item.setText(text)
#         item.setStyleSheet("""
#         QTextEdit {
#             color: #fff;
#             border: 0px;
#             border-radius: 5px;
#             background: #484848;
#         }""")

#         return item

#     def append(self, text: str):
#         print(f"\x1b[31;1mui.system.clipboard::DashClipboardUI::append\x1b[0m({text})")
#         self.history.append(text)
#         clipboard_item = self.initClipboardItem(text)
#         self.stackLayout.insertWidget(0, clipboard_item)

# def test_clipboard_ui():
#     import sys
#     FigD("/home/atharva/GUI/fig-dash/resources")
#     app = QApplication(sys.argv)
#     app.setStyleSheet("""
#     QToolTip {
#         color: #fff;
#         border: 0px;
#         padding-top: -1px;
#         padding-left: 5px;
#         padding-right: 5px;
#         padding-bottom: -1px;
#         font-size:  17px;
#         background: #000;
#         font-family: 'Be Vietnam Pro', sans-serif;
#     }""")
#     screen_rect = app.desktop().screenGeometry()
#     w, h = screen_rect.width()//2, screen_rect.height()//2
#     # create and reposition clipboard UI.
#     clipboard_ui = DashClipboardUI()
#     # add the custom window titlebar.
#     titlebar = WindowTitleBar(background="qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #390b56, stop : 0.091 #420d64, stop : 0.182 #4c0f72, stop : 0.273 #561181, stop : 0.364 #601390, stop : 0.455 #6a169f, stop : 0.545 #7418ae, stop : 0.636 #7f1abe, stop : 0.727 #891cce, stop : 0.818 #941ede, stop : 0.909 #9f20ee, stop : 1.0 #aa22ff);")
#     # titlebar.setStyleSheet("background: #292929; color: #fff;")
#     clipboard_ui.layout.insertWidget(0, titlebar)
#     clipboard_ui.connectTitlebar(titlebar)
#     # set window icon, title and flags.
#     clipboard_ui.setWindowIcon(FigD.Icon("system/clipboard/window_icon.png"))
#     clipboard_ui.setWindowTitle("Clipboard Viewer")
#     clipboard_ui.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#     clipboard_ui.setAttribute(Qt.WA_TranslucentBackground)
#     titlebar.setWindowIcon(
#         clipboard_ui.windowIcon(), 
#         size=(25,25)
#     )
#     # reposition window and show UI.
#     clipboard_ui.move(w, h)
#     clipboard_ui.show()
    
#     app.exec()