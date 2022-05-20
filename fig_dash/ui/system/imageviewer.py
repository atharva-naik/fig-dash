#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import bs4
import sys
import json
from fig_dash.ui import browser
import jinja2
import svgpathtools
from typing import *
from pathlib import Path
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.browser import DebugWebView
from fig_dash.theme import FigDAccentColorMap
from fig_dash.ui.titlebar import WindowTitleBar
from fig_dash.ui.effects import BackgroundBlurEffect
from fig_dash.ui import DashWidgetGroup, FigDAppContainer, styleContextMenu, wrapFigDWindow, extract_colors_from_qt_grad, create_css_grad
# PyQt5 imports
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QKeySequence, QColor, QFontDatabase, QPalette, QPainterPath, QRegion, QTransform
from PyQt5.QtCore import Qt, QSize, QPoint, QRectF, QTimer, QUrl, QDir, QMimeDatabase, QFileSystemWatcher, QSortFilterProxyModel
from PyQt5.QtWidgets import QAction, QWidget, QShortcut, QTreeView, QTreeWidget, QTreeWidgetItem, QSlider, QLineEdit, QMainWindow, QApplication, QSplitter, QLabel, QToolBar, QFileDialog, QToolButton, QSizePolicy, QVBoxLayout, QFileSystemModel, QTextEdit, QPlainTextEdit, QTabWidget, QHBoxLayout, QGraphicsDropShadowEffect, QMenu
# imageviewer widget.
FILTER_OPERATION_DETECTED = False
filterPaneJS = r"""
var viewerCanvas = document.getElementsByClassName("viewer-canvas")[0];
var filterPane = document.createElement("p");
filterPane.id = "filterPane";
filterPane.setAttribute("style", "bottom:0;left:0;overflow:hidden;position:absolute;right:0;top:0;backdrop-filter:blur(0px) brightness(100%) contrast(100%) drop-shadow(0px 0px 0px black) hue-rotate(0deg) invert(0%) grayscale(0%) opacity(100%) sepia(0%) saturate(100%)")
viewerCanvas.appendChild(filterPane);
console.log("filter pane creation was successfull");
"""
# hue-rotate, drop-shadow.
# IMAGEVIEWER_BLUR_FILTER_JS = r""""""
# IMAGEVIEWER_BRIGHTNESS_FILTER_JS = r""""""
# IMAGEVIEWER_CONTRAST_FILTER_JS = r""""""
# IMAGEVIEWER_DROP_SHADOW_FILTER_JS = r""""""
# IMAGEVIEWER_HUE_ROTATE_FILTER_JS = r""""""
# IMAGEVIEWER_INVERT_FILTER_JS = r""""""
# IMAGEVIEWER_GRAYSCALE_FILTER_JS = r""""""
# IMAGEVIEWER_OPACITY_FILTER_JS = r""""""
# IMAGEVIEWER_SEPIA_FILTER_JS = r""""""
# IMAGEVIEWER_SATURATE_FILTER_JS = r""""""
# blur(0px) brightness(100%) contrast(100%) drop-shadow(0px 0px 0px black) hue-rotate(0deg) invert(0%) grayscale(0%) opacity(100%) sepia(0%) saturate(100%)
scrollbar_style = '''
QScrollBar:vertical {
    border: 0px solid #999999;
    width: 12px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
/* QScrollBar:vertical:hover {
    background-color: rgba(255, 253, 184, 0.3);
} */
QScrollBar::handle:vertical {
    min-height: 0px;
    border: 0px solid red;
    border-radius: 0px;
    /* background-color: transparent; */
	background-color: rgba(255, 255, 255, 0.2);
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
}'''
file_tree_style = '''
QWidget {
    border: 0px;
    background: transparent;
    font-family: 'Be Vietnam Pro';
    font-size: 16px;
    color: #fff;
}
QScrollArea {
    background-position: center;
    border: 0px;
}
QScrollBar:vertical {
    border: 0px solid #999999;
    width: 15px;
    margin: 0px 0px 0px 0px;
    background-color: rgba(255, 255, 255, 0);
}
/* QScrollBar:vertical:hover {
    background-color: rgba(255, 253, 184, 0.3);
} */
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
}
'''
class ImageViewerViewGroup(DashWidgetGroup):
	def __init__(self, parent: Union[None, QWidget]=None):
		super(ImageViewerViewGroup, self).__init__(parent, "View")
		toggleWidget = QWidget()
		toggleWidget.setStyleSheet("background: transparent; color: #fff;")
		toggleLayout = QVBoxLayout()
		toggleLayout.setContentsMargins(0, 0, 0, 0)
		toggleLayout.setSpacing(0)
		toggleWidget.setLayout(toggleLayout)
		# add widgets to widget group.
		self.addWidget(toggleWidget)
		# self.layout.addWidget()

class ImageViewerMenu(QWidget):
	def __init__(self, parent: Union[None, QWidget]=None):
		super(ImageViewerMenu, self).__init__(parent)
		# create layout.
		self.layout = QHBoxLayout()
		self.layout.setSpacing(0)
		self.setFixedHeight(120)
		self.layout.setContentsMargins(0, 0, 0, 0)
		# create widget groups.
		self.viewgroup = ImageViewerViewGroup()
		# build layout.
		self.layout.addWidget(self.viewgroup)
		self.layout.addStretch()
		# set layout.
		self.setLayout(self.layout)

	def toggle(self):
		"""toggle the visibility of the ribbon menu."""
		if self.isVisible():
			self.hide()
		else: self.show()


class ImageViewerFileTree(QWidget):
    def __init__(self, root=os.path.expanduser("~"), parent=None):
        super(ImageViewerFileTree, self).__init__(parent)
        # veritcal layout.
        self.root = root  # root path.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addWidget(QLabel(root))
        # file system model.
        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(os.path.expanduser("~/Pictures"))
        # # create poxy filter sort model.
        # self.proxyModel = QSortFilterProxyModel()
        # self.proxyModel.setSourceModel(self.fileModel)
        # self.proxyModel.setFilterKeyColumn(1)
        # file tree view.
        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(
            self.fileModel.index(
                os.path.expanduser("~/Pictures")
            )
        )
        # # hide Size, Type and Date Modified.
        self.fileTree.hideColumn(1)
        self.fileTree.hideColumn(2)
        # self.fileTree.hideColumn(3)

        # hide scroll bar.
        self.fileTree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fileTree.clicked.connect(self.fileItemClicked)
        self.fileTree.setColumnWidth(0, 300)
        # self.fileTree.setMinimumHeight(400)
        # add file tree to layout.
        self.layout.addWidget(self.fileTree)

        self.setLayout(self.layout)
        self.setStyleSheet(file_tree_style)
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    # def setRootPath(self, path: str):
    #     if os.path.isfile(path):
    #         path = str(Path(path).parent)
    #     print("path:", path)
    #     self.root = path

    #     self.fileModel = QFileSystemModel()
    #     self.fileModel.setRootPath(path)

    #     self.fileTree.setModel(self.fileModel)
    #     self.fileTree.setRootIndex(
    #         self.fileModel.index(path)
    #     )
    #     self.fileTree.reset()
    def connectImageViewer(self, image_viewer: QWidget):
        self.image_viewer = image_viewer

    def fileItemClicked(self, index: int):
        filepath = self.sender().model().filePath(index)
        try:
            self.image_viewer
        except AttributeError as e:
            print(
                "\x1b[31;1mui.system.imageviewer.ImageViewerFileTree.fileItemClicked\x1b[0m", e)
        self.image_viewer.open(filepath)
        # print(filepath)

    def toggle(self):
        parent = self.parent()
        if self.isVisible():
            self.hide()
            icon = "show.svg"
        else:
            self.show()
            icon = "hide.svg"
        # if parent:
        # parent.fileBrowserVisBtn.setIcon(FigD.Icon(icon))
def getAbsolutePath(item):
	if item.parent() == None: 
		return item.text(0)
	else:
		# print("item =", item.text(0))
		return f"{getAbsolutePath(item.parent())}/{item.text(0)}"

class SVGTreeNode:
	def __init__(self, node: Union[bs4.element.Tag, svgpathtools.path.Arc, svgpathtools.path.Line, svgpathtools.path.CubicBezier],
				 treewidget: Union[None, QTreeWidget]=None):
		self._parent = None
		self._children = []
		self._record = {}
		self._node = node # store the node object
		# set the name field.
		# name can be line, arc, g, path, rect, title etc.
		if isinstance(node, bs4.element.Tag):
			self._name = node.name
		elif isinstance(node, svgpathtools.path.Arc):
			self._name = "arc"
		elif isinstance(node, svgpathtools.path.Line):
			self._name = "line"
		elif isinstance(node, svgpathtools.path.CubicBezier):
			self._name = "cubic bezier"
		else: 
			# TODO: safe way to deal with this without crashing UI.
			# need to write parsing function for this.
			raise TypeError(f"SVGTreeNode has invalid datatype: `{type(node)}`. node = {str(node)}")

		if treewidget is None:
			self._tree_widget_item = QTreeWidgetItem([self.name()])
		else:
			self._tree_widget_item = QTreeWidgetItem(treewidget, [self.name()])
		# build the subtree here (populate children)
		if self.name() in ["g", "defs"]:
			for child in node:
				if str(child).strip() == "":
					continue
				childNode = SVGTreeNode(child)
				self.addChild(childNode)
		elif self.name() == "path":
			self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/path.png"))
			path_objects = svgpathtools.parse_path(node.attrs["d"])
			for child in path_objects:
				childNode = SVGTreeNode(child)
				self.addChild(childNode)
		elif self.name() == "metadata":
			self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/metadata.png"))
			# print(node) # TODO: parse this into fields and values.
			self._record = {"content": str(node)}
		elif self.name() in ["lineargradient", "radialgradient"]:
			if self.name() == "lineargradient":
				self._tree_widget_item.setIcon(0, 
					FigD.Icon("system/imageviewer/linear_gradient.png")
				)
			elif self.name() == "radialgradient":
				self._tree_widget_item.setIcon(0, 
					FigD.Icon("system/imageviewer/radial_gradient.png")
				)
			for child in node:
				if str(child).strip() == "":
					continue
				childNode = SVGTreeNode(child)
				self.addChild(childNode)
			self._record = dict(node.attrs) 
		# elif self.name() == "stop":
		# 	self._record = dict(node.attrs)
		elif self.name() == "cubic bezier":
			self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/cubic_bezier.svg"))
			self._record["start"] = str(node.start)
			self._record["end"] = str(node.end)
			self._record["control1"] = str(node.control1)
			self._record["control2"] = str(node.control2)
		elif self.name() == "line":
			self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/line.png"))
			self._record["start"] = str(node.start)
			self._record["end"] = str(node.end)
		elif self.name() == "arc":
			self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/arc.png"))
			self._record["start"] = str(node.start)
			self._record["end"] = str(node.end)
			self._record["rotation"] = str(node.rotation)
			self._record["radius"] = str(node.radius)
			self._record["sweep"] = str(node.sweep)
			self._record["large arc"] = str(node.large_arc)
		# elif self.name() == "title":
		# 	self._record = {
		# 		"id": node.attrs.get("id", "-"),
		# 		"text": node.text,
		# 	}
		else:
			if node.name == "rect":
				self._tree_widget_item.setIcon(0, FigD.Icon("system/imageviewer/rect.png"))
			self._record = dict(node.attrs)
			# self._record = {
			# 	"id": node.attrs.get("id", "-"),
			# 	"fill": node.attrs.get("fill", "-"),
			# 	"width": node.attrs.get("width", "-"),
			# 	"height": node.attrs.get("height", "-"),
			# 	"opacity": node.attrs.get("opacity", "-"),
			# }
		self._tree_widget_item._record_ptr = self._record

	def toTreeWidgetItem(self):
		return self._tree_widget_item

	def name(self):
		return self._name

	def addChild(self, child):
		assert isinstance(child, SVGTreeNode), "invalid node type"
		self._tree_widget_item.addChild(child.toTreeWidgetItem())
		self._children.append(child)
		child.parent = self


class ImageViewerSVGTree(QWidget):
	def __init__(self, parent: Union[None, QWidget]=None):
		super(ImageViewerSVGTree, self).__init__(parent)
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(5, 5, 5, 5)
		# tree widget & details pane.
		self.tree = QTreeWidget()
		self.tree.setAnimated(True)
		self.tree.setFont(QFont("Be Vietnam Pro", 10))
		self.details_pane = self.initDetailsPane()
		self.splitter = QSplitter(Qt.Vertical)

		self.tree.setColumnCount(1)
		self.tree.setHeaderLabels(["element"])
		print(self.tree.verticalScrollBar().setStyleSheet(
			scrollbar_style
		))
		self._tree_records = {}
		# self.tree.setHeaderLabels(["name", "id", "text", "fill", "width", "height", "opacity", "start", "end", "radius", "rotation", "large arc", "sweep"])
		# self.tree.header().resizeSection(0, 100) # name
		# self.tree.header().resizeSection(1, 50) # id
		# self.tree.header().resizeSection(2, 100) # text
		# self.tree.header().resizeSection(3, 80) # fill
		# self.tree.header().resizeSection(4, 30) # width
		# self.tree.header().resizeSection(5, 50) # height
		# self.tree.header().resizeSection(6, 70) # opacity
		# self.tree.header().resizeSection(7, 50) # start
		# self.tree.header().resizeSection(8, 20) # end
		# self.tree.header().resizeSection(9, 50) # radius
		# self.tree.header().resizeSection(10, 70) # rotation
		# self.tree.header().resizeSection(11, 80) # large arc
		# self.true.header().resizeSection(12, 50) # sweep
		self.tree.itemClicked.connect(self.updateDetailsPane)
		self.tree.header().setStretchLastSection(True)
		# add tree & details pane to splitter.
		self.splitter.addWidget(self.tree)
		self.splitter.addWidget(self.details_pane)

		self.layout.addWidget(self.splitter)
		# self.layout.addStretch(1)
		self.setLayout(self.layout)

	def updateDetailsPane(self, item):
		record = item._record_ptr
		html = """
<div style="margin-left: auto; margin-right: auto; border: 1px solid green;">
	<table width="100%" style="background-color: rgba(152, 186, 60, 0.2); font-family: 'Be Vietnam Pro', sans-serif;">
		<thead border>
			<tr>
				<th style="border: 2px inset green; text-align: right; color: #72ff47;">field</th>
				<th style="border: 2px inset green; text-align: right; color: #72ff47;">value</th>
			</tr>
		</thead>
		<tbody>
"""
		for field, value in record.items():
			# html += f"""&nbsp;<span style="color: green; font-weight: bold;">{field}:</span> {value}<br>\n"""
			html += f"""
			<tr> 
				<td style="border: 2px inset green; text-align: right; color: #72ff47;">{field}</td>
				<td style="border: 2px inset green; text-align: right; color: #72ff47;">{value}</td>
			</tr>"""
		html += """
		</tbody>
	</table>
</div>"""
		self.details_pane.setHtml(html)	

	def initDetailsPane(self):
		pane = QTextEdit()
		pane.setReadOnly(True)
		pane.setText("")
		pane.setStyleSheet("""
		QScrollBar:vertical {
			border: 0px solid #999999;
			width: 15px;
			margin: 0px 0px 0px 0px;
			background-color: rgba(255, 255, 255, 0);
		}
		/* QScrollBar:vertical:hover {
			background-color: rgba(255, 253, 184, 0.3);
		} */
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
		
		return pane

	# def unfoldPath(self, path_key, path):
	# 	ctr = 0
	# 	op = {path_key: {}}
	# 	path = svgpathtools.parse_path(path)
	# 	# print("path_key =", path_key)
	# 	for part in path:
	# 		record = {}
	# 		record["end"] = str(part.end)
	# 		record["start"] = str(part.start)
	# 		if isinstance(part, svgpathtools.path.Line): 
	# 			op[path_key][f"line#{ctr}"] = record
	# 		elif isinstance(part, svgpathtools.path.Arc):
	# 			record["large arc"] = str(part.large_arc)
	# 			record["rotation"] = str(part.rotation)
	# 			record["radius"] = str(part.radius)
	# 			record["sweep"] = str(part.sweep)
	# 			op[path_key][f"arc#{ctr}"] = record
	# 		ctr += 1

	# 	return op

	# def parseSVGNode(self, node: bs4.element.Tag, key: str=""):
	# 	if node.name == "path":
	# 		path_d = str(node.attrs["d"])
	# 		return self.unfoldPath(key, path_d)
	# 		# svgpathtools.parse_path(path_d)
	# 	elif node.name == "g":
	# 		tree = {key: {}}
	# 		subctr = 0
	# 		for subnode in node:
	# 			if str(subnode).strip() == "": continue
	# 			tree[key][subnode.name+f"#{subctr}"] = self.parseSVGNode(subnode, key=subnode.name)
	# 			subctr += 1
	# 		return tree
	# 	elif node.name == "rect":
	# 		record = {
	# 			"id": node.attrs.get("id", "-"),
	# 			"fill": node.attrs.get("fill", "-"),
	# 			"width": node.attrs.get("width", "-"),
	# 			"height": node.attrs.get("height", "-"),
	# 			"opacity": node.attrs.get("opacity", "-"),
	# 		}
	# 		return record
	# 	elif node.name == "title":
	# 		record = {
	# 			"id": node.attrs.get("id", "-"),
	# 			"text": node.text,
	# 		}
	# 		return record
	# 	else: return {}

	# def buildTreeItems(self, tree):
	# 	treeItems = []
	# 	for name, subtree in tree.items():
	# 		if name.startswith("path"):
	# 			treeItem = QTreeWidgetItem([name])
	# 			# treeItem = QTreeWidgetItem(self.tree, [name])
	# 			# print(tree)
	# 			for key, record in subtree[name].items():
	# 				childItem = QTreeWidgetItem([key])
	# 				treeItem.addChild(childItem)
	# 				self._tree_records[getAbsolutePath(childItem)] = record
	# 		elif name.startswith("g"):
	# 			treeItem = QTreeWidgetItem([name])
	# 			for subname, subtree in tree[name].items():
	# 				subTreeItem = self.buildTreeItems(subtree)
	# 				treeItem.addChild(subTreeItem)
	# 		else: # rect etc.
	# 			record = subtree
	# 			treeItem = QTreeWidgetItem(self.tree, [name])
	# 			self._tree_records[getAbsolutePath(treeItem)] = record
	# 		treeItems.append(treeItem)

	# 	return treeItems

	def loadSVGData(self, svg_data: str="") -> dict:
		"""
		load the SVG Tree data from 
		Args:
			svg_data (str, optional): String format SVG data. Defaults to "".

		Returns:
			dict: JSON object for tree
		"""
		# from pprint import pprint
		tree = {}
		treeItems = []
		self.svg_data = bs4.BeautifulSoup(
			svg_data, features="html.parser"
		)
		# print(svg_data)
		self.svg = self.svg_data.find("svg")
		for child in self.svg.children:
			if str(child).strip() == "": continue
			treeNode = SVGTreeNode(child, treewidget=self.tree)
			treeItem = treeNode.toTreeWidgetItem()
			treeItems.append(treeItem)
		# print(json.dumps(tree))
		# for name, subtree in tree.items():
		# 	if name.startswith("path"):
		# 		treeItem = QTreeWidgetItem(self.tree, [name])
		# 		for key, record in subtree[name].items():
		# 			childItem = QTreeWidgetItem([key])
		# 			treeItem.addChild(childItem)
		# 			self._tree_records[getAbsolutePath(childItem)] = record
		# 	elif name.startswith("g"):
		# 		treeItem = QTreeWidgetItem(self.tree, [name])
		# 		for key, record in subtree[name].items():
		# 			childItem = QTreeWidgetItem([key])
		# 			treeItem.addChild(childItem)
		# 			self._tree_records[getAbsolutePath(childItem)] = record
		# 		# self._tree_records[getAbsolutePath(treeItem)] = record
		# 	else:
		# 		record = subtree
		# 		treeItem = QTreeWidgetItem(self.tree, [name])
		# 		self._tree_records[getAbsolutePath(treeItem)] = record
		# 	treeItems.append(treeItem)
		self.tree.insertTopLevelItems(0, treeItems)

		return tree


class ImageViewerEffectsPanel(QWidget):
	pass # effects: rotoscope, pixelate.

class ImageViewerLayers(QWidget):
	pass


class ImageViewerFilterSlider(QWidget):
	def __init__(self, text: str, icon: str="", icon_size: Tuple[int,int]=(25,25),
				 minm: int=0, maxm: int=50, value: int=100, accent_color: str="yellow",
				 parent: Union[QWidget, None]=None, webview: Union[DebugWebView, None]=None,
				 role: str="blur"):
# js_callback_code: Union[str, None]=None):
		super(ImageViewerFilterSlider, self).__init__(parent)
		self.webview = webview
		self.role = role
		# main layout.
		self.vboxlayout = QVBoxLayout()
		self.vboxlayout.setContentsMargins(0, 0, 0, 0)
		self.vboxlayout.setSpacing(0)
		# upper widget with hboxlayout.
		self.hboxlayout = QHBoxLayout()
		self.hboxlayout.setContentsMargins(0, 0, 0, 0)
		self.hboxlayout.setSpacing(0)
		# slider widget.
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(minm)
		self.slider.setMaximum(maxm)
		self.slider.setValue(value)
		self.slider.setMinimumWidth(200)
		# self.slider.setStyleSheet("")
		self.slider.valueChanged.connect(self.updateEffect)
		# self.slider.setStyleSheet("""
		# QSlider {
		# 	background: #292929;
		# }""")
		# text label.
		self.label = QLabel(text)
		self.label.setStyleSheet("""
		QLabel {
			font-size: 17px;
		}""")
		# slider readout.
		self.readout = QLineEdit()
		self.readout.setText(str(value))
		self.readout.setStyleSheet("""
		QLineEdit {
			font-size: 16px;
		}""")
		self.readout.setMaximumWidth(40)
		# display icon.
		self.icon = QLabel()
		self.icon.setPixmap(
			FigD.Icon(icon).pixmap(
				QSize(*icon_size)
		))
		# hboxwidget.
		self.hboxwidget = QWidget()
		self.hboxwidget.setLayout(self.hboxlayout)
		# build hboxlayout.
		self.hboxlayout.addWidget(self.icon)
		self.hboxlayout.addWidget(self.readout)
		self.hboxlayout.addWidget(self.slider)
		self.hboxlayout.addStretch(1)
		self.vboxlayout.addWidget(
			self.hboxwidget, 0, 
			Qt.AlignCenter
		)
		self.vboxlayout.addWidget(
			self.label, 0, 
			Qt.AlignCenter
		)
		self.vboxlayout.addStretch(1)
		self.setObjectName("ImageViewerFilterSlider")
		self.setStyleSheet("""
		QWidget#ImageViewerFilterSlider {
			color: #fff;
			font-family: 'Be Vietnam Pro';
			background: transparent;
		}""")
		self.setLayout(self.vboxlayout)
		# set slider palette color.
		background = accent_color
		if "qlineargradient" in background:
			sliderHandleColor = background.split(":")[-1].strip()
			sliderHandleColor = sliderHandleColor.split()[-1].split(")")[0]
			sliderHandleColor = sliderHandleColor.strip()
		else: 
			sliderHandleColor = background
		palette = QPalette()
		palette.setColor(QPalette.Window, QColor(0,255,255))
		palette.setColor(QPalette.Button, QColor(sliderHandleColor))
		palette.setColor(QPalette.Highlight, QColor(sliderHandleColor))
		self.slider.setPalette(palette)

	def _js_effect_applicator(self, currentStyle: str):
		print(currentStyle)
		if self.webview is not None:
			self.webview.page().runJavaScript(currentStyle)
		if self.role == "blur":
			currentStyle = currentStyle.replace("blur(0px)", f"blur({self.slider.value()}px")
		self.webview.page().runJavaScript(f"""document.getElementById("filterPane").setAttribute("style", '{currentStyle}');""")
		# currentStyle

	def updateEffect(self, value):
		global FILTER_OPERATION_DETECTED
		self.readout.setText(str(value))
		if not FILTER_OPERATION_DETECTED:
			FILTER_OPERATION_DETECTED = True
			if self.webview is None: return
			self.webview.page().runJavaScript(filterPaneJS)
		if self.webview is not None:
			self.webview.page().runJavaScript(
				'document.getElementById("filterPane").getAttribute("style")', 
				self._js_effect_applicator
			)
			# self.webview.page().runJavaScript(self.js_callback_code)


class ImageViewerFiltersPanel(QWidget):
	def __init__(self, parent: Union[QWidget, None]=None,
				 webview: Union[None, DebugWebView]=None,
				 accent_color: str="yellow"):
		super(ImageViewerFiltersPanel, self).__init__(parent)
		self.vboxlayout = QVBoxLayout()
		self.vboxlayout.setContentsMargins(10, 10, 10, 10)
		self.vboxlayout.setSpacing(5)
		self.blurSlider = ImageViewerFilterSlider(
			"blur (in px)", icon="system/fileviewer/blur.svg",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="blur"
		)
		self.brightnessSlider = ImageViewerFilterSlider(
			"brightness (in %)", icon="system/fileviewer/brightness.svg",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="brightness"
		)
		self.contrastSlider = ImageViewerFilterSlider(
			"contrast (in %)", icon="system/fileviewer/contrast.svg",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="contrast"
		)
		self.grayScaleSlider = ImageViewerFilterSlider(
			"gray scale (in %)", icon="system/fileviewer/grayscale.png",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="grayscale"
		)
		self.invertSlider = ImageViewerFilterSlider(
			"invert (in %)", icon="system/fileviewer/invert.svg",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="invert"
		)
		self.opacitySlider = ImageViewerFilterSlider(
			"opacity (in %)", icon="system/fileviewer/opacity.svg",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="opacity"
		)
		self.saturationSlider = ImageViewerFilterSlider(
			"saturation (in %)", icon="system/fileviewer/saturation.png",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="saturate"
		)
		self.sepiaSlider = ImageViewerFilterSlider(
			"sepia (in %)", icon="system/fileviewer/sepia.png",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="sepia"
		)
		self.hueRotateSlider = ImageViewerFilterSlider(
			"hue rotation (in ° )", icon="system/fileviewer/hue.png",
			minm=0, maxm=180, value=0, icon_size=(20,20),
			accent_color=accent_color, webview=webview,
			role="hue-rotate"
		)
		# self.dropShadowPicker = ImageViewerDropShadowPicker()
		self.vboxlayout.addWidget(
			self.blurSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.brightnessSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.contrastSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.grayScaleSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.invertSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.opacitySlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.saturationSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.sepiaSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		self.vboxlayout.addWidget(
			self.hueRotateSlider, 0, 
			Qt.AlignCenter | Qt.AlignTop
		)
		# self.vboxlayout.addWidget(
		# 	self.dropShadowPicker, 0, 
		# 	Qt.AlignCenter | Qt.AlignTop
		# )
		self.vboxlayout.addStretch(1)
		self.setLayout(self.vboxlayout)

		# self.vboxlayout.addWidget(self.)
class ImageViewerSidePanel(QTabWidget):
	def __init__(self, parent: Union[None, QWidget]=None,
				 webview: Union[None, DebugWebView]=None,
				 accent_color: str="yellow"):
		super(ImageViewerSidePanel, self).__init__()
		self.filters_panel = ImageViewerFiltersPanel(
			accent_color=accent_color, 
			webview=webview,
		)
		self.effects_panel = ImageViewerEffectsPanel()
		self.filetree = ImageViewerFileTree()
		self.svgtree = ImageViewerSVGTree()
		self.layers = ImageViewerLayers()
		self.addTab(self.filetree, "Folders")
		self.addTab(self.svgtree, "Elements")
		self.addTab(self.layers, "Layers")
		self.addTab(self.filters_panel, "Filters")
		self.addTab(self.effects_panel, "Effects")
		self.setStyleSheet("""color: #fff; background: #292929;""")
		self.setFont(QFont("Be Vietnam Pro", 10))

	def loadSVGData(self, svg_data: str=""):
		self.svgtree.loadSVGData(svg_data)

	def toggle(self):
		if self.isVisible():
			self.hide()
		else: self.show()


class ImageViewerWebView(DebugWebView):
    def __init__(self, *args, imageviewer=None, **kwargs):
        super(ImageViewerWebView, self).__init__(*args, **kwargs)
        self.imageviewer = imageviewer
        self.accent_color = "yellow" 
        self.shortcut_mapper = {}
        # self.menu = self.createContextMenu()
    def setAccentColor(self, accent_color):
        self.accent_color = accent_color

    def inspectTriggered(self):
        print(f"triggered inspect dev_view.isVisible() = {self.dev_view.isVisible()}")
        if not self.dev_view.isVisible():
            self.dev_view.show()
        self.inspect_action.trigger()
        print(f"triggered inspect dev_view.isVisible() = {self.dev_view.isVisible()}")

    def activateShortcut(self, action: QAction):
        # def printMapper(d):
        #     dmap = {}
        #     for k,v in d.items():
        #         dmap[k] = v.text()
        #     print(dmap)
        for keySeq in action.shortcuts():
            if keySeq.toString() in self.shortcut_mapper: continue
            self.shortcut_mapper[keySeq.toString()] = QShortcut(keySeq, self)
            self.shortcut_mapper[keySeq.toString()].activated.connect(action.trigger)
        # printMapper(self.shortcut_mapper)
    def createContextMenu(self) -> QMenu:
        self.contextMenuActions = []
        menu = self.page().createStandardContextMenu()
        menu.setObjectName("ImageViewerContextMenu")
        background_blur = BackgroundBlurEffect()
        background_blur.setEnabled(False)
        background_blur.setBlurRadius(10)
        menu.setGraphicsEffect(background_blur)
        # data = self.page().contextMenuData()
        menu = styleContextMenu(menu, accent_color=self.accent_color)
        for action in menu.actions():
            # buddself.addAction(action)
            # self.contextMenuActions.append(action)
            # self.contextMenuActions[-1].setShortcutContext(Qt.WidgetWithChildrenShortcut)
            if action.text() == "Save page":
                action.setIcon(FigD.Icon("system/imageviewer/save_page.svg"))
                action.setShortcut(QKeySequence("Ctrl+Shift+S"))
            elif action.text() == "View page source":
                action.setShortcut(QKeySequence("Ctrl+U"))
                action.setIcon(FigD.Icon("titlebar/source.svg"))
            elif action.text() == "Back":
                action.setShortcut(QKeySequence.Back)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("system/imageviewer/prev.svg"))
                else:
                    action.setIcon(FigD.Icon("system/imageviewer/prev_disabled.svg"))
            elif action.text() == "Forward":
                action.setShortcut(QKeySequence.Forward)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("system/imageviewer/next.svg"))
                else:
                    action.setIcon(FigD.Icon("system/imageviewer/next_disabled.svg"))
            elif action.text() == "Reload":
                action.setShortcut(QKeySequence.Refresh)
                action.setIcon(FigD.Icon("system/imageviewer/reload.svg"))
            elif action.text() == "Save image":
                action.setShortcut(QKeySequence.Save)
                action.setIcon(FigD.Icon("system/imageviewer/save_image.svg"))
                action.triggered.connect(self.imageviewer.saveImage)
            elif action.text() == "Copy image":
                action.setShortcut(QKeySequence.Copy)
                action.setIcon(FigD.Icon("browser/copy.svg"))
            elif action.text() == "Copy image address":
                action.setShortcut(QKeySequence("Ctrl+Shift+C"))
                action.setIcon(FigD.Icon("system/imageviewer/copy_image_address.svg"))
            elif action.text() == "Inspect":
                self.inspect_action = action
                action.setVisible(False) # hide original aspect action.
                wrappedInspectAction = menu.addAction("Inspect")
                wrappedInspectAction.setShortcut(QKeySequence("Ctrl+Shift+I"))
                if wrappedInspectAction.isEnabled():
                    wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
                else:
                    wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
                wrappedInspectAction.triggered.connect(
                    self.inspectTriggered
                ) 
            self.activateShortcut(action)
        # js snippets.
        zoomInJS = 'document.getElementsByClassName("viewer-zoom-in")[0].click();'
        zoomOutJS = 'document.getElementsByClassName("viewer-zoom-out")[0].click();'
        origSizeJS = 'document.getElementsByClassName("viewer-one-to-one")[0].click();'
        rotateACJS = 'document.getElementsByClassName("viewer-rotate-left")[0].click();'
        rotateCCJS = 'document.getElementsByClassName("viewer-rotate-right")[0].click();'
        flipHJS = 'document.getElementsByClassName("viewer-flip-horizontal")[0].click();'
        flipVJS = 'document.getElementsByClassName("viewer-flip-vertical")[0].click();'
        # additional ImageViewer actions.
        menu.addSeparator()
        menu.addAction(FigD.Icon("titlebar/zoom_in.svg"), "Zoom in", lambda: self.page().runJavaScript(zoomInJS))
        menu.addAction(FigD.Icon("titlebar/zoom_out.svg"), "Zoom out", lambda: self.page().runJavaScript(zoomOutJS))
        menu.addAction("Original size", lambda: self.page().runJavaScript(origSizeJS))
        menu.addSeparator()
        menu.addAction(
			FigD.Icon("system/imageviewer/rotate_cc.svg"), "Rotate 90° clockwise", 
			lambda: self.page().runJavaScript(rotateCCJS)
		)
        menu.addAction(
			FigD.Icon("system/imageviewer/rotate_ac.svg"), "Rotate 90° anti-clockwise", 
			lambda: self.page().runJavaScript(rotateACJS)
		)
        menu.addSeparator()
        menu.addAction(FigD.Icon("system/imageviewer/flip_horizontal.svg"), "Flip horizontally", lambda: self.page().runJavaScript(flipHJS))
        menu.addAction(FigD.Icon("system/imageviewer/flip_vertical.svg"), "Flip vertically", lambda: self.page().runJavaScript(flipVJS))

        return menu

    def contextMenuEvent(self, event):
        self.menu = self.createContextMenu()
        data = self.page().contextMenuData()
        self.menu.popup(event.globalPos())
        # elif data.mediaType() == 0:
        #     for action in self.menu.actions():
        #         print(action.text())
class ImageViewerWidget(QWidget):
    """
    [summary]
    Widget for viewing images
    - If a filepath is given: image viewer is opened.
    - If a folderpath is given: image gallery is opened.

    # UI Elements
    This section describes the UI design of the ImageViewer.


    # Browser (MainView) (as Image Viewer):

    OR

    # Browser (MainView) (as Image Gallery):
    # Viewer modes
    1. 2D flow-layout
    2. carousel mode
    3. 3D carousel (max 20 images)
    4. list mode
    5. tree mode
    """
    def __init__(self, **args):
        super(ImageViewerWidget, self).__init__()
		# arguments.
        print(args.keys())
        self.svg_data = None
        self.sources = args.get("sources", {})
        self.css_grad = args.get("css_grad", "gray")
        accent_color = args.get("accent_color", "yellow")
        # connect a mimedatabase.
        self.mime_database = QMimeDatabase()
        self.file_watcher = QFileSystemWatcher()
        # create layout
        layout = QVBoxLayout()
        # TODO: Check if margin is needed anymore at all.
        margin = 10
        layout.setContentsMargins(margin, 0, margin, margin)
        layout.setSpacing(0)
        self.layout = layout
        # build layout.
        self.browser = ImageViewerWebView(imageviewer=self)
        self.file_watcher.fileChanged.connect(self.browser.reload)
        # self.statusbar = self.statusBar()
        # self.statusbar.setStyleSheet("""
        # QWidget {
        #     color: gray;
        #     background: #000;
        # }""")
        self.side_panel = ImageViewerSidePanel(
			accent_color=accent_color,
			webview=self.browser,
		)
        self.svgtree = self.side_panel.svgtree
        self.filetree = self.side_panel.filetree
        self.filetree.connectImageViewer(self)
        self.side_panel.hide()
        # self.filetree.hide()
        self.browser.splitter.insertWidget(0, self.side_panel)
        layout.addWidget(self.browser.splitter)
        # set layout.
        self.setLayout(layout)

		# connect slots to signals.
        self.browser.urlChanged.connect(self.onUrlChange)
        # parameters stuff.
        self.zoom_factor = args.get("zoom_factor", 1.3)
        # set icon.
        self._fullscreen = False

    def saveImage(self):
        name = Path(self.path_ptr).name
        filename, _ = QFileDialog.getSaveFileName(
			self, "Save image file to ...", 
			name, "Image Files (*.png)"
		)
        print(filename)
        if filename is not None:
            # self.page().runJavaScript("")
            pass

    def loadSVGData(self, svg_data: str=""):
        self.svgtree.loadSVGData(svg_data)

    def viewSource(self):
        # print("showing source")
        # print(self.svg_data)
        textarea = QPlainTextEdit()
        if self.svg_data: 
            textarea.setPlainText(str(self.svg_data))
        else:
            textarea.setPlainText("Not an SVG (no source available)")
        textarea.setStyleSheet("background: #292929; color: #fff;")
        window = wrapFigDWindow(textarea)
        window.show()

    def initCentralWidget(self):
        centralWidget = QWidget()
        # init layout.
        layout = QVBoxLayout()
        margin = 10
        layout.setContentsMargins(margin, 0, margin, margin)
        layout.setSpacing(0)
        self.layout = layout
        # build layout.
        self.browser = ImageViewerWebView()
        self.browser.imageviewer = self
        # self.statusbar = self.statusBar()
        # self.statusbar.setStyleSheet("""
        # QWidget {
        #     color: gray;
        #     background: #000;
        # }""")
        self.side_panel = ImageViewerSidePanel()
        self.svgtree = self.side_panel.svgtree
        self.filetree = self.side_panel.filetree
        self.filetree.connectImageViewer(self)
        self.side_panel.hide()
        # self.filetree.hide()
        self.browser.splitter.insertWidget(0, self.side_panel)
        layout.addWidget(self.browser.splitter)
        # set layout.
        centralWidget.setLayout(layout)

    def onUrlChange(self):
        self.browser.setZoomFactor(self.zoom_factor)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):        
        self.browser.loadDevTools()
        # self.browser.page().runJavaScript("viewer.full();")
    def openUrl(self, path: str):
        filename_without_ext = str(Path(path).stem)
        isdir = os.path.isdir(path)
        # populate gallery info if path points to a folder.
        gallery_info = []
        if isdir:
            for iter_file in os.listdir(path):
                iter_file = os.path.join(path, iter_file)
                mimetype = self.mime_database.mimeTypeForFile(iter_file).name()
                if not mimetype.startswith("image"):
                    continue
                url = QUrl.fromLocalFile(iter_file).toString()
                gallery_info.append((url, Path(iter_file).stem))
        url = QUrl.fromLocalFile(path).toString()
        html = self.sources["IMAGE_VIEWER_HTML"].render({
            "FILEPATH": path,
            "FILEPATH_URL": url,
            "FILENAME_WITHOUT_EXT": filename_without_ext,
            "VIEWER_JS_PLUGIN_JS": self.sources["VIEWER_JS_PLUGIN_JS"],
            "VIEWER_JS_PLUGIN_CSS": self.sources["VIEWER_JS_PLUGIN_CSS"],
            "PATH_IS_FOLDER": isdir,
            "GALLERY_INFO": gallery_info,
			"CSS_GRAD": self.css_grad,
        })
        if self.window_ptr is not None:
            self.setWindowTitle(filename_without_ext)
        render_url = FigD.createTempUrl(html)
        self.browser.load(render_url)

    def connectMenu(self, menu: ImageViewerMenu):
        self.menu = menu
        self.menu.hide()
    # def connectTitlebar(self, titlebar: WindowTitleBar):
    #     self.titlebar = titlebar
    #     self.titlebar.findBtn.setParent(None)
    #     self.titlebar.connectWindow(self)
    #     rcb = self.titlebar.ribbonCollapseBtn
    #     try: rcb.clicked.connect(self.menu.toggle)
    #     except AttributeError as e: print(e)

    def open(self, path: str):
        self.svg_data = None
        path = os.path.expanduser(path)
        self.file_watcher.addPath(path)
        self.path_ptr = path
        filename_without_ext = str(Path(path).stem)
        isdir = os.path.isdir(path)
		# load SVG data.
        self.svgtree.tree.clear()
        self.svgtree.details_pane.setText("click on element on the SVG tree to view details")
        if path.endswith(".svg"):
            svg_data = open(path).read()
            self.loadSVGData(svg_data=svg_data)
            self.svg_data = svg_data 
        # populate gallery info if path points to a folder.
        gallery_info = []
        if isdir:
            for iter_file in os.listdir(path):
                iter_file = os.path.join(path, iter_file)
                mimetype = self.mime_database.mimeTypeForFile(iter_file).name()
                if not mimetype.startswith("image"):
                    continue
                url = QUrl.fromLocalFile(iter_file).toString()
                gallery_info.append((url, Path(iter_file).stem))
        url = QUrl.fromLocalFile(path).toString()
        html = self.sources["IMAGE_VIEWER_HTML"].render({
            "FILEPATH": path,
            "FILEPATH_URL": url,
            "FILENAME_WITHOUT_EXT": filename_without_ext,
            "VIEWER_JS_PLUGIN_JS": self.sources["VIEWER_JS_PLUGIN_JS"],
            "VIEWER_JS_PLUGIN_CSS": self.sources["VIEWER_JS_PLUGIN_CSS"],
            "PATH_IS_FOLDER": isdir,
            "GALLERY_INFO": gallery_info,
			"CSS_GRAD": self.css_grad,
        })
        if self.window_ptr is not None:
            self.setWindowTitle(filename_without_ext)
        render_url = FigD.createTempUrl(html)
        self.browser.load(render_url)
        # self.filetree.setRootPath(path)
        # print(path)
def launch_imageviewer(app):
    from fig_dash.ui.js.imageviewer import ViewerJSPluginCSS, ViewerJSPluginJS, ImageViewerHTML
    image_viewer_sources = {
		"IMAGE_VIEWER_HTML": ImageViewerHTML,
		"VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS,
		"VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
	}
    # titlebar.setStyleSheet("background: transparent; color: #fff;")
    menu = ImageViewerMenu()
    menu.hide()
    # accent color and css grad color.
    accent_color = FigDAccentColorMap["imageviewer"]
    grad_colors = extract_colors_from_qt_grad(accent_color)
    css_grad = create_css_grad(grad_colors)
    # create imageviewer widget.
    imageviewer = ImageViewerWidget(
		css_grad=css_grad, 
		accent_color=accent_color,
		sources=image_viewer_sources,
	)
    imageviewer.browser.setAccentColor(accent_color)
    imageviewer.connectMenu(menu)
    imageviewer.layout.insertWidget(0, menu)
    # imageviewer.layout.insertWidget(0, titlebar)
    # FullScreen = QShortcut(QKeySequence.FullScreen, imageviewer)
    # FullScreen.activated.connect(titlebar.fullscreenBtn.toggle)
    window = wrapFigDWindow(
		imageviewer, title="Image Viewer", 
		icon="system/imageviewer/logo.svg",
		accent_color=accent_color,
		titlebar_callbacks={
			"viewSourceBtn": imageviewer.viewSource,
            # "ribbonCollapseBtn": menu.toggle,
		}
	)
    window.show()
    try: openpath = sys.argv[1]
    except IndexError: 
        openpath = "~/GUI/FigUI/FigUI/FigTerminal/static/terminal.svg"
    imageviewer.open(openpath)
    CtrlB = QShortcut(QKeySequence("Ctrl+B"), imageviewer)
    CtrlB.activated.connect(imageviewer.side_panel.toggle)

def test_imageviewer():
    from fig_dash.ui.js.imageviewer import ViewerJSPluginCSS, ViewerJSPluginJS, ImageViewerHTML
    image_viewer_sources = {
		"IMAGE_VIEWER_HTML": ImageViewerHTML,
		"VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS,
		"VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
	}
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    menu = ImageViewerMenu()
    # menu.hide()
    # accent color and css grad color.
    accent_color = FigDAccentColorMap["imageviewer"]
    grad_colors = extract_colors_from_qt_grad(accent_color)
    css_grad = create_css_grad(grad_colors)
    # create imageviewer widget.
    imageviewer = ImageViewerWidget(
		css_grad=css_grad,
		accent_color=accent_color,
		sources=image_viewer_sources,
	)
    imageviewer.browser.setAccentColor(accent_color)
    imageviewer.connectMenu(menu)
    imageviewer.layout.insertWidget(0, menu)
    # imageviewer.layout.insertWidget(0, titlebar)
    imageviewer.setStyleSheet("background: transparent; border: 0px;")
    # FullScreen = QShortcut(QKeySequence.FullScreen, imageviewer)
    # FullScreen.activated.connect(titlebar.fullscreenBtn.toggle)
    window = wrapFigDWindow(
		imageviewer, title="Image Viewer", 
		icon="system/imageviewer/logo.svg",
		accent_color=accent_color, name="imageviewer",
		titlebar_callbacks={
			"viewSourceBtn": imageviewer.viewSource,
            # "ribbonCollapseBtn": menu.toggle,
		}
	)
    window.show()

    try: openpath = sys.argv[1]
    except IndexError: 
        openpath = "~/GUI/FigUI/FigUI/FigTerminal/static/terminal.svg"
    imageviewer.open(openpath)
    CtrlB = QShortcut(QKeySequence("Ctrl+B"), imageviewer)
    CtrlB.activated.connect(imageviewer.side_panel.toggle)

    app.exec()
# def test_imageviewer():
#     import sys
#     from fig_dash.ui.titlebar import TitleBar

#     FigD("/home/atharva/GUI/fig-dash/resources")
#     app = QApplication(sys.argv)
#     # set app stylesheet.
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

#     titlebar = WindowTitleBar(background="qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #be9433, stop : 0.091 #c49935, stop : 0.182 #ca9d36, stop : 0.273 #cfa238, stop : 0.364 #d5a639, stop : 0.455 #dbab3b, stop : 0.545 #e1af3d, stop : 0.636 #e7b43e, stop : 0.727 #edb940, stop : 0.818 #f3be42, stop : 0.909 #f9c243, stop : 1.0 #ffc745)")
#     # titlebar.setStyleSheet("background: transparent; color: #fff;")
#     menu = ImageViewerMenu()
#     menu.hide()
#     imageviewer = ImageViewerWidget(
#         logo="system/imageviewer/logo.svg",
#         parentless=True,
#     )
#     imageviewer.setAttribute(Qt.WA_TranslucentBackground)
#     # imageviewer.centralWidget().setAttribute(Qt.WA_TranslucentBackground)
#     imageviewer.titlebar = titlebar
#     imageviewer.connectMenu(menu)
#     imageviewer.connectTitlebar(titlebar)
#     imageviewer.layout.insertWidget(0, menu)
#     imageviewer.layout.insertWidget(0, titlebar)
#     imageviewer.setStyleSheet("background: transparent; border: 0px;")
#     QFontDatabase.addApplicationFont(
#         FigD.font("BeVietnamPro-Regular.ttf")
#     )
#     try: openpath = sys.argv[1]
#     except IndexError: openpath = "~/GUI/FigUI/FigUI/FigTerminal/static/terminal.svg"
#     imageviewer.open(openpath)
#     # imageviewer.open("~/Pictures/Wallpapers/Smock_FolderArchive_18_N.svg")
# 	# imageviewer.open("~/Pictures/KiaraHololive.jpeg")
#     # imageviewer.open("~/Pictures/Elena_Posterised.png")
#     imageviewer.setGeometry(100, 100, 960, 800)
#     imageviewer.setWindowFlags(
#         Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#     # app.setWindowIcon(FigD.Icon("system/imageviewer/logo.svg"))
# 	# attach Ctrl+B to sidebar collapse.
#     CtrlB = QShortcut(QKeySequence("Ctrl+B"), imageviewer)
#     CtrlB.activated.connect(imageviewer.side_panel.toggle)
#     FullScreen = QShortcut(QKeySequence.FullScreen, imageviewer)
#     FullScreen.activated.connect(titlebar.fullscreenBtn.toggle)
#     # print(FullScreen)
#     # FullScreen.activated.connect(imageviewer.toggleFullScreen)
#     titlebar.setWindowIcon(imageviewer.windowIcon())
#     titlebar.resetSliderPalette()
#     imageviewer.show()
#     app.exec()
if __name__ == "__main__":
    test_imageviewer()
# class ImageViewerWidget(QMainWindow):
#     """
#     [summary]
#     Widget for viewing images
#     - If a filepath is given: image viewer is opened.
#     - If a folderpath is given: image gallery is opened.

#     # UI Elements
#     This section describes the UI design of the ImageViewer.


#     # Browser (MainView) (as Image Viewer):

#     OR

#     # Browser (MainView) (as Image Gallery):
#     # Viewer modes
#     1. 2D flow-layout
#     2. carousel mode
#     3. 3D carousel (max 20 images)
#     4. list mode
#     5. tree mode
#     """

#     def __init__(self, **args):
#         super(ImageViewerWidget, self).__init__()
#         # connect a mimedatabase.
#         self.mime_database = QMimeDatabase()
#         # set central widget.
#         centralWidget = self.initCentralWidget()
#         self.setCentralWidget(centralWidget)
#         # connect slots to signals.
#         self.browser.urlChanged.connect(self.onUrlChange)
#         # parameters stuff.
#         self.parentless = args.get("parentless")
#         self.zoom_factor = args.get("zoom_factor", 1.3)
#         # set icon.
#         self._fullscreen = False
#         logo = args.get("logo")
#         logo = FigD.Icon(logo)
#         self.setWindowIcon(logo)

#     def loadSVGData(self, svg_data: str=""):
#         self.svgtree.loadSVGData(svg_data)

#     # def toggleFullScreen(self):
#     #     print("Full Screen")
#     #     if self._fullscreen:
#     #         self.showNormal()
#     #         self._fullscreen = False
#     #     else: 
#     #         self.showFullScreen()
#     #         self._fullscreen = True

#     def initCentralWidget(self):
#         centralWidget = QWidget()
#         # init layout.
#         layout = QVBoxLayout()
#         margin = 10
#         layout.setContentsMargins(margin, 0, margin, margin)
#         layout.setSpacing(0)
#         self.layout = layout
#         # build layout.
#         self.browser = ImageViewerWebView()
#         # self.statusbar = self.statusBar()
#         # self.statusbar.setStyleSheet("""
#         # QWidget {
#         #     color: gray;
#         #     background: #000;
#         # }""")
#         self.side_panel = ImageViewerSidePanel()
#         self.svgtree = self.side_panel.svgtree
#         self.filetree = self.side_panel.filetree
#         self.filetree.connectImageViewer(self)
#         self.side_panel.hide()
#         # self.filetree.hide()
#         self.browser.splitter.insertWidget(0, self.side_panel)
#         layout.addWidget(self.browser.splitter)
#         # set layout.
#         centralWidget.setLayout(layout)
#         centralWidget.setObjectName("ImageViewerCentralWidget")
#         centralWidget.setStyleSheet("""
#         QWidget#ImageViewerCentralWidget {
#             border-radius: 20px;
#             background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0.3 rgba(48, 48, 48, 1), stop : 0.6 rgba(29, 29, 29, 1));
#         }""")

#         return centralWidget

#     def onUrlChange(self):
#         self.browser.setZoomFactor(self.zoom_factor)
#         self.browser.loadFinished.connect(self.onLoadFinished)

#     def onLoadFinished(self):        
#         self.browser.loadDevTools()
#         # self.browser.page().runJavaScript("viewer.full();")
#     def openUrl(self, path: str):
#         filename_without_ext = str(Path(path).stem)
#         isdir = os.path.isdir(path)
#         # populate gallery info if path points to a folder.
#         gallery_info = []
#         if isdir:
#             for iter_file in os.listdir(path):
#                 iter_file = os.path.join(path, iter_file)
#                 mimetype = self.mime_database.mimeTypeForFile(iter_file).name()
#                 if not mimetype.startswith("image"):
#                     continue
#                 url = QUrl.fromLocalFile(iter_file).toString()
#                 gallery_info.append((url, Path(iter_file).stem))
#         url = QUrl.fromLocalFile(path).toString()
#         html = ImageViewerHTML.render({
#             "FILEPATH": path,
#             "FILEPATH_URL": url,
#             "FILENAME_WITHOUT_EXT": filename_without_ext,
#             "VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS,
#             "VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
#             "PATH_IS_FOLDER": isdir,
#             "GALLERY_INFO": gallery_info,
#         })
#         if self.parentless:
#             self.setWindowTitle(filename_without_ext)
#         render_url = FigD.createTempUrl(html)
#         self.browser.load(render_url)

#     def connectMenu(self, menu: ImageViewerMenu):
#         self.menu = menu

#     def connectTitlebar(self, titlebar: WindowTitleBar):
#         self.titlebar = titlebar
#         self.titlebar.findBtn.setParent(None)
#         self.titlebar.connectWindow(self)
#         rcb = self.titlebar.ribbonCollapseBtn
#         try: rcb.clicked.connect(self.menu.toggle)
#         except AttributeError as e: print(e)

#     def open(self, path: str):
#         path = os.path.expanduser(path)
#         filename_without_ext = str(Path(path).stem)
#         isdir = os.path.isdir(path)
# 		# load SVG data.
#         self.svgtree.tree.clear()
#         self.svgtree.details_pane.setText("click on element on the SVG tree to view details")
#         if path.endswith(".svg"):
#             svg_data = open(path).read()
#             self.loadSVGData(svg_data=svg_data) 
#         # populate gallery info if path points to a folder.
#         gallery_info = []
#         if isdir:
#             for iter_file in os.listdir(path):
#                 iter_file = os.path.join(path, iter_file)
#                 mimetype = self.mime_database.mimeTypeForFile(iter_file).name()
#                 if not mimetype.startswith("image"):
#                     continue
#                 url = QUrl.fromLocalFile(iter_file).toString()
#                 gallery_info.append((url, Path(iter_file).stem))
#         url = QUrl.fromLocalFile(path).toString()
#         html = ImageViewerHTML.render({
#             "FILEPATH": path,
#             "FILEPATH_URL": url,
#             "FILENAME_WITHOUT_EXT": filename_without_ext,
#             "VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS,
#             "VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
#             "PATH_IS_FOLDER": isdir,
#             "GALLERY_INFO": gallery_info,
#         })
#         if self.parentless:
#             self.setWindowTitle(filename_without_ext)
#         render_url = FigD.createTempUrl(html)
#         self.browser.load(render_url)