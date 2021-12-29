#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import jinja2
from typing import Union
# Qt imports.
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTabWidget, QWidget, QToolButton, QLabel, QApplication, QLineEdit, QMenu, QAction, QVBoxLayout, QHBoxLayout, QComboBox
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.widget.jupyter_nb import JupyterNBWidget
# QScintilla

dash_git_ui_style = '''
QWidget#DashGitUI {
    color: #fff;
    background: #000;
}'''
class GitUIBtn(QToolButton):
    def __init__(self, parent: Union[None, QWidget]=None, **kwargs):
        super(GitUIBtn, self).__init__(parent)
        icon = kwargs.get("icon")
        if icon:
            self.inactive_icon = os.path.join("widget/git", icon)
            stem, ext = os.path.splitext(icon)
            self.active_icon = os.path.join("widget/git", stem+"_active"+ext)
            self.setIcon(FigD.Icon(self.inactive_icon))
        tip = kwargs.get("tip", "a tip")
        size = kwargs.get("size", (23,23))
        self.setIconSize(QSize(*size))
        self.setToolTip(tip)
        self.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')

    def enterEvent(self, event):
        self.setIcon(FigD.Icon(self.active_icon))
        super(GitUIBtn, self).enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(FigD.Icon(self.inactive_icon))
        super(GitUIBtn, self).leaveEvent(event)


class GitBranchDropdown(QComboBox):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(GitBranchDropdown, self).__init__(parent)
        self.addItem("main")
        self.currentIndexChanged.connect(self.switchBranch)

    def switchBranch(self):
        pass


class GitBranchToolbar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(GitBranchToolbar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.mergeBtn = GitUIBtn(
            self, icon="merge.svg",
            tip="merge branch",
        )
        self.newBranchBtn = GitUIBtn(
            self, icon="new_branch.svg",
            tip="create new branch",
        )
        self.delBranchBtn = GitUIBtn(
            self, icon="delete_branch.svg",
            tip="delete branch",
        )
        self.branchDropdown = GitBranchDropdown()
        self.branchDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.mergeBtn)
        self.layout.addWidget(self.newBranchBtn)
        self.layout.addWidget(self.delBranchBtn)
        self.layout.addWidget(self.branchDropdown)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class GitRepoToolbar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(GitRepoToolbar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.diffBtn = GitUIBtn(
            self, icon="diff.svg",
            tip="show diff/changes",
        )
        self.forkBtn = GitUIBtn(
            self, icon="fork.svg",
            tip="fork git repo",
        )
        self.pullBtn = GitUIBtn(
            self, icon="pull.svg",
            tip="pull changes from remote",
        )
        self.pushBtn = GitUIBtn(
            self, icon="push.svg",
            tip="push changes to remote",
        )
        self.forcePushBtn = GitUIBtn(
            self, icon="force_push.svg",
            tip="force push changes to remote",
        )
        self.createRepoBtn = GitUIBtn(
            self, icon="create_git_repo.svg",
            tip="create a git repo",
        )
        self.cloneRepoBtn = GitUIBtn(
            self, icon="clone_git_repo.svg",
            tip="clone a git repo",
        )
        self.commitBtn = GitUIBtn(
            self, icon="commit.svg",
            tip="commit changes to local git",
        )
        self.branchDropdown = GitBranchDropdown()
        self.branchDropdown.setFixedWidth(150)
        self.layout.addStretch(1)
        self.layout.addWidget(self.diffBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.forkBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.createRepoBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.cloneRepoBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.commitBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.pullBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.pushBtn, 0, Qt.AlignCenter)
        self.layout.addWidget(self.forcePushBtn, 0, Qt.AlignCenter)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class GitEditToolbar(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(GitEditToolbar, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.addBtn = GitUIBtn(
            self, icon="add_file.svg",
            tip="stage files for commit",
        )
        self.revertBtn = GitUIBtn(
            self, icon="revert.svg",
            tip="revert changes",
        )
        self.revertBtn.setIconSize(QSize(20,20))
        self.resetBtn = GitUIBtn(
            self, icon="reset.svg",
            tip="reset git changes",
        )
        self.resetBtn.setIconSize(QSize(20,20))
        self.stashBtn = GitUIBtn(
            self, icon="stash.svg",
            tip="reset git changes",
        )
        self.stashBtn.setIconSize(QSize(20,20))
        self.layout.addStretch(1)
        self.layout.addWidget(self.addBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.stashBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.resetBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.revertBtn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addStretch(1)
        # print(self.toolbar.branchDropdown.styleSheet())
        self.setLayout(self.layout)


class DashGitUI(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None):
        super(DashGitUI, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # create widgets.
        self.branch_toolbar = GitBranchToolbar(self)
        self.repo_toolbar = GitRepoToolbar(self)
        self.edit_toolbar = GitEditToolbar(self)
        # add widgets to layout.
        self.layout.addWidget(self.repo_toolbar)
        self.layout.addWidget(self.branch_toolbar)
        self.layout.addWidget(self.edit_toolbar)
        
        self.setObjectName("DashGitUI")
        self.setStyleSheet(dash_git_ui_style)
        # print(self.toolbar.branchDropdown.styleSheet())
        self.setLayout(self.layout)


def test_git_ui():
    import sys
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = QApplication(sys.argv)
    git_ui = DashGitUI()
    git_ui.show()
    app.exec()


if __name__ == "__main__":
    test_git_ui()