#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::ui::system::terminal")
# This sucks right now. Need to improve it!
import os
import sys
import socket
import getpass
import pathlib
import subprocess
from typing import *
from ansi2html import Ansi2HTMLConverter
# fig dash imports.
from fig_dash.assets import FigD
from fig_dash.ui import DashWidgetGroup, FigDAppContainer, styleContextMenu, wrapFigDWindow, styleTextEditMenuIcons
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
    def __init__(self, path: str="", accent_color: str="gray", 
                 parent: Union[None, QWidget]=None):
        super(TerminalCommandInput, self).__init__(parent)
        self.accent_color = accent_color
        # create actions.
        searchAction = self.addAction(
            FigD.Icon("system/terminal/lambda.png"), 
            QLineEdit.LeadingPosition
        )
        copyAction = self.addAction(
            FigD.Icon("system/terminal/copy.svg"), 
            QLineEdit.TrailingPosition
        )
        copyAction.triggered.connect(self.copyCommand)
        self.setStyleSheet("""
        QLineEdit {
            color: #fff;
            padding: 0px;
            font-size: 19px;
            border-radius: 5px;
            background: transparent;
            /* background: #292929; */
        }""")
        self.setPlaceholderText("Type command to be executed. Use ↑ and ↓ to navigate history")
        self.resetCompleter(path)
        self.setMinimumWidth(600)
        self.setClearButtonEnabled(True)
        self.cmd_history = []
        self.curr_idx = -1
        self._backup_text = ""
        self.completion_paths = []
        self.menu = self.createStandardContextMenu()

    def appendCommand(self, cmd: str):
        self.cmd_history.append(cmd)
        self.curr_idx = len(self.cmd_history)

    def copyCommand(self):
        cmd = self.text().strip()
        QApplication.clipboard().setText(cmd)

    def updateCompleter(self, path):
        # initialize with the current list of completion paths.
        completion_paths = self.completion_paths
        self.qcompleter = QCompleter()
        # add commands.
        for file in os.listdir(path):
            # absolute and contracted paths.
            abs_path = os.path.join(path, file)
            contracted_path = contract_path(abs_path)
            # append the completion paths for current folder.
            completion_paths.append(f"cd {file}")
            completion_paths.append(f"ls {file}")
            # append the absolute completion paths.
            completion_paths.append(f"cd {abs_path}")
            completion_paths.append(f"ls {abs_path}")
            # append the contracted completion paths ("HOME"/"USER" directory is replaced with "~").
            completion_paths.append(f"cd {contracted_path}")
            completion_paths.append(f"ls {contracted_path}")
        # create string list model.
        stringModel = QStringListModel(completion_paths)
        # save the current set of paths in the object.
        self.completion_paths = completion_paths
        # reset the completer and the string model for the completer.
        self.qcompleter.setCompletionMode(QCompleter.InlineCompletion)
        self.qcompleter.setModel(stringModel)
        self.setCompleter(self.qcompleter)

    def resetCompleter(self, path):
        completion_paths = []
        self.qcompleter = QCompleter()
        # add commands.
        for file in os.listdir(path):
            # absolute and contracted paths.
            abs_path = os.path.join(path, file)
            contracted_path = contract_path(abs_path)
            # append the completion paths for current folder.
            completion_paths.append(f"cd {file}")
            completion_paths.append(f"ls {file}")
            # append the absolute completion paths.
            completion_paths.append(f"cd {abs_path}")
            completion_paths.append(f"ls {abs_path}")
            # append the contracted completion paths ("HOME"/"USER" directory is replaced with "~").
            completion_paths.append(f"cd {contracted_path}")
            completion_paths.append(f"ls {contracted_path}")
        # create string list model.
        stringModel = QStringListModel(completion_paths)
        # save the current set of paths in the object.
        self.completion_paths = completion_paths
        # reset the completer and the string model for the completer.
        self.qcompleter.setCompletionMode(QCompleter.InlineCompletion)
        self.qcompleter.setModel(stringModel)
        self.setCompleter(self.qcompleter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            # print("tab pressed", self.text())
            return
        elif event.key() in [Qt.Key_Up, Qt.Key_Down]:
            if self.curr_idx == len(self.cmd_history):
                self._backup_text = self.text()
            if self.curr_idx >= 0:
                if event.key() == Qt.Key_Up: 
                    self.curr_idx = max(self.curr_idx-1, 0)
                    # print(f"previous item: {cmd_history[self.curr_idx]}")
                elif event.key() == Qt.Key_Down:
                    self.curr_idx = min(self.curr_idx+1, len(self.cmd_history))
                    # print(f"next item: {cmd_history[self.curr_idx]}")
                cmd_history = self.cmd_history+[self._backup_text]
                self.setText(cmd_history[self.curr_idx])
        super(TerminalCommandInput, self).keyPressEvent(event)

    def contextMenuEvent(self, event): 
        self.menu = self.createStandardContextMenu()
        self.menu = styleContextMenu(self.menu, self.accent_color)
        self.menu = styleTextEditMenuIcons(self.menu)
        self.menu.popup(event.globalPos())

    def reset(self, path):
        pass


class TerminalPathLabel(QTextEdit):
    def __init__(self, accent_color: str="gray", 
                 parent: Union[QWidget, None]=None):
        super(TerminalPathLabel, self).__init__(parent=parent)
        self.accent_color = accent_color
        self.setStyleSheet("""
        QTextEdit {
            color: #fff;
            margin: 0px;
            padding: 0px;
            font-size: 18px;
            /* background: black; */
            background: transparent;
        }""")
        self.path = ""
        self.setReadOnly(True)
        self.setFixedHeight(25)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    def contextMenuEvent(self, event):
        self.contextMenu = self.createStandardContextMenu()
        self.contextMenu.addAction(
            FigD.Icon("system/fileviewer/copy_filepath.png"),
            "Copy path to clipboard",
            self.copyPathToClipboard,
        )
        self.contextMenu.addAction(
            FigD.Icon("system/fileviewer/copy_as_url.svg"),
            "Copy path as url",
            self.copyPathAsUrl,
        )
        self.contextMenu = styleContextMenu(
            self.contextMenu, 
            self.accent_color
        )
        self.contextMenu.popup(event.globalPos())

    def copyPathToClipboard(self):
        QApplication.clipboard().setText(self.path)

    def copyPathAsUrl(self):
        url = QUrl.fromLocalFile(self.path).toString()
        QApplication.clipboard().setText(url)

    def setPath(self, path: str):
        self.path = os.path.expanduser(path)
        self.setText(path)

    def setText(self, text: str):
        text = contract_path(text)
        text = f"<span style='color: #ff0032; font-weight: bold;'>&nbsp; └─── </span><span style='color: #ddff80; font-weight: bold;'>{getpass.getuser()}@{socket.gethostname()}</span>:<span style='color: #44fc94; font-weight: bold'>{text}</span>"
        super(TerminalPathLabel, self).setHtml(text)

# html output produced after running the terminal command.
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
        self.lineno_ctr = 0
        self.setReadOnly(True)
        self.accent_color = accent_color
        self.contextMenu = self.createStandardContextMenu()
    
    def appendCmdOutput(self, html: str):
        self.lineno_ctr += 1
        html = f"<span style='color: #4e9a06;'>[</span><span style='color: #8ae234; font-weight: bold;'>{self.lineno_ctr}</span><span style='color: #4e9a06;'>]</span>" + html
        self.appendHtml(html)

    def clearOutput(self):
        """
        Clear the QPlainTextEdit (similar to clear command on a terminal)
        """
        self.setPlainText("")

    def contextMenuEvent(self, event): 
        self.contextMenu = self.createStandardContextMenu()
        self.menu = styleContextMenu(self.contextMenu, self.accent_color)
        self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
        self.contextMenu.popup(event.globalPos())


class RedirectShellContainer(QWidget):
    def __init__(self, path: str="~", accent_color: str="gray", 
                 parent: Union[None, QWidget]=None):
        super(RedirectShellContainer, self).__init__(parent)
        path = os.path.expanduser(path)
        self.path = path
        os.chdir(path)
        self.input = TerminalCommandInput(path=path, accent_color=accent_color)
        self.output = TerminalCommandOutput(accent_color=accent_color)
        self.pathLabel = TerminalPathLabel(
            accent_color=accent_color,
        )
        self.pathLabel.setPath(path)
        self.input.returnPressed.connect(self.runCommand)
        self.input.textChanged.connect(self.expandPaths)
        # create VBoxLayout.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(5, 5, 5, 5)
        self.vboxlayout.setSpacing(0)
        # build VBoxLayout.
        self.vboxlayout.addWidget(self.output)
        self.vboxlayout.addWidget(self.input)
        self.vboxlayout.addWidget(self.pathLabel)
        
        self.output_formatter = Ansi2HTMLConverter()
        self.setLayout(self.vboxlayout)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else: self.show()

    def expandPaths(self):
        cmd = self.input.text().strip()
        try:
            if cmd.split()[0].strip() == "cd":
                path = " ".join(cmd.split()[1:]).strip()
                # print(os.path.exists(path))
        except IndexError as e:
            print(e)

    def runCommand(self):
        cmd = self.input.text().strip()
        self.input.appendCommand(cmd)
        if cmd == "clear":
            self.output.clearOutput()
        elif cmd.startswith("cd"):
            path = cmd.split("cd")[-1].strip()
            if path == "..":
                path = str(pathlib.Path(self.path).parent)
            elif path.startswith("/"): pass
            else:
                path = os.path.join(self.path, path)
            if not os.path.isdir(path):
                ansi = f"bash: cd: {path}: Not a directory"
                html = self.output_formatter.convert(ansi)
                self.output.appendCmdOutput(html)                
            elif os.path.exists(path): # print(path)
                os.chdir(path)
                self.path = path
                self.pathLabel.setPath(self.path)
            else:
                ansi = f"\x1b[31;1mbash: {path}\x1b[0m" 
                html = self.output_formatter.convert(ansi)
                self.output.appendCmdOutput(html)
        elif cmd == "exit":
            # TODO: change this to tab close.
            QApplication.instance().quit()
        else:
            # stdouterr = os.popen(cmd).read()
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            stdout = stdout.decode("utf-8")
            stderr = stderr.decode("utf-8")
            # print("out:", stdout, "error:", stderr)
            if stderr == "":
                ansi = "".join(stdout)
            else:
                ansi = "\x1b[31;1m"+"".join(stderr)+"\x1b[0m"
            html = self.output_formatter.convert(ansi)
            self.output.appendCmdOutput(html)
        self.input.setText("")

    def changeZoom(self, zoomValue: float):
        print(zoomValue)
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
            # print(cmd)
            self.process.start(term, flags)
            # print(winId)
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