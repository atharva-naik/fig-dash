#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.policy import default
from fig_dash import FigDLoad
FigDLoad("fig_dash::utils")

import os
from typing import *

# utility functions.
def collapseuser(path: str):
    return path.replace(os.path.expanduser("~"), "~")

# sleep for `time` secs. 
def pyqtSleep(time: int=1000):
    """A pyqt5 friendly version of time.sleep.
    time to wait in millis
    """
    from PyQt5.QtCore import QEventLoop, QTimer
    loop = QEventLoop()
    QTimer.singleShot(time, loop.quit)
    loop.exec_()

# human readable memory format
def h_format_mem(size: int):
    """convert bytes to human readable format.
    Args:
        size (int): memory size in bytes as integer.
    Returns:
        str: human readable memory size as string with suffix.
    """
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024*1024:
        return f"{round(size/1024, 2)} kB"
    elif size < 1024*1024*1024:
        return f"{round(size/(1024*1024), 2)} MB"
    elif size < 1024*1024*1024*1024:
        return f"{round(size/(1024*1024*1024), 2)} GB"
    else: 
        return f"{round(size/(1024*1024*1024*1024), 2)} TB"

def truncStr(string):
    if len(string) > 20:
        return string[:10]+"..."+string[-6:]
    else:
        return string

def notify(msg: Union[str, None]=None, icon: Union[str, None]=None, 
           title: Union[str, None]=None, critical: Union[bool, None]=False):
    """Send notification for different platforms. currently only supported for Linux.
    This function is just a wrapper for platform specific APIs.
    #### Linux: 
    notify-send command is used to send notifications.
    #### Windows: 
    Not supported yet.
    #### Darwin: 
    Not supported yet.
    
    #### Args:
        msg (Union[str, None], optional): Message to be shown. Defaults to None.
        icon (Union[str, None], optional): Icon for application. Defaults to None.
        title (Union[str, None], optional): Title/Name of the app. Defaults to None.
        critical (Union[bool, None], optional): Show critical notification. Defaults to False.
    """
    import getpass, platform
    if title is None: title = "Fig Dashboard"
    if msg is None: msg = f"Hello {getpass.getuser()}!"
    # /home/atharva/GUI/fig-dash/resources/icons/logo.svg
    if platform.system() == "Linux":
        code = f'''notify-send "{title}" "{msg}"'''
        if icon: code += f" -i {icon}" 
        if critical: code += f" -u critical"
        # print("\x1b[34;1mcode:\x1b[0m", code)
        os.system(code)

def secs_to_hms(secs):
    hrs = secs // 3600
    mins = (secs % 3600) // 60
    
    return (hrs, mins, secs)

def secs_to_htime(secs):
    if secs < 0: return (0, 0, 0)
    hrs = secs // 3600
    mins = (secs % 3600) // 60
    secs = secs - 3600*hrs - 60*mins

    return (hrs, mins, secs)

def QFetchIcon(url: str, is_svg=True):
    import requests
    from PyQt5.QtGui import QIcon

    content = requests.get(url)
    if is_svg: 
        path = "/tmp/lol1_2hjalx_ffl2c.svg"
        with open(path, "w") as f:
            f.write(content.text)
    else: 
        path = "/tmp/lol1_2hjalx_ffl2c.png"
        with open(path, "wb") as f:
            f.write(content.content)
    icon = QIcon(path)
    
    return icon

def sampleRGB() -> Tuple[int,int,int]:
    import random
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    # a = random.randint(125,255)
    return (r,g,b)

def sampleRGBA() -> Tuple[int,int,int,int]:
    import random
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    a = random.randint(125,255)
    
    return (r,g,b,a)

def sampleRGBSeries(n: int, center: Union[Tuple[int,int,int],None]=None,
                    width: Union[Tuple[int,int,int],int]=25) -> List[Tuple[int,int,int]]:
    import random
    series = []
    if center is None:
        center = sampleRGB()
    if isinstance(width, int):
        width = (width, width, width)
    for i in range(n):
        rW = min(max(random.randint(-width[0]//2, width[0]//2),0),255)
        gW = min(max(random.randint(-width[1]//2, width[1]//2),0),255)
        bW = min(max(random.randint(-width[2]//2, width[2]//2),0),255)
        series.append((
            center[0] - rW,
            center[1] - gW,
            center[2] - bW,
        ))

    return series

def brightenRGB(rgb: Tuple[int,int,int], ratio: float) -> Tuple[int,int,int]:
    """Transform RGB triple, by making it brighter or dimmer.

    Args:
        rgb (Tuple[int, int, int]): (R,G,B) color triple.
        ratio (float): If the ratio is x, the returned tuple is n times brighter.

    Returns:
        Tuple[int, int, int]: transformed RGB triple"""
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    return rgb 

def extractSliderColor(gradient: str, where="back") -> str:
    """Extract the first or last color from a qgradient stylesheet string.

    Args:
        gradient (str): qgradient stylesheet string.
        where (str, optional): Whether the first stop or last stop has to be extacted. 
        Defaults to "back".

    Returns:
        str: extracted color as hex string.
    """
    if ("qlineargradient" in gradient or "qconicalgradient" in gradient) and (where=="back"):
        sliderColor = gradient.split(":")[-1].strip()
        sliderColor = sliderColor.split()[-1]
        sliderColor = sliderColor.split(")")[0]
        sliderColor = sliderColor.strip()
    elif ("qlineargradient" in gradient or "qconicalgradient" in gradient) and (where=="front"):
        sliderColor = gradient.split("stop")[1]
        sliderColor = sliderColor.split("#")[-1]
        sliderColor = sliderColor.split(",")[0]
        sliderColor = "#"+sliderColor.strip()
    else: 
        sliderColor = "white" 

    return sliderColor

def exif_color_space(img):
    exif = img._getexif() or {}
    a = exif.get(0xA001)
    b = exif.get(0x0001)
    if a == 1 or b == 'R98':
        return 'sRGB'
    elif a == 2 or b == 'R03':
        return 'Adobe RGB'
    elif a is None and b is None:
        return 'Empty EXIF tags ColorSpace and InteropIndex'
    else:
        return f'UNKNOWN color space ({a}, {b})'

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

# class to document objects.
class ObjectDocumenter:
    def _serialize_param(self, param) -> dict:
        import inspect
        assert isinstance(param, inspect.Parameter)
        return {
            "default": "" if param.default == inspect._empty else str(param.default),
            "kind": str(param.kind),
            "annotation": "" if param.annotation == inspect._empty else str(param.annotation),
            "isdefault": False if param.default == inspect._empty else True
        }

    def __call__(self, obj, to_string=False) -> Union[List[dict], str]:
        import inspect
        functions = []
        # function, builtin_function_or_method
        fn_type_list = [
            "<class 'builtin_function_or_method'>", 
            "<class 'function'>", "<class 'method'>", 
        ]
        for attr_name in dir(obj):
            if attr_name.startswith("__") and attr_name.endswith("__"): continue
            attr = getattr(obj, attr_name)
            # print("getting documentation for:", attr_name)
            if str(type(attr)) in fn_type_list:
                try: 
                    signature = inspect.signature(attr)
                    return_annotation = "" if signature.return_annotation == inspect._empty else str(signature.return_annotation)
                    params = {k: self._serialize_param(p) for k,p in dict(signature.parameters).items()}
                    functions.append({
                        "name": attr_name, 
                        "parameters": params,
                        "docstring": attr.__doc__,
                        "return_annotation": return_annotation,
                    })
                except ValueError:
                    functions.append({
                        "name": attr_name, 
                        "parameters": {},
                        "docstring": attr.__doc__,
                        "return_annotation": "UNKNOWN",
                    })
        if to_string:
            return self._serialize_function_docs(functions)
        else: return functions

    def _serialize_function_docs(self, funcs: List[dict]) -> str:
        docs = ""
        for func in funcs:
            paramStrs = []
            for name, pdict in func["parameters"].items():
                paramStr = name
                if pdict["annotation"] != "":
                    paramStr += f": {pdict['annotation']}"
                if pdict["isdefault"]:
                    paramStr += f"={pdict['default']}"  
                paramStrs.append(paramStr)
            paramsStr = ", ".join(paramStrs)
            docs += f"def {func['name']}({paramsStr})"
            if func['return_annotation'] != "":
                docs += f" -> {func['return_annotation']}:\n"
            else: docs += ":\n"
            docs += f'''    """{func['docstring']}"""\n'''
            docs += "\n"

        return docs