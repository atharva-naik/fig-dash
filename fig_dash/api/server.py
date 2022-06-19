import os
import sys
from flask import Flask, request 
from PyQt5.QtWidgets import QApplication, QWidget

# Flask server application.
FIG_DASH_SERVER = Flask(__name__, static_folder="/home",
                        static_url_path="/home")
FIG_DASH_SERVER.config["STATIC_FOLDER"] = "/home"
# FigD server api endpoints.
@FIG_DASH_SERVER.route("/api/system/fileviewer")
def open_fileviewer():
    from fig_dash.api.system.fileviewer import FileViewerBackend
    fileviewer_backend = FileViewerBackend(folder="~", background="/home/atharva/Pictures/Wallpapers/3339083.jpg")
    path = request.args.get("path", "~")
    print(path)
    html, file_count, hidden_count, items_count, folder_count = fileviewer_backend.open(path)
    print(f"{items_count} items, file_count: {file_count}, hidden_count: {hidden_count}, folder_count: {folder_count}")

    return html

# main section.
if __name__  == "__main__":
    app = QApplication(sys.argv)
    # create and show the widget.
    widget = QWidget()
    widget.setGeometry(0, 0, 10, 10)
    widget.show()
    # run the flask server.
    FIG_DASH_SERVER.run(debug=True)
    # run the app.
    app.exec()