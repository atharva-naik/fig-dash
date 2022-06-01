print("fig_dash::utils")
import os
from PIL import Image
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEventLoop, QTimer, QT_VERSION_STR
from typing import Union, Tuple, List


def collapseuser(path: str):
    return path.replace(os.path.expanduser("~"), "~")

def pyqtSleep(time: int=1000):
    '''
    A pyqt5 friendly version of time.sleep.
    time to wait in millis
    '''
    loop = QEventLoop()
    QTimer.singleShot(time, loop.quit)
    loop.exec_()

def h_format_mem(size):
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

def notify(msg=None, icon=None, title="Fig Dashboard", critical=False):
    import getpass
    import platform
    if msg is None: 
        msg = f"Hello {getpass.getuser()}!"
    # /home/atharva/GUI/fig-dash/resources/icons/logo.svg
    if platform.system() == "Linux":
        # use notify send for Linux.
        code = f'''notify-send "Fig Dashboard" "{msg}"'''
        if icon: code += f" -i {icon}" 
        if critical: code += f" -u critical"
        print("\x1b[34;1mcode:\x1b[0m", code)
        os.system(code)

def secs_to_hms(secs):
    hrs = secs // 3600
    mins = (secs % 3600) // 60
    
    return (hrs, mins, secs)

def QFetchIcon(url: str, is_svg=True) -> QIcon:
    import requests
    import tempfile

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
    # os.remove(path)
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

def exif_color_space(img: Image):
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