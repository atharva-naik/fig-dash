#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::desktop")
import os
import time
from turtle import back
import jinja2
import shutil
import datetime
from typing import *
from pysondb import db
from pathlib import Path
from functools import partial
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import styleContextMenu
from fig_dash.ui.webview import DebugWebView
from fig_dash.ui.system.filexplorer import FILE_VIEWER_TRASH_PATH, FILE_VIEWER_CACHE_PATH, blank, FileViewerThumbnailer, FileViewerEventHandler, FileViewerKeyPressSearch, FileViewerBrowser
# PyQt5 imports 
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtGui import QIcon, QImage, QPixmap, QColor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QPoint, QObject, QTimer, QFile, QFileInfo, QUrl, QMimeDatabase, pyqtSlot, pyqtSignal, QThread, QFileSystemWatcher
from PyQt5.QtWidgets import QMenu, QWidget, QWidgetAction, QMainWindow, QShortcut, QApplication, QStackedWidget, QFileIconProvider

# default desktop background URL.
DEFAULT_DESKTOP_BACKGROUND = "https://uhdwallpapers.org/uploads/converted/20/06/25/macos-big-sur-wwdc-2560x1440_785884-mm-90.jpg"
class DesktopBackground(QObject):
    def __init__(self, path):
        super(DesktopBackground, self).__init__()
        import pysondb
        self.db_ptr = pysondb.db.getDb(
            FigD.static("")
        )

class DesktopEventHandler(QObject):
    showClipboard = pyqtSignal(int, int) 
    def __init__(self):
        super(DesktopEventHandler, self).__init__()

    @pyqtSlot(float, float, float, float)
    def triggerClipboard(self, top: float, right: float, 
                         bottom: float, left: float):
        # print(f"DesktopEventHandler.triggerClipboard({top}, {right}, {bottom}, {left})")
        x = int((left+right)//2)
        y = int((top+bottom)//2)
        # print(f"DesktopEventHandler.triggerClipboard: eventPos({x}, {y})")
        self.showClipboard.emit(x, y)

# desktop view - browser section.
class DesktopBrowserSection(FileViewerBrowser):
    def __init__(self, accent_color: str):
        super(DesktopBrowserSection, self).__init__(accent_color)

    def initOrchardMenu(self):
        self.orchardMenu = QMenu()
        if hasattr(self, "widget"):
            self.viewMenu = self.orchardMenu.addMenu("View")
            self.sortMenu = self.orchardMenu.addMenu("Sort by")
            self.orchardMenu.addAction(
                FigD.Icon("textedit/reload.svg"),
                "Refresh", self.reload, 
                QKeySequence.Refresh,
            )
            self.orchardMenu.addSeparator()
            self.orchardMenu.addAction(
                FigD.Icon("system/fileviewer/new_tab_icon.svg"), 
                "New Folder", partial(self.widget.createDialogue, "folder")
            )
            self.newFileMenu = self.orchardMenu.addMenu("New File")
            self.newFileMenu = styleContextMenu(self.newFileMenu)
            self.newFileMenu.addAction(
                FigD.Icon("system/fileviewer/file.svg"), "Empty Text File",
                partial(self.widget.createDialogue, "file")
            )
            self.orchardMenu.addSeparator()
        self.orchardMenu.addAction("Restore Missing Files...      ")
        self.orchardMenu.addAction(
            FigD.Icon("system/fileviewer/terminal.svg"), 
            "Open in Terminal", blank, QKeySequence("Ctrl+Alt+T")
        )
        self.orchardMenu.addSeparator()
        self.pasteItem = self.orchardMenu.addAction(
            FigD.Icon("textedit/paste.svg"), 
            "Paste", blank, QKeySequence.Paste,
        )
        self.pasteShortcutToItem = self.orchardMenu.addAction(
            FigD.Icon("system/fileviewer/paste_shortcut.ico"), 
            "Paste shortcut"
        )
        self.pasteItem.setEnabled(False)
        self.pasteShortcutToItem.setEnabled(False)
        self.undoDelete = self.orchardMenu.addAction(
            "Undo Delete", blank, QKeySequence.Undo,
        )
        self.toolsMenu = self.orchardMenu.addMenu("Tools")
        # system tools menu.
        self.sysToolsMenu = self.orchardMenu.addMenu("System Tools")
        self.sysToolsMenu.addAction("Computer Management")
        self.sysToolsMenu.addAction("Task Manager")
        self.sysToolsMenu.addAction("Command Prompt")
        # `GTK Open` for Linux/`Run` for Windows.
        self.sysToolsMenu.addAction("GTK Open")
        self.sysToolsMenu.addAction("All Tasks")
        self.sysToolsMenu.addAction("Device Manager")
        self.sysToolsMenu.addAction("Network Connections")
        self.sysToolsMenu.addAction("Settings")
        self.sysToolsMenu.addAction("Empty Recycle Bin")
        self.sysToolsMenu = styleContextMenu(self.sysToolsMenu)

        self.undoDelete.setEnabled(False)
        self.orchardMenu.addAction("Organize Desktop by Name")
        self.orchardMenu.addSeparator()
        # self.orchardMenu.addAction(FigD.Icon("system/fileviewer/properties.svg"), "Properties")
        self.orchardMenu.addSeparator()
        self.orchardMenu.addAction(
            FigD.Icon("system/fileviewer/background-image.png"),
            "Change Desktop Background"
        )
        self.orchardMenu.addAction(
            FigD.Icon("desktop/slideshow.ico"),
            "Activate Wallpaper Carousel"
        )
        self.orchardMenu.addAction(
            FigD.Icon("desktop/personalize.ico"), 
            "Personalize",
        )
        self.orchardMenu = styleContextMenu(self.orchardMenu)

        return self.orchardMenu

# desktop clock worker.
class DesktopClockWorker(QObject):
    dateChanged = pyqtSignal(str)
    timeChanged = pyqtSignal(str)
    timeOfDayChanged = pyqtSignal(str)
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DesktopClockWorker, self).__init__(parent)
        self.tod_ctr = 0
        # the clock backend.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)
        # state variables.
        self.date = ""
        self.timeOfDay = ""
        
    def update(self):
        now = datetime.datetime.now()
        timeNow = now.strftime("%-I:%M:%S %p")
        # millis = int(now.strftime("%f")) % 1000
        if self.tod_ctr % 10 == 0:
            hr = int(now.strftime("%H"))
            self.emitTimeOfDay(hr)
            self.setDay(now)
        self.tod_ctr += 1
        self.timeChanged.emit(timeNow)

    def setDay(self, now: datetime.datetime):
        dateNow = now.strftime("%a %b %d %Y")
        if self.date != dateNow:
            self.dateChanged.emit(dateNow)
            # print(f"self.dateChanged.emit({dateNow})")
    def emitTimeOfDay(self, hr: int):
        timeOfDay = self.getTimeOfDay(hr)
        if timeOfDay != self.timeOfDay:
            tod_icon = FigD.icon(f"system/datetime/{timeOfDay}.png")
            print(f"self.timeOfDayChanged.emit({tod_icon})")
            self.timeOfDayChanged.emit(tod_icon)
            self.timeOfDay = timeOfDay

    def getTimeOfDay(self, hr: int):
        if 6<=hr<=11: timeOfDay="morning"
        elif 11<=hr<=16: timeOfDay="afternoon"
        elif 16<=hr<=19: timeOfDay="evening"
        else: timeOfDay="night"

        return timeOfDay

# desktop view
class DebugDesktopView(DebugWebView):
    zoomChanged = pyqtSignal(float)
    selectionChanged = pyqtSignal(list)
    def __init__(self, *args, accent_color: str="rgb(255,255,255)", 
                 background=DEFAULT_DESKTOP_BACKGROUND, **kwargs):
        browser = DesktopBrowserSection(accent_color=accent_color)
        super(DebugDesktopView, self).__init__(
            *args, browser=browser, 
            **kwargs,
        )
        self.clipboardManager = None
        browser.widget = self
        # desktop clock.
        self._desktop_clock_backend = DesktopClockWorker()
        self._desktop_clock_backend.dateChanged.connect(self.updateDate)
        self._desktop_clock_backend.timeChanged.connect(self.updateTime)
        self._desktop_clock_backend.timeOfDayChanged.connect(self.updateTimeOfDay)
        # import system handler and extract accent color for scrollbar.
        from fig_dash.api.js.system import SystemHandler
        from fig_dash.ui import create_css_grad, extract_colors_from_qt_grad
        self.thumbnail_thread_pool = []
        self.thumbnail_workers = []
        self.css_grad = create_css_grad(
            extract_colors_from_qt_grad(accent_color)
        )
        self.browser.zoomChanged.connect(self.signalZoom)
        if os.path.exists(os.path.expanduser(background)):
            self.background_image = QUrl.fromLocalFile(background).toString()
            # print(f"background_image: url({self.background_image})")
        else: self.background_image = QUrl(background).toString()
        # file watcher, icon_provider and mime_database for getting icons for desktop.
        self.file_watcher = QFileSystemWatcher()
        self.icon_provider = QFileIconProvider()
        self.mime_database = QMimeDatabase()
        self.loaded_file_items = []
        self.selected_item = None
        self.hidden_visible = False
        self.file_watcher.directoryChanged.connect(self.reOpen)
        # handle click events (using click handler)
        self.channel = QWebChannel()
        self.eventHandler = FileViewerEventHandler(self)
        self.desktopHandler = DesktopEventHandler()
        # connect slots to signals.
        self.desktopHandler.showClipboard.connect(self.showClipboard)
        self.channel.registerObject("eventHandler", self.eventHandler)
        self.channel.registerObject("desktopHandler", self.desktopHandler)
        self.systemHandler = SystemHandler()
        self.systemHandler.connectChannel(self.channel)
        self.browser.page().setWebChannel(self.channel)
        # shortcuts common among fileviewer and desktop.
        from fig_dash.ui import FigDShortcut
        self.MoveSelUp = FigDShortcut(
            QKeySequence.MoveToPreviousLine, 
            self, "Select item above",
        )
        self.MoveSelUp.connect(self.moveSelectionUp)
        self.MoveSelDown = FigDShortcut(
            QKeySequence.MoveToNextLine, 
            self, "Select item below"
        )
        self.MoveSelDown.connect(self.moveSelectionDown)
        self.MoveSelLeft = FigDShortcut(
            QKeySequence.MoveToPreviousChar, 
            self, "Select item on left"
        )
        self.MoveSelLeft.connect(self.moveSelectionLeft)
        self.MoveSelRight = FigDShortcut(
            QKeySequence.MoveToNextChar, 
            self, "Select item on right"
        )
        self.MoveSelRight.connect(self.moveSelectionRight)
        self.OpenItem = FigDShortcut(
            QKeySequence.InsertParagraphSeparator, 
            self, "Enter selected folder/file",
        )
        self.OpenItem.connect(self.openSelected)
        self.SelectAll = FigDShortcut(
            QKeySequence.SelectAll, self, 
            "Select all files/folders"
        )
        self.SelectAll.connect(self.selectAll)
        self.Delete = FigDShortcut(
            QKeySequence.Delete, self,
            "Move selected item to Trash"
        )
        self.Delete.connect(self.delSelItem)
        self.CtrlH = FigDShortcut(
            QKeySequence("Ctrl+H"), self,
            "Toggle hidden files/folders"
        )
        self.CtrlH.connect(self.toggleHiddenFiles)
        # key press search bar.
        self.keypress_search = FileViewerKeyPressSearch()
        self.keypress_search.connectWidget(self)
        self.keypress_search.hide()
        self.browser.urlChanged.connect(self.onUrlChange)
        # connect Esc key shortcut to Esc handler.
        self.browser.Esc.setEnabled(False)
        self.EscKey = FigDShortcut(
            QKeySequence("Esc"), self,
            "Unselect selected files/folders"
        )
        self.EscKey.connect(self.EscHandler)
        self.open("~/Desktop")

    def showClipboard(self, x: int, y: int):
        if self.clipboardManager is None:
            from fig_dash.theme import FigDAccentColorMap
            from fig_dash.ui.system.clipboard import DashClipboardUI
            accent_color = FigDAccentColorMap["clipboard"]
            # self.clipboardManager = DashClipboardUI(accent_color=accent_color)
            self.clipboardManager = QMenu()
            self.clipboardManager = styleContextMenu(
                self.clipboardManager,
                accent_color, margin=2,
            )
            clipboard = DashClipboardUI(accent_color=accent_color)
            clipboard.setMinimumHeight(400)
            widgetAction = QWidgetAction(self.clipboardManager)
            widgetAction.setDefaultWidget(clipboard)
            self.clipboardManager.addAction(widgetAction)
            # self.clipboardManager.setWindowFlags(Qt.Popup)
            # self.clipboardManager.setAttribute(Qt.WA_TranslucentBackground)
        # self.clipboardManager.move(QPoint(x, y))
        # self.clipboardManager.show()
        pos = self.mapToGlobal(QPoint(x, y))
        self.clipboardManager.popup(pos)

    def updateTime(self, time: str):
        # print(time)
        page = self.browser.page()
        if page: page.runJavaScript(f"""
        time.textContent = "{time}" """)

    def updateDate(self, date: str):
        # print(date)
        page = self.browser.page()
        if page: page.runJavaScript(f"""
        date.textContent = "{date}" """)

    def updateTimeOfDay(self, timeOfDay: str):
        print(timeOfDay)
        page = self.browser.page()
        if page: page.runJavaScript(f"""
        .textContent = "{timeOfDay}" """)        

    def moveSelectionUp(self):
        self.browser.page().runJavaScript("""
        var selItems = document.getElementsByClassName("selected file_item");
        var id = selItems[selItems.length-1].id;
        var numItemsInRow = Math.floor(window.innerWidth/120);
        var itemSelPtr = document.getElementById(id);
        for (var i=0; i<numItemsInRow; i++) {
            itemSelPtr = itemSelPtr.previousSibling;
        }
        id = itemSelPtr.id;
        clearSelectedItems();
        selectItemById(id);
        ensureInView(document.getElementById(id));""")

    def moveSelectionDown(self):
        self.browser.page().runJavaScript("""
        var selItems = document.getElementsByClassName("selected file_item");
        var id = selItems[selItems.length-1].id;
        var numItemsInRow = Math.floor(window.innerWidth/120);
        var itemSelPtr = document.getElementById(id);
        for (var i=0; i<numItemsInRow; i++) {
            itemSelPtr = itemSelPtr.nextSibling;
        }
        id = itemSelPtr.id;
        clearSelectedItems();
        selectItemById(id);
        ensureInView(document.getElementById(id));""")

    def moveSelectionLeft(self):
        self.browser.page().runJavaScript("""
        var selItems = document.getElementsByClassName("selected file_item");
        var id = selItems[selItems.length-1].previousSibling.id;
        clearSelectedItems();
        selectItemById(id);
        ensureInView(document.getElementById(id));""")

    def moveSelectionRight(self):
        self.browser.page().runJavaScript("""
        var selItems = document.getElementsByClassName("selected file_item");
        var id = selItems[selItems.length-1].nextSibling.id;
        clearSelectedItems();
        selectItemById(id);
        ensureInView(document.getElementById(id));""")

    def getWindowTitle(self):
        return f"File Viewer ({Path(self.folder).name})"

    def EscHandler(self):
        '''handle ESC key'''
        if self.browser.searchPanel.isVisible():
            self.browser.searchPanel.closePanel()
        elif self.keypress_search.isVisible():
            self.keypress_search.hide()
        else: 
            self.selected_item = None
            self.clearSelection()

    def signalZoom(self, zoomValue: Union[float, None]=None):
        if zoomValue is None:
            zoomValue = self.browser.zoomFactor()
        self.zoomChanged.emit(100*zoomValue)
        print(f"zoomChanged.emit({100*zoomValue})")

    def toggleHiddenFiles(self):
        if self.hidden_visible:
            self.hidden_visible = False
            self.browser.page().runJavaScript('hideHiddenFiles();')
        else:
            self.hidden_visible = True
            self.browser.page().runJavaScript('showHiddenFiles();')
        
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

    def openSelected(self):
        print(f"openSelected({self.selected_item})")

    def reOpen(self):
        path = str(self.folder)
        self.open(path)

    def openFileInTerminal(self):
        """opens selected file in terminal."""
        pass

    def callXdgOpen(self, path: str) -> str:
        '''call xdg-open for the appropriate mimetype.'''
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        FigD.debug(f"{path}: calling xdg-open for {mimetype} files")
        url = QUrl.fromLocalFile(path).toString()
        os.system(f'xdg-open "{url}"')

        return mimetype

    def listFiles(self, path: str, **args):
        listed_mimetypes = []
        listed_and_full_paths_files = []
        listed_and_full_paths_folders = []
        # hidden files are marked by a 0 sort in reverse order or not
        reverse = args.get("reverse", False)
        for file in os.listdir(path):
            mimeType = self.mime_database.mimeTypeForFile(path)
            listed_mimetypes.append(mimeType.name())
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

        return listed, full_paths, hidden_flag_list, listed_mimetypes

    def getIcon(self, path):
        name = self.icon_provider.icon(QFileInfo(path)).name()
        # NOTE: paths where mimetype icons may be found.
        for theme_path in [
            "/usr/share/icons/breeze/devices/48",
            "/usr/share/icons/breeze/places/64",
            "/usr/share/icons/breeze/mimetypes/32",  
        ]: # get icon path for breeze theme.
            path = os.path.join(theme_path, name+".svg")
            if os.path.exists(path): return path

        return path

    def changeZoom(self, zoomValue: float):
        print(f"changeZoom({zoomValue})")
        self.browser.setZoomFactor(zoomValue/100)
        
    def createDialogue(self, item_type="file"):
        if item_type == "folder": 
            path = self.createFolder()
            icon = "file:///usr/share/icons/breeze/places/64/inode-directory.svg"
        elif item_type == "file": 
            path = self.createFile()
            icon = "file:///usr/share/icons/breeze/mimetypes/64/text-plain.svg"
        name = Path(path).name
        self.browser.createItem(path, name, icon, hidden=False) 

    def delSelItem(self):
        if self.selected_item is None: return
        print(f"moving {self.selected_item} to Trash")
        shutil.move(self.selected_item, FILE_VIEWER_TRASH_PATH)
        
    def renameDialog(self, path: Union[str, None]=None):
        '''rename file item, by creating an editable field.'''
        if path is None: path = self.selected_item
        print(f"renaming item at {path}")
        if self.selected_item:
            self.browser.initiateRenameForId(self.selected_item)

    def renameItem(self, id: str, new_name: str):
        parent = Path(id).parent
        new_name = os.path.join(parent, new_name)
        FigD.debug(f"renaming {id} to {new_name}")
        os.rename(id, new_name)

    def createFile(self):
        '''create a new empty file'''
        i = 1
        while True:
            path = os.path.join(self.folder, f"Untitled File {i}")
            if not os.path.exists(path): break
            else: i += 1
        FigD.debug(f"created new file: {path}")
        open(path, "w")

        return path

    def createFolder(self):
        '''create a new empty folder'''
        i = 1
        while True:
            try:
                path = os.path.join(self.folder, f"Untitled Folder {i}")
                os.mkdir(path); break
            except FileExistsError: i += 1
        FigD.debug(f"created new folder: {path}")

        return path

    def viewSource(self):
        """view source of the current view."""
        try: self.browser.page().triggerAction(QWebEnginePage.ViewSource)
        except Exception as e: 
            print("ui::system::fileviewer::FileViewerWidget.viewSource", e)

    def createThumbnailWorker(self, path: str, thumb_size: int) -> QThread:
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

    def open(self, folder: str="~"):
        from fig_dash.utils import collapseuser
        from fig_dash.ui.js.webchannel import QWebChannelJS
        from fig_dash.ui.js.filexplorer import FileViewerHtml, FileViewerStyle, FileViewerCustomJS, FileViewerMJS, ViSelectJS
        '''open a file/folder location.'''
        # print(f"background_image: url({self.background_image})")
        try: # print(self.dash_window)
            i = self.dash_window.tabs.currentIndex()
            self.dash_window.tabs.setTabText(i, folder)
        except AttributeError: pass 
        # expand user.
        folder = os.path.expanduser(folder)
        if folder != os.path.expanduser("~/Desktop") and os.path.isdir(folder):
            from fig_dash.ui.system.filexplorer import fileviewer_window_factory
            fileViewerWindow = fileviewer_window_factory(path=folder)
            fileViewerWindow.show()
            return fileViewerWindow
        self.file_watcher.addPath(folder)
        # call xdg-open if a file is clicked instead of a folder.
        if os.path.isfile(folder): 
            mimetype = self.callXdgOpen(folder)
            return
        # might be a device or something.
        if not os.path.isdir(folder): return
        # check if the user has permission to view folder
        try: os.scandir(folder)
        except PermissionError as e:
            print("fileviewer.open", e); return
        self.folder = Path(folder)
        listed, full_paths, hidden_flag_list, mimetypes_list = self.listFiles(folder)
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
        # iterate over full paths.
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
            mimeType = self.mime_database.mimeTypeForFile(path).name()
            icons.append((iconPath, mimeType, path))

        icon_theme_devices_path = "/usr/share/icons/breeze/devices/48"
        icon_theme_places_path = "/usr/share/icons/breeze/places/64"
        icon_theme_mimes_path = "/usr/share/icons/breeze/mimetypes/64"
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

        def format_listed(prelisted):
            listed = []
            for rec in prelisted:
                # rec = "_<br>".join(rec.split("_"))
                # rec = "<br>".join(chunk_string(rec))
                listed.append(rec)

            return listed         
        from fig_dash.ui.js.webchannel import QWebChannelJS
        from fig_dash.ui.js.desktop import DesktopDockCSS, DesktopHtml
        from fig_dash.ui.js.filexplorer import FileViewerEmbedHtml, FileViewerStyle, FileViewerCustomJS, FileViewerMJS, ViSelectJS
        self.params = {
            "FOLDER": self.folder.name,
            "FONT_COLOR": "#fff",
            "WEBCHANNEL_JS": QWebChannelJS,
            "FILEVIEWER_JS": ViSelectJS,
            "FILEVIEWER_MJS": FileViewerMJS,
            "FILEVIEWER_CSS": FileViewerStyle,
            "FILEVIEWER_CJS": FileViewerCustomJS,
            "PARENT_FOLDER": self.folder.parent.name,
            "FILEVIEWER_ICONS": icon_paths,
            "FILEVIEWER_PATHS": full_paths,
            "FILEVIEWER_ITEMS": format_listed(listed),
            "FILEVIEWER_MIMETYPES": mimetypes_list,
            "BACKGROUND_IMAGE": self.background_image,
            "HIDDEN_FLAG_LIST": hidden_flag_list,
            "NUM_ITEMS": len(listed),
            "CSS_GRAD": self.css_grad,
            "DESKTOP_DATETIME": datetime.datetime.now().strftime("%a %b %d %Y %-I:%M:%S %p"),
            "DESKTOP_DOCK_CSS": DesktopDockCSS.render(DESKTOP_BACKGROUND=self.background_image),
            "DESKTOP_CALENDAR_ICON": FigD.iconUrl("system/datetime/calendar.png"),
            "DESKTOP_CLOCK_TIME_OF_DAY": FigD.iconUrl("system/datetime/morning.png"),
        }
        self.params.update(self.systemHandler.js_sources)
        embedded_file_viewer_html = jinja2.Template(
            FileViewerEmbedHtml.render(**self.params)
        ).render(**self.params)
        self.params.update({"EMBEDDED_FILE_VIEWER": embedded_file_viewer_html})
        self.desktop_html = DesktopHtml.render(**self.params)
        render_url = FigD.createTempUrl(self.desktop_html)
        self.browser.load(render_url)
        s = time.time()
        for path in full_paths: 
            self.createThumbnailWorker(path=path, thumb_size=240)
        print(f"\x1b[32;1m**created thumbnail workers in {time.time()-s}s**\x1b[0m")

    def updateSelection(self, item):
        '''update widget state when currently selected item is changed'''
        self.selected_item = item
        code = jinja2.Template(r"""
try {
    var selItemSpan = selItemElement.getElementsByClassName('item_name')[0];
    selItemSpan.style.overflow = "hidden";
    selItemSpan.style.webkitLineClamp = 3;
}
catch(err) {
    console.log(err);
    var selItemElement = document.getElementById('{{ ID }}');
}
// change selected item element
selItemElement = document.getElementById('{{ ID }}');
var selItemSpan = selItemElement.getElementsByClassName('item_name')[0];
// show the fullname of the selected item's label (span).
selItemSpan.style.overflow = "";
selItemSpan.style.webkitLineClamp = 10;""").render(ID=item)
        self.browser.page().runJavaScript(code)
        self.selectionChanged.emit([self.selected_item])
        _, file_ext = os.path.splitext(item)
        if file_ext == "":
            file_ext = ".ext"
        icon = self.getIcon(item)
        mimetype = self.mime_database.mimeTypeForFile(item).name()
        file_info = QFileInfo(item)
        name = file_info.fileName()
        try:
            if file_info.isDir():
                items = len(os.listdir(item))
            else: items = 0
        except PermissionError as e: 
            items = 0
    # def keyPressEvent(self, event):
    #     try:
    #         letter = chr(event.key())
    #         # self.keypress_search.showPanel(
    #         #     parent=self, 
    #         #     w=self.width(),
    #         #     h=self.height(),
    #         # )
    #         # self.keypress_search.setText(letter.lower())
    #     except (TypeError, ValueError) as e:
    #         print("\x1b[31;1mfileviewer.keyPressEvent\x1b[0m", e)
    #         # fail silently.
    #     return super(DebugDesktopView, self).keyPressEvent(event)
    def onUrlChange(self):
        self.selected_item = None
        self.browser.setZoomFactor(1.35)
        self.browser.loadFinished.connect(self.loadDevTools)

    def copyUrlToClipboard(self):
        if self.selected_item:
            url = QUrl.fromLocalFile(self.selected_item).toString()
            QApplication.clipboard().setText(url)
            FigD.debug(f"copied {url} to clipboard")  

    def copyStemToClipboard(self):
        if self.selected_item:
            stem = Path(self.selected_item).stem
            QApplication.clipboard().setText(stem)
            FigD.debug(f"copied {stem} to clipboard")    

    def copyPathToClipboard(self):
        if self.selected_item:
            QApplication.clipboard().setText(self.selected_item)
            FigD.debug(f"copied {self.selected_item} to clipboard")

    def copyNameToClipboard(self):
        if self.selected_item:
            name = Path(self.selected_item).name
            QApplication.clipboard().setText(name)
            FigD.debug(f"copied {name} to clipboard")            

    @pyqtSlot()
    def selectAll(self):
        '''select all items.'''
        self.browser.page().runJavaScript('selectAllItems();')

    def reload(self):
        '''refresh the webview'''
        self.browser.reload()

    def scrollToItem(self, id: str):
        '''scroll item into view by id.'''
        code = f"document.getElementById('{id}').scrollIntoView()"
        self.browser.page().runJavaScript(code)

    def invertSelection(self):
        '''invert selected items.'''
        self.browser.page().runJavaScript('invertSelectedItems();')

    def highlightItem(self, id: str):
        '''select a specific item by id'''
        self.clearSelection()
        self.browser.page().runJavaScript(f"selectItemById('{id}')")

    def clearSelection(self):
        '''clear selected items.'''
        self.browser.page().runJavaScript('clearSelectedItems();')

    def copyToClipboard(self, text):
        QApplication.clipboard().setText(text)
        FigD.debug(f"copied {text} to clipboard")

# Dash desktop widget.
class DashDesktopWidget(QStackedWidget):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(DashDesktopWidget, self).__init__(parent=parent)

# FigD desktop window.
class FigDesktopWindow(QMainWindow):
    def __init__(self, background=DEFAULT_DESKTOP_BACKGROUND):
        super(FigDesktopWindow, self).__init__()
        self.virtual_desktops = DebugDesktopView(background=background)
        self.setCentralWidget(self.virtual_desktops)
        # window flags and icon.
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(FigD.Icon("fig.svg"))

    def keyPressEvent(self, event):
        return super(FigDesktopWindow, self).keyPressEvent(event)

# test desktop.
def test_desktop():
    import sys
    from fig_dash.ui import FigDAppContainer, wrapFigDWindow
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    desktop = FigDesktopWindow(
        background=FigD.wallpaper("pixabay/balloon.jpg")
    )
    figd_window = wrapFigDWindow(desktop, size=(25,25), icon="fig.svg", 
                                 title="Desktop", width=1600, height=1000, 
                                 add_tabs=False, app_name="Desktop")
    figd_window.showFullScreen()
    app.exec()

if __name__ == "__main__":
    test_desktop()