#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fig_dash import FigDLoad
FigDLoad("fig_dash::ui::system::imageviewer")

import base64
import argparse
import PIL, bs4
import requests
import svgpathtools
from typing import *
from pathlib import Path
from functools import partial
from PIL import Image, ImageCms
import os, io, re, sys, time, platform
# fig-dash imports.
from fig_dash.assets import FigD
from fig_dash.ui.webview import DebugWebView, DebugWebBrowser
from fig_dash.ui import DashRibbonMenu, DashSimplifiedMenu, FigDMainWidget, FigDAppContainer, FigDNavBar, FigDShortcut, styleContextMenu, styleTextEditMenuIcons, wrapFigDWindow, extract_colors_from_qt_grad, create_css_grad, extractFromAccentColor
# PyQt5 imports
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap, QKeySequence, QColor, QFontMetricsF, QPalette, QPainterPath, QRegion, QTransform
from PyQt5.QtCore import Qt, QSize, QObject, QPoint, QRectF, QTimer, QUrl, QThread, QMimeDatabase, QFile, QFileInfo, QFileSystemWatcher, QSortFilterProxyModel, pyqtSignal, QStringListModel
from PyQt5.QtWidgets import QAction, QWidget, QCompleter, QShortcut, QTreeView, QTreeWidget, QTreeWidgetItem, QSlider, QLineEdit, QApplication, QSplitter, QLabel, QToolBar, QFileDialog, QToolButton, QSizePolicy, QVBoxLayout, QFileSystemModel, QTextEdit, QPlainTextEdit, QTabWidget, QHBoxLayout, QGraphicsDropShadowEffect, QMenu
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
IMAGEVIEWER_BACKDROP_REGEX_MAP = {
	"blur": "blur\(.*?px\)",
	"sepia": "sepia\(.*?\%\)",
	"invert": "invert\(.*?\%\)",
	"opacity": "opacity\(.*?\%\)",
	"contrast": "contrast\(.*?\%\)",
	"saturate": "saturate\(.*?\%\)",
	"grayscale": "grayscale\(.*?\%\)",
	"brightness": "brightness\(.*?\%\)",
	"hue-rotate": "hue-rotate\(.*?deg\)",
}
IMAGEVIEWER_IMG_EXTRACT_JS = r"""
function extractImageBytes(img) {
	var canvas = document.createElement('canvas');
	var context = canvas.getContext('2d');
	canvas.height = img.naturalHeight;
	canvas.width = img.naturalWidth;
	context.filter = img.style.filter
	context.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
	
	return canvas.toDataURL();
}"""
IMAGEVIEWER_BYTES_EXTRACT_JS = IMAGEVIEWER_IMG_EXTRACT_JS+r"""
var imgElement = document.getElementsByClassName("viewer-canvas")[0].getElementsByTagName("img")[0]
var imgBytes = extractImageBytes(imgElement);
console.log(imgBytes);
imgBytes"""
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
class ImageViewerSVGLoader(QObject):
	finished = pyqtSignal()
	bytesFetched = pyqtSignal(str)
	def __init__(self):
		super(ImageViewerSVGLoader, self).__init__()

	def load(self, url):
		try: data = requests.get(url).text
		except requests.exceptions.InvalidSchema as e:
			print("\x1b[31;1mui::system::imageviewer::ImageViewerSVGLoader.load:\x1b[0m", e)
		self.bytesFetched.emit(data)
		self.finished.emit()

# ribbon menu.
class ImageViewerMenu(DashRibbonMenu):
	def __init__(self, accent_color: str="green", 
				 parent: Union[None, QWidget]=None):
		super(ImageViewerMenu, self).__init__(
			parent=parent, group_names=[
				"File", "Edit", "View", "Zoom", "Flip and rotate", 
				"Resize and crop", "Filters", "Effects", "Play", 
				"Convert", "Compress", "Share", "Tags", "Rate", 
				"Notes", "Search", "More tools",
			], accent_color=accent_color,
		)
		self.addWidgetGroup("File", [
			([
                {
                    "icon": "widget/weather/save.svg",
                    "text": "Save As",
                    "tip": "Save image to a given path",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextUnderIcon,
                    "size": (30,30),
                },
                {
                    "text": "Save",
                    "tip": "Save changes to image",
                    "background": accent_color,
                }
			], {
               "alignment_flag": Qt.AlignCenter, 
               "orient": "vertical",
			}),
		])
		self.addWidgetGroup("Flip and rotate", [
			([
                {
                    "icon": "system/imageviewer/rotate_cc.png",
                    "text": "Rotate\nClockwise",
                    "tip": "Rotate image clockwise",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextUnderIcon,
                    "size": (43,43),
                },
                {
                    "icon": "system/imageviewer/rotate_ac.png",
                    "text": "Rotate Anti\nClockwise",
                    "tip": "Rotate image anti-clockwise",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextUnderIcon,
                    "size": (43,43),
                }
			], {
               "alignment_flag": Qt.AlignCenter, 
               "orient": "horizontal",
			})
		])
		self.addWidgetGroup("Resize and crop", [
			([
                {
					"text": "free",
                    "icon": "system/imageviewer/crop-free.svg",
                    "tip": "Free cropping mode",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                },
                {
					"text": "din",
                    "icon": "system/imageviewer/crop-din.svg",
                    "tip": "Crop din",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                }
			], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
			}),
			([
                {
					"text": "landscape",
                    "icon": "system/imageviewer/crop-landscape.svg",
                    "tip": "Landscape cropping mode",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                },
                {
					"text": "portrait",
                    "icon": "system/imageviewer/crop-portrait.svg",
                    "tip": "Portrait cropping mode",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                }
			], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
			}),
			([
                {
					"text": "original",
                    "icon": "system/imageviewer/crop-original.svg",
                    "tip": "Original crop",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                },
                {
					"text": "square",
                    "icon": "system/imageviewer/crop-square.svg",
                    "tip": "Square cropping mode",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                }
			], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
			}),
			([
                {
					"text": "3:2",
                    "icon": "system/imageviewer/crop-3-2.svg",
                    "tip": "3:2 aspect ratio crop",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                },
                {
					"text": "5:4",
                    "icon": "system/imageviewer/crop-portrait.svg",
                    "tip": "5:4 aspect ratio crop",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                }
			], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
			}),
			([
                {
					"text": "7:5",
                    "icon": "system/imageviewer/crop-7-5.svg",
                    "tip": "7:5 aspect ratio crop",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                },
                {
					"text": "16:9",
                    "icon": "system/imageviewer/crop-16-9.svg",
                    "tip": "16:9 aspect ratio crop",
                    "background": accent_color,
                    "style": Qt.ToolButtonTextBesideIcon,
                    "size": (30,30),
                }
			], {
               "alignment_flag": Qt.AlignLeft, 
               "orient": "vertical",
			})
		])
		self.hideGroup("Search")
		self.hideGroup("More tools")

# simplified menu for ImageViewer
class ImageViewerSimplifiedMenu(DashSimplifiedMenu):
	def __init__(self, accent_color: str="green", 
				 parent: Union[None, QWidget]=None):
		super(ImageViewerSimplifiedMenu, self).__init__(parent=parent, accent_color=accent_color)
		self.addWidget()

# file tree for image viewer.
class ImageViewerFileTree(QWidget):
    def __init__(self, root=os.path.expanduser("~"), parent=None):
        super(ImageViewerFileTree, self).__init__(parent)
        # veritcal layout.
        self.root = root  # root path.
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
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
        self.vboxlayout.addWidget(self.fileTree)

        self.setLayout(self.vboxlayout)
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
		self.vboxlayout = QVBoxLayout()
		self.vboxlayout.setContentsMargins(5, 5, 5, 5)
		# tree widget & details pane.
		self.tree = QTreeWidget()
		self.tree.setAnimated(True)
		self.tree.setFont(QFont("Be Vietnam Pro", 10))
		self.details_pane = self.initDetailsPane()
		self.splitter = QSplitter(Qt.Vertical)

		self.tree.setColumnCount(1)
		self.tree.setHeaderLabels(["element"])
		print(self.tree.verticalScrollBar().setStyleSheet(scrollbar_style))
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

		self.vboxlayout.addWidget(self.splitter)
		self.setLayout(self.vboxlayout)

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
	pass # effects: rotoscope, pixelate, vignette, red eye removal, distortion, sharpen, custom kernel application.

# sliders for applying filters.
class ImageViewerFilterSlider(QWidget):
	imageChanged = pyqtSignal() 
	def __init__(self, text: str, icon: str="", icon_size: Tuple[int,int]=(25,25),
				 minm: int=0, maxm: int=50, value: int=100, accent_color: str="yellow",
				 parent: Union[QWidget, None]=None, imageviewer=None, role: str="blur"):
		super(ImageViewerFilterSlider, self).__init__(parent)
		# connect to imageviewer and assume it has the browser or webview attribute pointing to the webview.
		self.imageviewer = imageviewer
		try: 
			self.webview = imageviewer.browser
		except AttributeError as e: 
			self.webview = imageviewer.webview
			print(e)
		self.apply_effect = True
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
		self.readout.returnPressed.connect(self.setEffect)
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

	def _js_effect_applicator(self, filterValue: str):
		"""apply backdrop-filter effect using js."""
		if filterValue == "":
			filterValue = "blur(0px) brightness(100%) contrast(100%) drop-shadow(0px 0px 0px black) hue-rotate(0deg) invert(0%) grayscale(0%) opacity(100%) sepia(0%) saturate(100%)"
		# the new updated value of filter property targeted by 'role'
		if self.role == "blur":
			newValue = f"blur({self.slider.value()}px)"
		elif self.role in ["opacity", "brightness", "contrast", "grayscale", "invert", "saturate", "sepia"]:
			newValue = f"{self.role}({self.slider.value()}%)"
		elif self.role == "hue-rotate":
			newValue = f"hue-rotate({self.slider.value()}deg)"
		
		regex = IMAGEVIEWER_BACKDROP_REGEX_MAP[self.role]
		filterValue = re.sub(regex, newValue, filterValue)
		
		jscode = f'document.getElementsByClassName("viewer-canvas")[0].getElementsByTagName("img")[0].style.filter = "{filterValue}";'
		self.webview.page().runJavaScript(jscode)

	def setFilterEffect(self, value: float):
		if isinstance(value, (int, float)):
			self.apply_effect = True
			self.updateEffect(value)

	def setFilterValue(self, value: float):
		if isinstance(value, (int, float)):
			self.apply_effect = False
			self.readout.setText(str(value))
			self.slider.setValue(value)
			self.apply_effect = True

	def setEffect(self):
		try: 
			value = float(self.readout.text())
			self.slider.setValue(value)
		except Exception as e:
			scopeStr = "\x1b[31;1mui::system::imageviewer::ImageViewerFilterSlider.setEffect:\x1b[0m"
			print(scopeStr, e)

	def updateEffect(self, value):
		self.readout.setText(str(value))
		if not self.apply_effect: 
			self.apply_effect = True
			return	
		if self.webview is not None:
			self.webview.page().runJavaScript(
				'document.getElementsByClassName("viewer-canvas")[0].getElementsByTagName("img")[0].style.filter', 
				self._js_effect_applicator
			)
		else:
			print("couldn't save because webview was none")
		# if auto save is on then save image after filter is applied.
		self.imageChanged.emit()

# image viewer panel containing filters.
class ImageViewerFiltersPanel(QWidget):
	imageChanged = pyqtSignal()
	def __init__(self, parent: Union[QWidget, None]=None,
				 imageviewer=None, accent_color: str="yellow"):
		super(ImageViewerFiltersPanel, self).__init__(parent)
		self.imageviewer = imageviewer
		self.vboxlayout = QVBoxLayout()
		self.vboxlayout.setContentsMargins(10, 10, 10, 10)
		self.vboxlayout.setSpacing(5)
		self.blurSlider = ImageViewerFilterSlider(
			"blur (in px)", icon="system/fileviewer/blur.svg",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="blur"
		)
		self.blurSlider.imageChanged.connect(self.imageChanged.emit)
		self.brightnessSlider = ImageViewerFilterSlider(
			"brightness (in %)", icon="system/fileviewer/brightness.svg",
			minm=0, maxm=150, value=100, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="brightness"
		)
		self.brightnessSlider.imageChanged.connect(self.imageChanged.emit)
		self.contrastSlider = ImageViewerFilterSlider(
			"contrast (in %)", icon="system/fileviewer/contrast.svg",
			minm=0, maxm=150, value=100, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="contrast"
		)
		self.contrastSlider.imageChanged.connect(self.imageChanged.emit)
		self.grayScaleSlider = ImageViewerFilterSlider(
			"gray scale (in %)", icon="system/fileviewer/grayscale.png",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="grayscale"
		)
		self.grayScaleSlider.imageChanged.connect(self.imageChanged.emit)
		self.invertSlider = ImageViewerFilterSlider(
			"invert (in %)", icon="system/fileviewer/invert.svg",
			minm=0, maxm=150, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="invert"
		)
		self.invertSlider.imageChanged.connect(self.imageChanged.emit)
		self.opacitySlider = ImageViewerFilterSlider(
			"opacity (in %)", icon="system/fileviewer/opacity.svg",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="opacity"
		)
		self.opacitySlider.imageChanged.connect(self.imageChanged.emit)
		self.saturationSlider = ImageViewerFilterSlider(
			"saturation (in %)", icon="system/fileviewer/saturation.png",
			minm=0, maxm=100, value=100, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="saturate"
		)
		self.saturationSlider.imageChanged.connect(self.imageChanged.emit)
		self.sepiaSlider = ImageViewerFilterSlider(
			"sepia (in %)", icon="system/fileviewer/sepia.png",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="sepia"
		)
		self.sepiaSlider.imageChanged.connect(self.imageChanged.emit)
		self.hueRotateSlider = ImageViewerFilterSlider(
			"hue rotation (in ° )", icon="system/fileviewer/hue.png",
			minm=0, maxm=180, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
			role="hue-rotate"
		)
		self.hueRotateSlider.imageChanged.connect(self.imageChanged.emit)
		self.vignetteSlider = ImageViewerFilterSlider(
			"vignette (in %)", icon="system/imageviewer/vignette.svg",
			minm=0, maxm=100, value=0, icon_size=(20,20),
			accent_color=accent_color, imageviewer=imageviewer,
		)
		self.vignetteSlider.imageChanged.connect(self.imageChanged.emit)
		self.resetBtn = QToolButton()
		self.resetBtn.setText("Reset Filters")
		self.resetBtn.setStyleSheet("""
		QToolButton {
			padding: 5px;
			font-size: 17px;
			margin-top: 20px;
			border-radius: 5px;
			background: #484848;
			border: 1px solid gray;
		}
		QToolButton:hover {
			color: #292929;
			background: """+accent_color+""";
		}""")
		self.filterNames = [
			"brightness", "contrast", "grayscale", 
			"invert", "opacity", "saturate", 
			"sepia", "hue-rotate", "blur",
		]
		self.sliderNames = {
			"blur": "blurSlider",
			"sepia": "sepiaSlider",
			"invert": "invertSlider",
			"opacity": "opacitySlider",
			"contrast": "contrastSlider",
			"saturate": "saturationSlider",
			"grayscale": "grayScaleSlider",
			"hue-rotate": "hueRotateSlider",
			"brightness": "brightnessSlider",
		}
		self.resetBtn.clicked.connect(self.reset)
		# self.dropShadowPicker = ImageViewerDropShadowPicker()
		self.vboxlayout.addWidget(self.blurSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.brightnessSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.contrastSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.grayScaleSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.invertSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.opacitySlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.saturationSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.sepiaSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.hueRotateSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.vignetteSlider, 0, Qt.AlignCenter | Qt.AlignTop)
		self.vboxlayout.addWidget(self.resetBtn, 0, Qt.AlignCenter | Qt.AlignTop)
		# self.vboxlayout.addWidget(
		# 	self.dropShadowPicker, 0, 
		# 	Qt.AlignCenter | Qt.AlignTop
		# )
		self.vboxlayout.addStretch(1)
		self.setLayout(self.vboxlayout)

	def setFilterValues(self, **values):
		if self.imageviewer is None: return
		currentState = {}
		for filterName in self.filterNames:
			sliderName = self.sliderNames[filterName]
			currentState[filterName] = values.get(filterName, getattr(self, sliderName).slider.value())
		# create the css backdropFilter string.
		backdropFilter: str = "" 
		for filterName, value in currentState.items():
			sliderName = self.sliderNames[filterName]
			filterSlider = getattr(self, sliderName)
			filterSlider.setFilterValue(value)
			if filterName == "blur":
				backdropFilter += f"blur({value}px)"
			elif filterName == "hue-rotate":
				backdropFilter += f" hue-rotate({value}deg)"
			elif filterName in ["opacity","brightness","contrast","grayscale","invert","saturate","sepia"]:
				backdropFilter += f" {filterName}({value}%)"
		print(backdropFilter)
		self._js_set_filter_values(backdropFilter=backdropFilter)

	def _js_set_filter_values(self, backdropFilter: str):
		"""apply backdrop-filter effect using js."""
		if self.imageviewer is None: return
		jscode = f'filterPane.style.backdropFilter = "{backdropFilter}";'
		print(backdropFilter)
		self.imageviewer.browser.page().runJavaScript(jscode)

	def reset(self):
		filterState = {
			"grayscale": 0, "invert": 0, "opacity": 100,
			"blur": 0, "brightness": 100, "contrast": 100,
			"saturation": 100, "sepia": 0, "hue-rotate": 0,
		}
		self.setFilterValues(**filterState)

# image viewer plain text edit.
class ImageViewerPlainTextEdit(QPlainTextEdit):
	def __init__(self, *args, accent_color: str="green", **kwargs):
		super(ImageViewerPlainTextEdit, self).__init__(*args, **kwargs)
		self.accent_color = accent_color
		self.setReadOnly(True)
		self.CtrlC = QShortcut(QKeySequence.Copy, self)

	def contextMenuEvent(self, event):
		self.contextMenu = self.createStandardContextMenu()
		for action in self.contextMenu.actions():
			if action.text().strip() == "&Copy":
				self.CtrlC.activated.connect(action.trigger)
				action.setShortcut("Ctrl+C")
		self.contextMenu = styleContextMenu(self.contextMenu, self.accent_color)
		self.contextMenu = styleTextEditMenuIcons(self.contextMenu)
		self.contextMenu.popup(event.globalPos())

# image viewer metadata panel.
class ImageViewerMetaDataPanel(QWidget):
	def __init__(self, accent_color: str="gray", 
				 parent: Union[None, QWidget]=None):
		super(ImageViewerMetaDataPanel, self).__init__(parent)
		self.accent_color = accent_color
		self.mimedb = QMimeDatabase()
		# panel layout.
		self.vboxlayout = QVBoxLayout()
		self.setLayout(self.vboxlayout)
		# init sub widgets.
		self.panel = self.initPanel()
		# build layout.
		self.vboxlayout.addWidget(self.panel)
		drop_shadow = self.createDropShadow(accent_color, "back")
		self.setGraphicsEffect(drop_shadow)

	def createDropShadow(self, accent_color: str, where: str):
		drop_shadow_color = extractFromAccentColor(accent_color, where=where)
		drop_shadow = QGraphicsDropShadowEffect()
		drop_shadow.setColor(QColor(drop_shadow_color))
		drop_shadow.setBlurRadius(10)
		drop_shadow.setOffset(0, 0)

		return drop_shadow

	def toggle(self):
		if self.isVisible():
			self.hide()
		else: self.show()

	def update(self, path: str):
		from fig_dash.utils import h_format_mem, extractSliderColor, exif_color_space, has_transparency

		self.path = path
		fontColor = extractSliderColor(self.accent_color)
		self.info = QFileInfo(path)
		mimetype = self.mimedb.mimeTypeForFile(self.path).name()
		# # stat info.
		# statInfo = os.stat(path)
		try:
			birthTime = self.info.birthTime().toPyDateTime()
			birthTime = birthTime.strftime("%b %d, %Y %H:%M %p")
		except ValueError as e: 
			birthTime = f"Creation time not available for {platform.system()}"
		lastRead = self.info.lastRead().toPyDateTime().strftime("%b %d, %Y %H:%M %p")
		lastModified = self.info.lastModified().toPyDateTime().strftime("%b %d, %Y %H:%M %p")
		metadataChangeTime = self.info.metadataChangeTime().toPyDateTime().strftime("%b %d, %Y %H:%M %p")
		# create PIL object to get image specific metadata.
		colorspace = ""
		colorprofile = ""
		ICC_INFO = ""
		MISC_INFO = ""
		MEDIA_INFO = ""
		COLOR_SPACE = ""
		HEADER_INFO = ""
		INTENT_INFO = ""
		PROFILE_INFO = ""
		MISC_FILE_INFO = f"""
		<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Misc. File Info</span>
		<div style="color: #fff;">
			<b>Owner:</b> {self.info.owner()} <br>
			<b>Group:</b> {self.info.group()} <br>
			<b>Read only:</b> {(not(self.info.isWritable()) and self.info.isReadable())} <br>
			<b>Extension:</b> {self.info.completeSuffix()} <br>
			<b>Hidden file:</b> {self.info.isHidden()} <br>
			<b>Symbolic link:</b> {self.info.isSymbolicLink() or self.info.isSymLink()} <br>
		</div><br>"""
		# user and group permissions for file.
		UserPermissions = "["
		if self.info.permission(QFile.ReadUser):
			UserPermissions += "R"
		if self.info.permission(QFile.WriteUser):
			UserPermissions += "W"
		# if self.info.permission(QFile.ExecuteUser):
			# UserPermissions += "X"
		UserPermissions += "]"
		GroupPermissions = "["
		if self.info.permission(QFile.ReadUser):
			GroupPermissions += "R"
		if self.info.permission(QFile.WriteUser):
			GroupPermissions += "W"
		# if self.info.permission(QFile.ExecuteUser):
			# GroupPermissions += "X"
		GroupPermissions += "]"
		PERMISSIONS_INFO = f"""
		<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Permissions</span>
		<div style="color: #fff;">
			<b>{self.info.owner()}:</b> {UserPermissions} <br>
			<b>{self.info.group()} (grp):</b> {GroupPermissions} <br>
			<b>Everyone:</b> {'Unknown'} <br>
		</div><br>"""
		try:
			PILObj = Image.open(path)
			width = PILObj.size[0]
			height = PILObj.size[1]
			# icc
			icc = PILObj.info.get("icc_profile", "")
			if icc != "":
				prf = ImageCms.ImageCmsProfile(io.BytesIO(icc))
				print("Product Name:", prf.product_name)
				print("Product Info:", prf.product_info)
				print("Profile Attributes:", prf.profile.attributes)
				
				p = prf.profile
				colorspace = f"{p.xcolor_space}"
				colorprofile = p.profile_description
				if p.icc_measurement_condition is None: 
					icc_measurement_condition = {}
				else: 
					icc_measurement_condition = p.icc_measurement_condition
				try:
					creation_date = p.creation_date
				except ValueError:
					creation_date = "Date not available"
				if p.clut is None: p.clut = {}
				measurement_condition = "<br>"+"<br>".join([f"{k}: {v}" for k,v in icc_measurement_condition.items()])
				clut = "<br>"+"<br>".join([f"{k}: {', '.join([str(i) for i in v])}" for k,v in p.clut.items()])

				MISC_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Misc. Metadata</span>
				<div style="color: #fff;">
					<b>Clut:</b> {clut} <br>
					<b>Model:</b> {p.model} <br>
					<b>Target:</b> {p.target} <br>
					<b>Device Class:</b> {p.device_class} <br>
					<b>Connection Space:</b> {p.connection_space} <br>
					<b>Is Matrix Shaper?:</b> {p.is_matrix_shaper} <br>
					<b>Viewing Condition:</b> {p.viewing_condition} <br>
					<b>Screening Description:</b> {p.screening_description} <br>
				</div><br>"""
				ICC_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">ICC</span>
				<div style="color: #fff;">
					<b>Version:</b> {p.icc_version} <br>
					<b>Measurement Condition:</b> {measurement_condition} <br>
					<b>Viewing Condition:</b> {p.icc_viewing_condition} <br>
				</div><br>"""
				PROFILE_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Profile</span>
				<div style="color: #fff;">
					<!-- <b>Id:</b> {p.profile_id} <br> -->
					<b>Description:</b> {p.profile_description} <br>
					<b>Version:</b> {p.version} <br>
					<b>Creation Date:</b> {creation_date} <br>
					<b>Copyright:</b> {p.copyright} <br>
					<b>Manufacturer:</b> {p.manufacturer} <br>
					<b>Technology:</b> {p.technology} <br>
				</div><br>"""
				COLOR_SPACE = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Color Space</span>
				<div style="color: #fff;">
					<b>Red Primary:</b> ({", ".join([f"{c:.2f}" for c in p.red_primary[0]])}) ({", ".join([f"{c:.2f}" for c in p.red_primary[1]])}) <br>
					<b>Blue Primary:</b> ({", ".join([f"{c:.2f}" for c in p.blue_primary[0]])}) ({", ".join([f"{c:.2f}" for c in p.blue_primary[1]])}) <br>
					<b>Green Primary:</b> ({", ".join([f"{c:.2f}" for c in p.green_primary[0]])}) ({", ".join([f"{c:.2f}" for c in p.green_primary[1]])}) <br>
					<b>Red Colorant:</b> ({", ".join([f"{c:.2f}" for c in p.red_colorant[0]])}) ({", ".join([f"{c:.2f}" for c in p.red_colorant[1]])}) <br>
					<b>Blue Colorant:</b> ({", ".join([f"{c:.2f}" for c in p.blue_colorant[0]])}) ({", ".join([f"{c:.2f}" for c in p.blue_colorant[1]])}) <br>
					<b>Green Colorant:</b> ({", ".join([f"{c:.2f}" for c in p.green_colorant[0]])}) ({", ".join([f"{c:.2f}" for c in p.green_colorant[1]])}) <br>
				</div><br>"""
				if p.intent_supported is None: p.intent_supported = {}
				supported = "<br>"+"<br>".join([f"{k}: {', '.join([str(i) for i in v])}" for k,v in p.intent_supported.items()])
				INTENT_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Intent Information</span>
				<div style="color: #fff;">
					<b>Rendering:</b> {p.rendering_intent} <br>
					<b>Is supported?:</b> {p.colorimetric_intent} <br>
					<b>Supported:</b> {supported} <br>
					<b>Perceptual Rendering Gamut:</b> {p.perceptual_rendering_intent_gamut} <br>
					<b>Saturation Rendering Gamut:</b> {p.saturation_rendering_intent_gamut} <br>
				</div><br>"""
				MEDIA_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Media Information</span>
				<div style="color: #fff;">
					<b>Black Point:</b> ({", ".join([f"{c:.2f}" for c in p.media_black_point[0]])}) ({", ".join([f"{c:.2f}" for c in p.media_black_point[1]])}) <br>
					<b>White Point:</b> ({", ".join([f"{c:.2f}" for c in p.media_white_point[0]])}) ({", ".join([f"{c:.2f}" for c in p.media_white_point[1]])}) <br>
					<b>White Point Temperature:</b> {p.media_white_point_temperature:.2f} <br>
				</div><br>"""
				HEADER_INFO = f"""
				<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Header Information</span>
				<div style="color: #fff;">
					<b>Manufacturer:</b> {p.header_manufacturer} <br>
					<b>Model:</b> {p.header_model} <br>
					<b>Flags:</b> {p.header_flags} <br>
				</div><br>"""
				# print(dir(prf.profile))
			# colorspace = exif_color_space(PILObj)
			hasAlpha = "Yes" if has_transparency(PILObj) else "No"

		except PIL.UnidentifiedImageError as e:
			width = "scalable"
			height = "scalable"
			hasAlpha = "Not meaningful for svg"
			print(e)
		except IsADirectoryError as e:
			width = "-"
			height = "-"
			hasAlpha = "-"
			print(e)
		fileSize = self.info.size()
		self.panel.setPlainText("")
		# update file information.
		self.panel.appendHtml(f"""
		<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">File Information</span>
		<div style="color: #fff;">
			<b>Kind:</b> {mimetype} <br>
			<b>Size:</b> {h_format_mem(fileSize)} ({fileSize:,} bytes) <br>
			<b>Disk:</b> {h_format_mem(fileSize)} on disk <br>
			<b>Where:</b> {self.path} <br>
			<b>Created:</b> {birthTime} <br>
			<b>Modified:</b> {lastModified} <br>
			<b>Last opened:</b> {lastRead} <br>
			<b>Metadata changed:</b> {metadataChangeTime} <br>
		</div>
		<br>
		<span style="font-weight: bold; font-size: 22px; color: {fontColor}; font-family: 'Be Vietnam Pro' ">Image Information</span>
		<div style="color: #fff;">
			<b>Dimensions:</b> {width} x {height} <br>
			<b>Color space:</b> {colorspace} <br>
			<b>Color profile:</b> {colorprofile} <br>
			<b>Alpha channel:</b> {hasAlpha} <br>
		</div> <br>
		{MISC_FILE_INFO}
		{PERMISSIONS_INFO}
		{PROFILE_INFO}
		{COLOR_SPACE}
		{MEDIA_INFO}
		{INTENT_INFO}
		{HEADER_INFO}
		{ICC_INFO}
		{MISC_INFO}""")

	def initPanel(self) -> QWidget:
		return ImageViewerPlainTextEdit(accent_color=self.accent_color)

# image viewer side panel with various tabs containing: 
class ImageViewerSidePanel(QTabWidget):
	def __init__(self, parent: Union[None, QWidget]=None, imageviewer=None, 
				 accent_color: str="yellow", where: str="back"):
		super(ImageViewerSidePanel, self).__init__(parent=parent)
		# panels.
		self.filters_panel = ImageViewerFiltersPanel(
			accent_color=accent_color, 
			imageviewer=imageviewer,
		)
		self.effects_panel = ImageViewerEffectsPanel()
		self.filetree = ImageViewerFileTree()
		self.svgtree = ImageViewerSVGTree()
		# self.layers = ImageViewerLayers()
		self.addTab(self.filetree, "Folders")
		self.addTab(self.svgtree, "Elements")
		# self.addTab(self.layers, "Layers")
		self.addTab(self.filters_panel, "Filters")
		self.addTab(self.effects_panel, "Effects")
		self.setStyleSheet("""color: #fff; background: #292929;""")
		self.setFont(QFont("Be Vietnam Pro", 10))
		# drop shadow effect.
		drop_shadow = self.createDropShadow(accent_color, where)
		self.setGraphicsEffect(drop_shadow)

	def createDropShadow(self, accent_color: str, where: str):
		drop_shadow_color = extractFromAccentColor(accent_color, where=where)
		drop_shadow = QGraphicsDropShadowEffect()
		drop_shadow.setColor(QColor(drop_shadow_color))
		drop_shadow.setBlurRadius(10)
		drop_shadow.setOffset(0, 0)

		return drop_shadow

	def loadSVGData(self, svg_data: str=""):
		self.svgtree.loadSVGData(svg_data)

	def toggle(self):
		if self.isVisible():
			self.hide()
		else: self.show()

# web browser for image viewer
class ImageViewerBrowser(DebugWebBrowser):
    def __init__(self, *args, imageviewer=None, **kwargs):
        super(ImageViewerBrowser, self).__init__(*args, **kwargs)
        self.imageviewer = imageviewer
        self.accent_color = "yellow" 
        self.shortcut_mapper = {}
        self.widget = None

    def connectWidget(self, widget: QWidget):
        self.widget = widget

    def setAccentColor(self, accent_color):
        self.accent_color = accent_color
    # def inspectTriggered(self):
    #     print(f"triggered inspect dev_view.isVisible() = {self.dev_view.isVisible()}")
    #     if not self.dev_view.isVisible():
    #         self.dev_view.show()
    #     self.inspect_action.trigger()
    #     print(f"triggered inspect dev_view.isVisible() = {self.dev_view.isVisible()}")
    def activateShortcut(self, action: QAction):
        for keySeq in action.shortcuts():
            if keySeq.toString() in self.shortcut_mapper: continue
            self.shortcut_mapper[keySeq.toString()] = QShortcut(keySeq, self)
            self.shortcut_mapper[keySeq.toString()].activated.connect(action.trigger)
        # printMapper(self.shortcut_mapper)
    def createContextMenu(self) -> QMenu:
        self.contextMenuActions = []
        menu = self.page().createStandardContextMenu()
        menu.setObjectName("ImageViewerContextMenu")
        menu = styleContextMenu(menu, accent_color=self.accent_color)
        copyMenu = None
        copyImageAddress = None
        for action in menu.actions():
            if action.text() == "Back":
                action.setShortcut(QKeySequence.Back)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("lineedit/prev.svg"))
                else:
                    action.setIcon(FigD.Icon("lineedit/prev_disabled.svg"))
            elif action.text() == "Forward":
                action.setShortcut(QKeySequence.Forward)
                if action.isEnabled():
                    action.setIcon(FigD.Icon("lineedit/next.svg"))
                else:
                    action.setIcon(FigD.Icon("lineedit/next_disabled.svg"))
            elif action.text() == "Reload":
                action.setShortcut(QKeySequence.Refresh)
                action.setIcon(FigD.Icon("lineedit/reload.svg"))
            elif action.text() == "Save page":
                action.setIcon(FigD.Icon("system/imageviewer/save_page.svg"))
                action.setShortcut(QKeySequence("Ctrl+Shift+S"))
                # action_texts = [a.text() for a in menu.actions()]
                # if "Save image" not in action_texts:
                #     print("adding save image")
                #     saveAction = QAction()
                #     saveAction.setText("Save image")
                #     saveAction.setIcon(FigD.Icon("system/imageviewer/save_image.svg"))
                #     saveAction.setShortcut(QKeySequence.Save)
                #     saveAction.triggered.connect(self.imageviewer.saveImage)
                #     menu.insertAction(action, saveAction)
            elif action.text() == "Save image":
                action.setShortcut(QKeySequence.Save)
                action.setIcon(FigD.Icon("system/imageviewer/save_image.svg"))
                action.triggered.connect(self.imageviewer.saveImage)
            elif action.text() == "View page source":
                action.setShortcut(QKeySequence("Ctrl+U"))
                action.setIcon(FigD.Icon("titlebar/source.svg"))
            elif action.text() == "Copy image":
                action.setVisible(False)
                copyMenu = menu.addMenu(FigD.Icon("browser/copy.svg"), "Copy")
                copyMenu = styleContextMenu(copyMenu, self.accent_color)
                # action.setShortcut(QKeySequence.Copy)
                # action.setIcon(FigD.Icon("browser/copy.svg"))
                # action.triggered.connect(self.imageviewer.copyImageToClipboard)
            elif action.text() == "Copy image address":
                copyImageAddress = action
                copyImageAddress.setVisible(False)
                # action.setShortcut(QKeySequence("Ctrl+Shift+C"))
                # action.setIcon(FigD.Icon("system/imageviewer/copy_image_address.svg"))
            # elif action.text() == "Inspect":
            #     self.inspect_action = action
            #     action.setVisible(False) # hide original aspect action.
            #     wrappedInspectAction = menu.addAction("Inspect")
            #     wrappedInspectAction.setShortcut(QKeySequence("Ctrl+Shift+I"))
            #     if wrappedInspectAction.isEnabled():
            #         wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
            #     else:
            #         wrappedInspectAction.setIcon(FigD.Icon("titlebar/dev_tools.svg"))
            #     wrappedInspectAction.triggered.connect(
            #         self.inspectTriggered
            #     ) 
            self.activateShortcut(action)
        if copyMenu:
            copyMenu.addAction(
				FigD.Icon("system/imageviewer/copy_image.svg"), "Copy image",
				self.imageviewer.copyImageToClipboard, QKeySequence.Copy,
		    )
            copyMenu.addAction(
				FigD.Icon("system/imageviewer/copy_image_address.svg"), "Copy address",
				copyImageAddress.trigger, QKeySequence("Ctrl+Shift+C"),
		    )
            copyMenu.addAction(
				FigD.Icon("browser/copy.svg"), "Copy base64",
				copyImageAddress.trigger,
		    )
            copyMenu.addAction(
				FigD.Icon("system/imageviewer/copy_bytes.png"), 
				"Copy bytes", copyImageAddress.trigger,
		    )
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
        # menu.addAction(
		# 	FigD.Icon("system/imageviewer/rotate_cc.svg"), "Rotate 90° clockwise", 
		# 	lambda: self.page().runJavaScript(rotateCCJS)
		# )
        # menu.addAction(
		# 	FigD.Icon("system/imageviewer/rotate_ac.svg"), "Rotate 90° anti-clockwise", 
		# 	lambda: self.page().runJavaScript(rotateACJS)
		# )
        zoomMenu = menu.addMenu(FigD.Icon("titlebar/zoom_in.svg"), "Zoom")
        zoomMenu = styleContextMenu(zoomMenu, accent_color=self.accent_color)
        zoomMenu.addAction(
			FigD.Icon("titlebar/zoom_in.svg"), "Zoom in", 
			lambda: self.page().runJavaScript(zoomInJS),
			QKeySequence.ZoomIn,
		)
        zoomMenu.addAction(
			FigD.Icon("titlebar/zoom_out.svg"), "Zoom out", 
			lambda: self.page().runJavaScript(zoomOutJS),
			QKeySequence.ZoomOut,
		)
        zoomMenu.addAction("Original size", lambda: self.page().runJavaScript(origSizeJS))
        rotateMenu = menu.addMenu(FigD.Icon("system/imageviewer/rotate_cc.svg"), "Rotate")
        rotateMenu = styleContextMenu(rotateMenu, accent_color=self.accent_color)
        rotateMenu.addAction(
			FigD.Icon("system/imageviewer/rotate_cc.svg"), "90° clockwise", 
			lambda: self.page().runJavaScript(rotateCCJS)
		)
        rotateMenu.addAction(
			FigD.Icon("system/imageviewer/rotate_cc.svg"), "180° clockwise", 
			lambda: self.page().runJavaScript(rotateCCJS+"\n"+rotateCCJS)
		)
        rotateMenu.addAction(
			FigD.Icon("system/imageviewer/rotate_ac.svg"), "90° anti-clockwise", 
			lambda: self.page().runJavaScript(rotateACJS)
		)
        rotateMenu.addAction(
			FigD.Icon("system/imageviewer/rotate_ac.svg"), "180° anti-clockwise", 
			lambda: self.page().runJavaScript(rotateACJS+"\n"+rotateACJS)
		)
        flipMenu = menu.addMenu(FigD.Icon("system/imageviewer/flip_horizontal.svg"), "Flip")
        flipMenu = styleContextMenu(flipMenu, accent_color=self.accent_color)
        flipMenu.addAction(
			FigD.Icon("system/imageviewer/flip_horizontal.svg"), 
			"Horizontal", lambda: self.page().runJavaScript(flipHJS))
        flipMenu.addAction(
			FigD.Icon("system/imageviewer/flip_vertical.svg"), 
			"Vertical", lambda: self.page().runJavaScript(flipVJS)
		)
        if self.widget:
            # show javascript based toolbar.
            showJSToolBar = menu.addAction(
			    "Show more tools", 
			    partial(
					self.widget.setJSToolBarVisible,
					not(self.widget.isJSToolBarVisible()),
				),
		    ) 
            showJSToolBar.setCheckable(True)
            showJSToolBar.setChecked(self.widget.isJSToolBarVisible())
            # show navigation pane.
            showNavPane = menu.addAction(
			    "Show navigation pane", 
			    partial(
					self.widget.setNavBarVisible,
					not(self.widget.isNavBarVisible()),
				),
		    ) 
            showNavPane.setCheckable(True)
            showNavPane.setChecked(self.widget.isNavBarVisible())
            menu.addAction(
				FigD.Icon("lineedit/search_image.svg"),
				"Search Google with this image",
				self.widget.searchWithGoogle,
			)

        return menu

    def contextMenuEvent(self, event):
        self.menu = self.createContextMenu()
        data = self.page().contextMenuData()
        self.menu.popup(event.globalPos())

# image viewer webview.
class ImageViewerWebView(DebugWebView):
    def __init__(self, *args, imageviewer=None, 
				 accent_color: str="yellow", **kwargs):
        browser = ImageViewerBrowser(
			accent_color=accent_color, 
			imageviewer=imageviewer
		)
        super(ImageViewerWebView, self).__init__(
            *args, browser=browser, 
            **kwargs
        )

    def __str__(self):
        return "\x1b[34mui::system::imageviewer::ImageViewerWebView\x1b[0m"

# image viewer widget.
class ImageViewerWidget(FigDMainWidget):
    changeTabIcon = pyqtSignal(str)
    changeTabTitle = pyqtSignal(str)
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
        self.path_ptr = None
        self.save_ptr = None
        self.__auto_save = False
        self._image_search_mode = False
        self._is_js_navbar_visible = args.get("show_navbar", False)
        self._is_js_toolbar_visible = args.get("add_js_toolbar", False)
		# arguments.
        print(args.keys())
        self.svg_data = None
        self.css_grad = args.get("css_grad", "gray")
        accent_color = args.get("accent_color", "yellow")
        # connect a mimedatabase.
        self.mime_database = QMimeDatabase()
        self.file_watcher = QFileSystemWatcher()
		# shortcuts.
        self.CtrlS = FigDShortcut(QKeySequence.Save, self, "Save image")
        self.CtrlS.activated.connect(self.saveImage)
        self.CtrlShiftK = FigDShortcut(QKeySequence("Ctrl+Shift+K"), self, "Toggle metadata panel visibility.")
        self.ShiftF = FigDShortcut(QKeySequence("Shift+F"), self, "Toggle navbar visibility")
        # create layout
        layout = QVBoxLayout()
        # TODO: Check if margin is needed anymore at all.
        margin = 0
        layout.setContentsMargins(margin, 0, margin, margin)
        layout.setSpacing(0)
        self.centralLayout = layout
		# image search worker.
        from fig_dash.api.browser.imagesearch import GoogleImageSearchBackend
        self.imageSearchWorker = GoogleImageSearchBackend()
        self.imageSearchWorker.urlFetched.connect(self.openWebPage)
        # build layout.
        self.debug_webview = ImageViewerWebView(imageviewer=self)
        self.browser = self.debug_webview.browser
        self.browser.connectWidget(self)
        self.browser.CtrlC = FigDShortcut(QKeySequence.Copy, self.browser, "Copy image to clipboard")
        self.browser.CtrlC.activated.connect(self.copyImageToClipboard)
        self.file_watcher.fileChanged.connect(self.browser.reload)
        self.side_panel = ImageViewerSidePanel(
			accent_color=accent_color,
			imageviewer=self,
		)
        self.navbar = FigDNavBar(
			search_prompt="Search for images locally or on the web",
			navbtns=["back", "forward", "reload"], 
			accent_color=accent_color, 
		)
        self.navbar.connectBrowser(self.browser)
        self.navbar.hide()
        self.ShiftF.activated.connect(self.navbar.toggle)
        self.searchbar = self.navbar.searchbar
        self.searchbar.returnPressed.connect(self.searchImage)
        self.searchbar.connect("imageSearch", self.toggleImageSearchMode)
        self.side_panel.filters_panel.imageChanged.connect(self._decide_on_save)
		
        self.metadata_panel = ImageViewerMetaDataPanel(accent_color=accent_color)
        self.metadata_panel.hide()
        self.CtrlShiftK.activated.connect(self.metadata_panel.toggle)
        self.svgtree = self.side_panel.svgtree
        self.filetree = self.side_panel.filetree
        self.filetree.connectImageViewer(self)
        self.side_panel.hide()
        # self.filetree.hide()
        self.debug_webview.insertWidget(0, self.side_panel)
        self.debug_webview.addWidget(self.metadata_panel)
        layout.addWidget(self.navbar)
        layout.addWidget(self.debug_webview)
        # set layout.
        self.setLayout(layout)
        # parameters stuff.
        self.zoom_factor = args.get("zoom_factor", 1.3)
        # set icon.
        self._fullscreen = False

    def setImageSearchMode(self, value: bool):
        self._image_search_mode = value

    def isImageSearchMode(self) -> bool:
        return self._image_search_mode

    def setJSToolBarVisible(self, value: bool):
        self._is_js_toolbar_visible = value
        if value: self.showJSToolBar()
        else: self.hideJSToolBar()
	
    def setNavBarVisible(self, value: bool):
        self._is_js_navbar_visible = value
        if value: self.showNavBar()
        else: self.hideNavBar()

    def toggleJSToolBar(self):
        if self.isJSToolBarVisible():
            self.setJSToolBarVisible(False)
        else: 
            self.setJSToolBarVisible(True)

    def toggleNavBar(self):
        if self.isNavBarVisible():
            self.setNavBarVisible(False)
        else: 
            self.setNavBarVisible(True)

    def toggleImageSearchMode(self):
        if self.isImageSearchMode():
            self.setImageSearchMode(False)
        else: 
            self.setImageSearchMode(True)

    def showJSToolBar(self):
        self.browser.page().runJavaScript(
			"document.getElementsByClassName('viewer-toolbar')[0].style.display=''"
		)

    def hideJSToolBar(self):
        self.browser.page().runJavaScript(
			"document.getElementsByClassName('viewer-toolbar')[0].style.display='none'"
		)

    def showNavBar(self):
        self.browser.page().runJavaScript(
			"document.getElementsByClassName('viewer-navbar')[0].style.display=''"
		)

    def hideNavBar(self):
        self.browser.page().runJavaScript(
			"document.getElementsByClassName('viewer-navbar')[0].style.display='none'"
		)

    def changeZoom(self, zoomValue: float):
        self.browser.setZoomFactor(zoomValue/100)

    def _decide_on_save(self):
        # print(f"triggered auto save: {self.autoSave()}")
        if self.autoSave():
            print("saving changes")
            self.saveImage() 

    def _save_image_callback(self, base64_str: Union[str, None]):
        if base64_str is not None and self.save_ptr:
            base64_str = base64_str.split("data:image/png;base64,")[-1]
            base64_bytes = base64_str.encode("ascii")
            img_bytes = base64.b64decode(base64_bytes)
            with open(self.save_ptr, "wb") as fp:
                fp.write(img_bytes)
        elif base64_str is None:
            print("\x1b[34;1mCouldn't save image: base64_str=None\x1b[0m")

    def searchImage(self):
        query_or_url = self.searchbar.text()
		# if the input is a file path.
        if os.path.exists(query_or_url):
            if self.isImageSearchMode():
                self.imageSearchWorker.start(path=query_or_url)
            else:
                self.open(query_or_url)
            return
		# if the input is an URL.
        url = QUrl.fromUserInput(query_or_url)
        from fig_dash.api.browser.url.validate import isValidTLD
        if url.toString() != "" and isValidTLD(url):
            self.searchbar.append(url)
            self.openUrl(url)
            print(f"url: {url}")
        else: # search on google images
            if query_or_url.startswith("data:image/"): 
                import base64
                import tempfile
                ext = query_or_url.split(";")[0].split("data:image/")[-1]
                content = base64.decodebytes(query_or_url.split(",")[-1].encode("ascii"))
                #with tempfile.NamedTemporaryFile(suffix="."+suffix) as f:
                #     f.write(content)
                self.open(FigD.createTempPath(content, mode="wb", ext=ext))
            else:
                import urllib.parse
                url = QUrl(f"https://www.google.com/search?q={urllib.parse.quote_plus(query_or_url)}&tbm=isch&sclient=img")
                self.openWebPage(url)

    def searchWithGoogle(self):
        """search currently opened file/URL with google image search."""
        if self.path_ptr: self.imageSearchWorker.start(path=self.path_ptr)
        else: self.imageSearchWorker.start(url=self.browser.url().toString())

    def saveImage(self):
        if self.save_ptr is None:
            name = Path(self.path_ptr).name
            filename, _ = QFileDialog.getSaveFileName(
			    self, "Save image file to ...", 
			    name, "Image Files (*.png)"
		    )
            self.save_ptr = filename
        else: filename = self.save_ptr
        print(filename)
        if filename is not None:
            self.browser.page().runJavaScript(
				IMAGEVIEWER_BYTES_EXTRACT_JS, 
				self._save_image_callback
			)

    def _copy_image_callback(self, base64_str: str):
        if base64_str is None: 
            print("base64_str:", base64_str)
            return
        base64_str = base64_str.split("data:image/png;base64,")[-1]
        base64_bytes = base64_str.encode("ascii")
        img_bytes = base64.b64decode(base64_bytes)
        self.__copied_pixmap = QPixmap()
        self.__copied_pixmap.loadFromData(img_bytes)
        QApplication.clipboard().setPixmap(self.__copied_pixmap)

    def copyImageToClipboard(self):
        """copy displayed image to clipboard"""
        print("copying image")
        self.browser.page().runJavaScript(IMAGEVIEWER_BYTES_EXTRACT_JS, self._copy_image_callback)
        # if self.path_ptr:
        #     self.__copied_pixmap = QPixmap(self.path_ptr)
        #     QApplication.clipboard().setPixmap(self.__copied_pixmap)
    def loadSVGData(self, svg_data: str=""):
        self.svgtree.loadSVGData(svg_data)

    def viewSource(self):
        import jinja2
        # print("showing source")
        # print(self.svg_data)
        textarea = QPlainTextEdit()
        textarea.setStyleSheet("background: #292929; color: #fff; font-family: 'Be Vietnam Pro'")
		# code to set tab distance.
        textarea.setTabStopWidth(
			QFontMetricsF(
				textarea.font()
			).horizontalAdvance(' ')*4
		)
        textarea.setTabStopDistance(
			QFontMetricsF(
				textarea.font()
			).horizontalAdvance(' ') * 4
		)
        if self.svg_data and self.path_ptr: 
            content = open(self.path_ptr).read()
            textarea.setPlainText(content)
        else:
            textarea.setPlainText("Not an SVG (no source available)")
        window = wrapFigDWindow(textarea)
        window.show()

    def initCentralWidget(self):
        centralWidget = QWidget()
        # init layout.
        layout = QVBoxLayout()
        margin = 10
        layout.setContentsMargins(margin, 0, margin, margin)
        layout.setSpacing(0)
        self.centralLayout = layout
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
        self.debug_webview.insertWidget(0, self.side_panel)
        layout.addWidget(self.debug_webview)
        # set layout.
        centralWidget.setLayout(layout)
        # self.browser.page().runJavaScript("viewer.full();")
    def toggleAutoSave(self, state: int):
        """toggle auto save state of the image viewer"""
        if state == 2: 
            # print("ImageViewerWidget.setAutoSave(True)")
            self.setAutoSave(True)
        elif state == 0: 
            # print("ImageViewerWidget.setAutoSave(False)")
            self.setAutoSave(False)

    def setAutoSave(self, autoSave: bool):
        self.__auto_save = autoSave

    def autoSave(self):
        return self.__auto_save

    def connectMenu(self, menu: ImageViewerMenu):
        self.menu = menu
        self.menu.hide()

    def launchSVGLoadWorker(self, url: str):
        # thread and worker.
        self.__svg_load_thread = QThread()
        self.__svg_load_worker = ImageViewerSVGLoader()
        # move worker to thread.
        self.__svg_load_worker.moveToThread(self.__svg_load_thread)
		# thread slots.
        self.__svg_load_thread.started.connect(partial(self.__svg_load_worker.load, url))
        self.__svg_load_thread.finished.connect(self.__svg_load_thread.deleteLater)
		# worker slots.
        self.__svg_load_worker.bytesFetched.connect(self.svgDataRecieved)
        self.__svg_load_worker.finished.connect(self.__svg_load_thread.quit)
        self.__svg_load_worker.finished.connect(self.__svg_load_worker.deleteLater)
        # start thread.
        self.__svg_load_thread.start()

    def svgDataRecieved(self, svgBytes: bytes):
        print(svgBytes)
        self.svg_data = svgBytes
        self.svg_data = self.loadSVGData(svg_data=self.svg_data)

    def isJSToolBarVisible(self):
        return self._is_js_toolbar_visible

    def isNavBarVisible(self):
        return self._is_js_navbar_visible

    def openWebPage(self, url: Union[QUrl, str]):
        if isinstance(url, QUrl):
            url = url.toString()
        self.searchbar.append(url)
        self.changeTabTitle.emit(url)
        self.changeTabIcon.emit(FigD.icon("system/fileviewer/browser.svg"))
        self.svg_data = None
        self.path_ptr = None
		# load SVG data.
        self.svgtree.tree.clear()
        self.svgtree.details_pane.setText("click on an element in the SVG tree to view details")
        self.browser.load(QUrl(url))

    def openUrl(self, url: Union[QUrl, str]):
        from fig_dash.ui.js.imageviewer import ViewerJSPluginCSS, ViewerJSPluginJS, ImageViewerHTML
        if isinstance(url, QUrl):
            url = url.toString()
        self.searchbar.append(url)
        self.changeTabTitle.emit(url)
        self.changeTabIcon.emit(FigD.icon("system/fileviewer/browser.svg"))
        self.svg_data = None
        self.path_ptr = None
        if url.endswith(".svg"):
            FigD.debug("launched SVG data loading worker")
            self.launchSVGLoadWorker(
			    QUrl(url).toString(QUrl.FullyEncoded)
		    )
		# load SVG data.
        self.svgtree.tree.clear()
        self.svgtree.details_pane.setText("click on an element in the SVG tree to view details")
        html = ImageViewerHTML.render({
            "FILEPATH": url,
            "FILEPATH_URL": url,
            "FILENAME_WITHOUT_EXT": url,
            "VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS.render(
				SHOW_JS_TOOLBAR='' if self.isJSToolBarVisible() else 'style="display: none;"',
				SHOW_NAVBAR='' if self.isNavBarVisible() else 'style="display: none;"',
			),
            "VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
            "PATH_IS_FOLDER": False,
            "GALLERY_INFO": [],
			"CSS_GRAD": self.css_grad,
        })
        render_url = FigD.createTempUrl(html)
        self.browser.load(render_url)        

    def open(self, path: str):
        from fig_dash.ui.js.imageviewer import ViewerJSPluginCSS, ViewerJSPluginJS, ImageViewerHTML
        self.svg_data = None
        self.searchbar.append(path)
        if path != os.path.expanduser(path):
            self.searchbar.append(os.path.expanduser(path))
        path = os.path.expanduser(path)
        self.file_watcher.addPath(path)
        self.metadata_panel.update(path)
        self.path_ptr = path
        filename_without_ext = str(Path(path).stem)
        self.searchbar.append(filename_without_ext)
        self.changeTabTitle.emit(filename_without_ext)
        self.changeTabIcon.emit(path)
        isdir = os.path.isdir(path)
		# load SVG data.
        self.svgtree.tree.clear()
        self.svgtree.details_pane.setText("click on an element in the SVG tree to view details")
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
        html = ImageViewerHTML.render({
            "FILEPATH": path,
            "FILEPATH_URL": url,
            "FILENAME_WITHOUT_EXT": filename_without_ext,
            "VIEWER_JS_PLUGIN_JS": ViewerJSPluginJS.render(
				SHOW_JS_TOOLBAR='' if self.isJSToolBarVisible() else 'style="display: none;"',
				SHOW_NAVBAR='' if self.isNavBarVisible() else 'style="display: none;"',
			),
            "VIEWER_JS_PLUGIN_CSS": ViewerJSPluginCSS,
            "PATH_IS_FOLDER": isdir,
            "GALLERY_INFO": gallery_info,
			"CSS_GRAD": self.css_grad,
        })
        render_url = FigD.createTempUrl(html)
        self.browser.load(render_url)
        # self.filetree.setRootPath(path)
        # print(path)
def launch_imageviewer(app):
    # accent color and css grad color.
    from fig_dash.theme import FigDAccentColorMap
    accent_color = FigDAccentColorMap["imageviewer"]
    grad_colors = extract_colors_from_qt_grad(accent_color)
    css_grad = create_css_grad(grad_colors)
	# create ribbon menu for imageviewer.
    menu = ImageViewerMenu(accent_color=accent_color)
    menu.setFixedHeight(120)
    menu.hide()
    # create imageviewer widget.
    imageviewer = ImageViewerWidget(
		css_grad=css_grad, 
		accent_color=accent_color,
	)
    imageviewer.browser.setAccentColor(accent_color)
    imageviewer.connectMenu(menu)
    imageviewer.centralLayout.insertWidget(0, menu)
	# FigD window.
    window = wrapFigDWindow(
		imageviewer, title="Image Viewer", 
		icon="system/imageviewer/logo.svg",
		accent_color=accent_color,
		titlebar_callbacks={
			"autoSave": imageviewer.toggleAutoSave,
			"viewSourceBtn": imageviewer.viewSource,
		}
	)
    window.show()
    try: openpath = sys.argv[1]
    except IndexError: 
        openpath = "~/GUI/FigUI/FigUI/FigTerminal/static/terminal.svg"
    imageviewer.open(openpath)
    CtrlB = FigDShortcut(
		QKeySequence("Ctrl+B"), imageviewer, 
		"Toggle side pannel visibility"
	)
    CtrlB.activated.connect(imageviewer.side_panel.toggle)

def imageviewer_factory(**args):
	# create ribbon menu for imageviewer.
    css_grad = args.get("accent_color", 'yellow')
    openpath = args.get("openpath", FigD.icon("system/imageviewer/lenna.png"))
    accent_color = args.get("accent_color", 'yellow')
    show_navbar = args.get("show_navbar", False)
    add_js_toolbar = args.get("add_js_toolbar", False)
    s = time.time()
    menu = ImageViewerMenu(accent_color=accent_color)
    menu.setFixedHeight(120)
    menu.hide()
    print(f"menu created in: {time.time()-s}")
    # create imageviewer widget.
    s = time.time()
    imageviewer = ImageViewerWidget(
		css_grad=css_grad, 
		show_navbar=show_navbar,
		accent_color=accent_color,
		add_js_toolbar=add_js_toolbar,
		
	)
    print(f"ImageViewerWidget created in: {time.time()-s}")
    s = time.time()
    imageviewer.browser.setAccentColor(accent_color)
    imageviewer.connectMenu(menu)
    imageviewer.centralLayout.insertWidget(0, menu)
    imageviewer.setStyleSheet("background: transparent; border: 0px;")
    CtrlB = FigDShortcut(
		QKeySequence("Ctrl+B"), imageviewer, 
		"Toggle side pannel visibility"
	)
    CtrlB.activated.connect(imageviewer.side_panel.toggle)
    imageviewer.open(openpath)

    return imageviewer

def imageviewer_window_factory(**args):
    from fig_dash.theme import FigDAccentColorMap
    # accent color and css grad color.
    LENNA_PATH = FigD.icon("system/imageviewer/lenna.png")
    openpath = args.get("openpath", LENNA_PATH)
    accent_color = FigDAccentColorMap["imageviewer"]
    widget_args = {
		"css_grad": create_css_grad(extract_colors_from_qt_grad(accent_color)),
		"openpath": openpath,
		"accent_color": accent_color,
        "show_navbar": args.get("show_navbar", False),
        "add_js_toolbar": args.get("add_js_toolbar", False),
	}
    imageviewer = imageviewer_factory(**widget_args)
    tab_title = Path(openpath).stem
    tab_icon = openpath
    window = wrapFigDWindow(
		imageviewer, title="Image Viewer", icon="system/imageviewer/logo.svg",
		accent_color=accent_color, name="imageviewer", widget_args=widget_args,
        widget_factory=imageviewer_factory, window_args=args, 
		titlebar_callbacks={
			"autoSave": imageviewer.toggleAutoSave,
			"viewSourceBtn": imageviewer.viewSource,
		}, window_factory=imageviewer_window_factory,
		find_function=imageviewer.browser.reactToCtrlF,
		tab_title=tab_title, tab_icon=tab_icon,
	)

    return window

def parse_imageviewer_args():
	parser = argparse.ArgumentParser("system imageviewer application for Fig Dashboard")
	parser.add_argument("-p", "--path", type=str, help="path to opened image", 
						default=FigD.icon("system/imageviewer/lenna.png"))
	parser.add_argument("-n", "--show_navbar", action="store_true", help="show navbar.")
	parser.add_argument("-jt", "--add_js_toolbar", action="store_true", 
						help="add javascript based toolbar to imageviewer web view.")

	return parser.parse_args()

def test_imageviewer():
    FigD("/home/atharva/GUI/fig-dash/resources")
    app = FigDAppContainer(sys.argv)
    args = parse_imageviewer_args()
    # openpath = "~/Pictures/atharva.jpg"
	# openpath = "~/GUI/FigUI/FigUI/FigTerminal/static/terminal.svg"
    window = imageviewer_window_factory(**vars(args))
    window.show()
    app.exec()

if __name__ == "__main__":
    test_imageviewer()
