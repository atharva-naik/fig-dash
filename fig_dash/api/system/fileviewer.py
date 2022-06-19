import os
import sys
import time
import jinja2
from typing import *
from pathlib import Path
from fig_dash.assets import FigD
# Qt imports.
from PyQt5.QtCore import Qt, QObject, QUrl, QMimeDatabase, QFileInfo
from PyQt5.QtWidgets import QFileIconProvider, QApplication

# caching path for all thumbnails: PDFs, videos, 3D models.
FILE_VIEWER_CACHE_PATH = os.path.expanduser("~/.cache/fig_dash/fileviewer/thumbnails")
# file viewer backend.
class FileViewerBackend:
    def __init__(self, folder: str="~", **args):
        from fig_dash.api.js.system import SystemHandler

        folder = os.path.expanduser(folder) 
        self.folder = Path(folder)
        # rendering params.
        self.params = {}
        # system handler for api js.
        self.systemHandler = SystemHandler()
        # mimetype database and icon provider.
        self.mime_database = QMimeDatabase()
        self.icon_provider = QFileIconProvider()
        #  file path lists.
        self.listed_filenames = []
        self.listed_full_paths = []
        self.listed_hidden_files = []
        self.loaded_file_items = []
        # intialization arguments.
        self.font_color = args.get("font_color", '#fff')
        self.background_image = args.get("background", "")

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

    def open(self, folder: str="~") -> Tuple[str, int, int, int, int]:
        """open a file/folder location."""
        from fig_dash.utils import collapseuser
        from fig_dash.ui.js.webchannel import QWebChannelJS
        from fig_dash.ui.js.fileviewer import FileViewerHtml, FileViewerStyle, FileViewerCustomJS, FileViewerMJS, ViSelectJS
        # expand user.
        folder = os.path.expanduser(folder) 
        # call xdg-open if a file is clicked instead of a folder.
        if os.path.isfile(folder): 
            mimetype = self.callXdgOpen(folder)
            return f"opening file of type {mimetype} with xdg-open", 0, 0, 0, 0
        # might be a device or something.
        if not os.path.isdir(folder):
            return f"can't open {folder} as it is not a file or directory", 0, 0, 0, 0
        # check if the user has permission to view folder
        try: os.scandir(folder)
        except PermissionError as e:
            print("fileviewer.open", e)
            return f"api::system::fileviewer::FileViewerBackend.open:{e}", 0, 0, 0, 0
        self.folder = Path(folder)
        listed, full_paths, hidden_flag_list = self.listFiles(folder)
        # populate content for searching.
        self.listed_filenames = listed
        self.listed_full_paths = full_paths
        self.listed_hidden_files = hidden_flag_list
        # file, folder and hidden file counts.
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
        # self.statusbar.updateBreakdown(
        #     files=file_count, hidden=hidden_count,
        #     items=len(self.listed_filenames),
        #     folders=folder_count,
        # )
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
        # create list of icons.
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
        # icon theme paths.
        icon_theme_devices_path = FigD.icon("devices")
        icon_theme_places_path = FigD.icon("places")
        icon_theme_mimes_path = FigD.icon("mimetypes")
        # if os.path.exists(icon_theme_places_path):
        icon_paths = []
        for name, mimetype, full_path in icons:
            if name == "":
                name = "text-plain"
            elif os.path.isdir(full_path):
                if full_path == os.path.expanduser("~/Pictures"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-image.svg"))
                elif full_path == os.path.expanduser("~/Desktop"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "user-desktop.svg"))
                elif full_path.endswith("/Templates"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-templates.svg"))
                elif full_path.endswith("/Documents"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-documents.svg"))
                elif full_path.endswith("/Downloads"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-download.svg"))
                elif full_path.endswith("Videos"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-video.svg"))
                elif full_path.endswith("Music"):
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder-music.svg"))
                else:
                    icon_paths.append(os.path.join(icon_theme_places_path, "folder.svg"))
            elif mimetype.startswith("image/"):
                path = full_path
                icon_paths.append(path)
            elif mimetype in ["application/pdf"]:
                # check if file is already cached.
                filename = full_path.replace("/", "|")
                cached_file_path = os.path.join(FILE_VIEWER_CACHE_PATH, filename + ".png")
                if os.path.exists(cached_file_path):
                    icon_paths.append(cached_file_path)
                else: 
                    path = os.path.join(icon_theme_mimes_path, name+".svg")
                    if os.path.exists(path): 
                        icon_paths.append(path)
                        continue
                    path = os.path.join(icon_theme_places_path, name+".svg")
                    if os.path.exists(path): 
                        icon_paths.append(path)
                        continue
                    path = os.path.join(icon_theme_devices_path, name+".svg")    
                    if os.path.exists(path): 
                        icon_paths.append(path)
                        continue
                    path = FigD.icon("mimetypes/text-plain.svg")
                    icon_paths.append(path)                  
            else:
                # print(mimetype, name, full_path)
                path = os.path.join(icon_theme_mimes_path, name+".svg")
                if os.path.exists(path): 
                    icon_paths.append(path)
                    continue
                path = os.path.join(icon_theme_places_path, name+".svg")
                if os.path.exists(path): 
                    icon_paths.append(path)
                    continue
                path = os.path.join(icon_theme_devices_path, name+".svg")    
                if os.path.exists(path): 
                    icon_paths.append(path)
                    continue
                path = FigD.icon("mimetypes/text-plain.svg")
                icon_paths.append(path)
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
            "FILEVIEWER_ITEMS": self.format_listed(listed),
            "BACKGROUND_IMAGE": self.background_image,
            "HIDDEN_FLAG_LIST": hidden_flag_list,
            "NUM_ITEMS": len(listed),
        }
        self.params.update(self.systemHandler.js_sources)
        viewer_html = jinja2.Template(
            FileViewerHtml.render(**self.params)
        ).render(**self.params)
        # s = time.time()
        # for path in full_paths: 
        #     self.createThumbnailWorker(path=path, thumb_size=240)
        # print(f"\x1b[32;1m**created thumbnail workers in {time.time()-s}s**\x1b[0m")
        return viewer_html, file_count, hidden_count, len(self.listed_filenames), folder_count

    def format_listed(self, prelisted: list):
        listed = []
        for rec in prelisted:
            listed.append(rec)

        return listed    

    def callXdgOpen(self, path: str) -> str:
        '''call xdg-open for the appropriate mimetype.'''
        mimetype = self.mime_database.mimeTypeForFile(path).name()
        FigD.debug(f"{path}: calling xdg-open for {mimetype} files")
        url = QUrl.fromLocalFile(path).toString()
        os.system(f'xdg-open "{url}"')

        return mimetype

# test fileviewer backend for testing creation of file viewer pages.
if __name__  == "__main__":
    app = QApplication(sys.argv)
    file_viewer_backend = FileViewerBackend()
    html, file_count, hidden_count, items_count, folder_count = file_viewer_backend.open("~/Pictures")
    print(f"{items_count} items, file_count: {file_count}, hidden_count: {hidden_count}, folder_count: {folder_count}")
    print(html)
    app.exec()