#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This sucks right now. Need to improve it!
import os
import sys
from typing import *
from ansi2html import Ansi2HTMLConverter
# fig dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import DashWidgetGroup, FigDAppContainer, styleContextMenu, wrapFigDWindow
from fig_dash.theme import FigDAccentColorMap, FigDSystemAppIconMap
# PyQt5 imports.
from PyQt5.QtGui import QIcon, QColor, QWindow, QTextFormat, QKeySequence#, QFont, QImage, QPixmap, QKeySequence#, QFontDatabase, QPalette, QPainterPath, QRegion, QTransform
from PyQt5.QtCore import Qt, QSize, QPoint, QRectF, QTimer, QUrl, QDir, QTimer, QProcess, QStringListModel, pyqtSlot
from PyQt5.QtWidgets import QAction, QWidget, QShortcut, QLineEdit, QMainWindow, QApplication, QSplitter, QLabel, QToolBar, QFileDialog, QToolButton, QSizePolicy, QVBoxLayout, QFileSystemModel, QTextEdit, QPlainTextEdit, QHBoxLayout, QMenu, QCompleter

# ribbon menu for DashTerminalMenu.
class DashTerminalMenu(DashWidgetGroup):
    def __init__(self, parent: Union[QWidget, None]=None):
        super(DashTerminalMenu, self).__init__(parent)


class DashWebTerminal(QWidget):
    pass

def contract_path(path):
    return path.replace(os.path.expanduser("~"), "~")

class TerminalCommandInput(QLineEdit):
    def __init__(self, path: str="", parent: Union[None, QWidget]=None):
        super(TerminalCommandInput, self).__init__(parent)
        # create actions.
        searchAction = self.addAction(
            FigD.Icon("browser/search.svg"), 
            QLineEdit.LeadingPosition
        )
        copyAction = self.addAction(
            FigD.Icon("browser/copy.svg"), 
            QLineEdit.TrailingPosition
        )
        copyAction.triggered.connect(self.copyCommand)
        self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            padding: 5px;
            background: #292929;
            border-radius: 5px;
        }""")
        self.setPlaceholderText("Type command to be executed. Use ↑ and ↓ to navigate history")
        self.updateCompleter(path)
        self.setMinimumWidth(600)
        self.setClearButtonEnabled(True)
        self.cmd_history = []
        self.curr_idx = -1
        self._backup_text = ""

    def appendCommand(self, cmd: str):
        self.cmd_history.append(cmd)
        self.curr_idx = len(self.cmd_history)

    def copyCommand(self):
        cmd = self.text().strip()
        QApplication.clipboard().setText(cmd)

    def updateCompleter(self, path):
        self.qcompleter = QCompleter()
        completion_paths = []
        for file in os.listdir(path):
            completion_paths.append(f"cd {file}")
            abs_path = os.path.join(path, file)
            completion_paths.append(f"cd {abs_path}")
            contracted_path = contract_path(abs_path)
            completion_paths.append(f"cd {contracted_path}")
            completion_paths.append(f"ls {file}")
            completion_paths.append(f"ls {abs_path}")
            completion_paths.append(f"ls {contracted_path}")
        stringModel = QStringListModel(completion_paths)
        self.qcompleter.setCompletionMode(QCompleter.InlineCompletion)
        self.qcompleter.setModel(stringModel)
        self.setCompleter(self.qcompleter)

    def keyPressEvent(self, event):
        # print(event.key())
        if event.key() == Qt.Key_Tab:
            print("tab pressed", self.text())
            return
        elif event.key() == Qt.Key_Up:
            if self.curr_idx == len(self.cmd_history):
                self._backup_text = self.text()
            if self.curr_idx >= 0: 
                self.curr_idx = max(self.curr_idx-1, 0)
                cmd_history = self.cmd_history+[self._backup_text]
                self.setText(cmd_history[self.curr_idx])
                # print(f"previous item: {cmd_history[self.curr_idx]}")
        elif event.key() == Qt.Key_Down:
            if self.curr_idx == len(self.cmd_history):
                self._backup_text = self.text()
            if self.curr_idx >= 0: 
                self.curr_idx = min(self.curr_idx+1, len(self.cmd_history))
                cmd_history = self.cmd_history+[self._backup_text]
                self.setText(cmd_history[self.curr_idx])
                # print(f"next item: {cmd_history[self.curr_idx]}")
        super(TerminalCommandInput, self).keyPressEvent(event)

    def reset(self, path):
        pass


class TerminalCommandOutput(QPlainTextEdit):
    """The output area for terminal command output"""
    def __init__(self, path: str="", accent_color: str="gray", 
                 parent: Union[None, QWidget]=None):
        super(TerminalCommandOutput, self).__init__(parent)
        self.setStyleSheet("""
        QPlainTextEdit {
            color: #fff;
            padding: 5px;
            background: transparent;
            /* background: rgba(41, 41, 41, 0.8); */
        }""")
        self.accent_color = accent_color
        self.menu = self.createStandardContextMenu()
    
    def clearOutput(self):
        """
        Clear the QPlainTextEdit (similar to clear command on a terminal)
        """
        self.setPlainText("")

    def contextMenuEvent(self, event): 
        self.menu = self.createStandardContextMenu()
        self.menu = styleContextMenu(self.menu, self.accent_color)
        self.menu.popup(event.globalPos())


class RedirectShellContainer(QWidget):
    def __init__(self, path: str="~", accent_color: str="gray", 
                parent: Union[None, QWidget]=None):
        super(RedirectShellContainer, self).__init__(parent)
        path = os.path.expanduser(path)
        self.path = path
        self.output = TerminalCommandOutput(accent_color=accent_color)
        self.input = TerminalCommandInput(path=path)
        self.input.returnPressed.connect(self.runCommand)
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(5, 5, 5, 5)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.addWidget(self.output)
        self.vboxlayout.addWidget(self.input)
        self.output_formatter = Ansi2HTMLConverter()
        self.setLayout(self.vboxlayout)

    def runCommand(self):
        cmd = self.input.text().strip()
        self.input.appendCommand(cmd)
        if cmd == "clear":
            self.output.clearOutput()
        else:
            stdouterr = os.popen(cmd).read()
            ansi = "".join(stdouterr) # print(ansi)
            html = self.output_formatter.convert(ansi) # print(html)
            self.output.appendHtml(html)
        self.input.setText("")
        # print(cmd)

class GnomeShellContainer(QWidget):
    '''You can display images with lsix.'''
    def __init__(self, term: str="xterm", accent_color: str="gray", 
                 parent: Union[None, QWidget]=None, height: int=25, 
                 cmd: Union[None, str]=None):
        super(GnomeShellContainer, self).__init__(parent)
        print(term)
        if term == "xterm":
            flags = ['-into', winId, 
                    # '-ls',
                    '-xrm', "'XTerm*selectToClipboard: true'",
                    '-ti', 'vt340', 
                    '-fa', 'Monospace', 
                    '-fs', '11', 
                    '-geometry', f'300x{height}', 
                    '-background', '#300a24']
        elif term == "urxvt":
            # urxvt --font "xft:Monospace:size=11" -depth 32 -bg rgba:3800/3800/3800/fa00 -fg rgb:ff00/ff00/ff00
            flags = ['-embed', winId, 
                    '-depth', '32', 
                    '-fg', 'rgb:ff00/ff00/ff00', 
                    '-geometry', f'300x{height}', 
                    '--font', 'xft:Monospace:size=11',
                    '-bg', 'rgba:3800/3800/3800/fa00']
        elif term == "redirect":
            self.shell = RedirectShellContainer(accent_color=accent_color)
            self.vboxlayout = QVBoxLayout()
            self.vboxlayout.setContentsMargins(0, 0, 0, 0)
            self.vboxlayout.setSpacing(0)
            self.vboxlayout.addWidget(self.shell)
            self.setLayout(self.vboxlayout)
        if term in ["xterm", "urxvt"]:
            self.process = QProcess(self)
            winId = str(int(self.winId()))
            if cmd is not None: 
                "executes the command in `cmd` at startup."
                flags += ["-e", f'"{cmd}"']
            print(cmd)
            self.process.start(term, flags)
            print(winId)
        # blankWindow = QTextEdit()
        # blankWindow.setReadOnly(True)
        # blankWindow.setsetFixedWidth(800)
        # blankWindow.setFixedHeight(20*height+20)
        # if parent:
        #     parent.logger.addWidget(self.loggerWindow)
        #     parent.logger.info(f"xterm opened into a window with id: {int(self.winId())}")
        # layout.addWidget(blankWindow)
        # self.setLayout(layout)
def wrapInQWindow(widget: QWidget):
    qwindow = QWindow.fromWinId(widget.winId())
    container = QWidget.createWindowContainer(qwindow)
    
    return container

def wrapInQWidget(widget: QWidget):
    wrap = QWidget()
    wrap.setObjectName("WrapWidget")
    wrap.setStyleSheet("""
    QWidget#WrapWidget{
        border: 0px;
        background: transparent;
    }""")
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    wrap.setLayout(layout)

    return wrap


class TerminalLogWindow(QTextEdit):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(TerminalLogWindow, self).__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
        QTextEdit {
            background:#ffdb78; 
            color: black;
        }""")
        self.cursorPositionChanged.connect(self.highlightLine)
        self.setLineWrapColumnOrWidth(200)
        self.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.verticalScrollBar().minimum()

    def toggle(self):
        print("toggled log window.")
        if self.isVisible():
            self.hide()
        else: self.show()

    def highlightLine(self):
        selections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        selections.append(selection)
        self.setExtraSelections(selections) 


class DashGnomeTerminal(QSplitter):
    def __init__(self, term="xterm", accent_color: str="gray", 
                 parent: Union[QWidget, None]=None, height: int=25,
                 cmd: Union[None, str]=None):
        super(DashGnomeTerminal, self).__init__(Qt.Vertical, parent=parent)
        self.gnomeShell = GnomeShellContainer(
            accent_color=accent_color,
            term=term, parent=parent, 
            height=height, cmd=cmd,
        )
        if term in ["xterm", "urxvt"]:
            self.gnomeShellUI = wrapInQWindow(self.gnomeShell)
        else: 
            self.gnomeShellUI = self.gnomeShell
        self.logWindow = TerminalLogWindow() 
        self.logWindow.hide()
        # self.logWindow.hide()
        self.addWidget(self.gnomeShellUI)
        self.addWidget(self.logWindow)
        # self.CtrlB = QShortcut(QKeySequence("Ctrl+B"), self)
        # self.CtrlB.activated.connect(self.logWindow.toggle)
        # self.setMinimumHeight(700)
class TerminalMenu(QWidget):
    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()


class DashTerminalWidget(QWidget):
    """
    A terminal widget that can handle various backends:
    tsh, csh, bash shell (gnome), web terminal (custom) etc.
    """
    def __init__(self, term: str="xterm", accent_color: str="gray",
                 parent: Union[None, QWidget]=None):
        super(DashTerminalWidget, self).__init__(parent)
        self.menu = TerminalMenu()
        # Gnome based terminal (QWindow wrapper around a gnome terminal instance)
        self._gnome_terminal = DashGnomeTerminal(term=term, accent_color=accent_color)
        self.gnome_terminal = wrapInQWidget(self._gnome_terminal)
        # create layout.
        self.vboxlayout = QVBoxLayout() 
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.logWindow = self._gnome_terminal.logWindow
        # self.CtrlB = QShortcut(QKeySequence("Ctrl+B"), self)
        # self.CtrlB.activated.connect(self._gnome_terminal.logWindow.toggle)
        # build layout.
        self.vboxlayout.addWidget(self.menu)
        self.vboxlayout.addWidget(self.gnome_terminal)
        # set layout.
        self.setLayout(self.vboxlayout)

def launch_terminal(app):
    icon = FigDSystemAppIconMap["terminal"]
    accent_color = FigDAccentColorMap["terminal"]
    terminal = DashTerminalWidget(accent_color=accent_color)
    window = wrapFigDWindow(terminal, icon=icon, 
                            accent_color=accent_color,
                            width=900, height=500)
    window.show()    

def test_terminal():
    app = FigDAppContainer(sys.argv)
    icon = FigDSystemAppIconMap["terminal"]
    accent_color = FigDAccentColorMap["terminal"]
    terminal = DashTerminalWidget(term="redirect", accent_color=accent_color)
    window = wrapFigDWindow(terminal, icon=icon,
                            accent_color=accent_color,
                            width=900, height=500)
    window.CtrlB = QShortcut(QKeySequence("Ctrl+B"), window)
    window.CtrlB.activated.connect(terminal.logWindow.toggle)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # dependencies: xterm, urxvt
    # installation: 
    # xterm: sudo apt-get install xterm
    # urxvt: sudo apt-get install rxvt-unicode
    test_terminal()