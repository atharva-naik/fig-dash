#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-
from fig_dash.assets import FigD

FigDAccentColorMap = {
    "clipboard": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #390b56, stop : 0.091 #420d64, stop : 0.182 #4c0f72, stop : 0.273 #561181, stop : 0.364 #601390, stop : 0.455 #6a169f, stop : 0.545 #7418ae, stop : 0.636 #7f1abe, stop : 0.727 #891cce, stop : 0.818 #941ede, stop : 0.909 #9f20ee, stop : 1.0 #aa22ff);", 
    "imageviewer": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #be9433, stop : 0.091 #c49935, stop : 0.182 #ca9d36, stop : 0.273 #cfa238, stop : 0.364 #d5a639, stop : 0.455 #dbab3b, stop : 0.545 #e1af3d, stop : 0.636 #e7b43e, stop : 0.727 #edb940, stop : 0.818 #f3be42, stop : 0.909 #f9c243, stop : 1.0 #ffc745)",
    # "mailviewer": "",
    "videoplayer": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #a00055, stop : 0.091 #a70054, stop : 0.182 #ae0052, stop : 0.273 #b50250, stop : 0.364 #bc064e, stop : 0.455 #c20b4c, stop : 0.545 #c81149, stop : 0.636 #ce1746, stop : 0.727 #d41e43, stop : 0.818 #d92440, stop : 0.909 #de2a3c, stop : 1.0 #e33138)",
    # "audioviewer": "",
    # "translator": "",
    "codeeditor": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #eb5f34, stop : 0.091 #f95a59, stop : 0.182 #ff5c7d, stop : 0.273 #fd65a0, stop : 0.364 #f373c1, stop : 0.455 #e184dd, stop : 0.545 #c995f3, stop : 0.636 #aca5ff, stop : 0.727 #8eb4ff, stop : 0.818 #72c0ff, stop : 0.909 #5dcaff, stop : 1.0 #56d3ff)",
    # "qconicalgradient(cx: 0, cy: 0, angle: 0, stop : 0.0 #eb5f34, stop : 0.091 #f95a59, stop : 0.182 #ff5c7d, stop : 0.273 #fd65a0, stop : 0.364 #f373c1, stop : 0.455 #e184dd, stop : 0.545 #c995f3, stop : 0.636 #aca5ff, stop : 0.727 #8eb4ff, stop : 0.818 #72c0ff, stop : 0.909 #5dcaff, stop : 1.0 #56d3ff);",
    "fileviewer": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #124b7f, stop : 0.091 #175187, stop : 0.182 #1c578e, stop : 0.273 #215e96, stop : 0.364 #25649e, stop : 0.455 #296ba5, stop : 0.545 #2e71ad, stop : 0.636 #3278b5, stop : 0.727 #367ebd, stop : 0.818 #3a85c5, stop : 0.909 #3e8ccd, stop : 1.0 #4293d5);",
    "app_launcher": "qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #105adf, stop : 0.091 #0067e7, stop : 0.182 #0073ed, stop : 0.273 #007ef2, stop : 0.364 #0089f6, stop : 0.455 #0093f9, stop : 0.545 #009dfb, stop : 0.636 #00a7fc, stop : 0.727 #00b1fd, stop : 0.818 #00bafd, stop : 0.909 #00c3fc, stop : 1.0 #0cccfc);",
}
FigDSystemAppIconMap = {
    "clipboard": FigD.icon("system/clipboard/logo.png"), 
    "fileviewer": FigD.icon("system/fileviewer/logo.svg"),
    "imageviewer": FigD.icon("system/imageviewer/logo.svg"),
    # "mailviewer": "",
    "videoplayer": FigD.icon("system/videoplayer/logo.png"),
    # "audioviewer": "",
    # "translator": "",
    "codeeditor": FigD.icon("widget/codemirror/logo.png"),
    "app_launcher": FigD.icon("system/app_launcher.png"),
}


class DashStyleCenter:
    pass

class DashThemeCenter:
    pass