#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-
import os
import getpass
import platform

# get platform name.
PLATFORM_NAME = platform.system()
# populate global variables containing all the paths.
if PLATFORM_NAME == "Linux":
    CONFIG_DIR = os.path.expanduser("~/.config")
    CHROME_DIR = os.path.join(CONFIG_DIR, "google-chrome")
elif PLATFORM_NAME == "Windows":
    CONFIG_DIR = os.path.expanduser('''C:\\Users\\''' + getpass.getuser() + '''\\AppData\\Local''')
    CHROME_DIR = os.path.join(CONFIG_DIR, "Google\\Chrome")
elif PLATFORM_NAME == "Linux":
    CONFIG_DIR = ""
    CHROME_DIR = ""
# chrome paths.
CHROME_DEFAULT_DIR = os.path.join(CHROME_DIR, "Default")
CHROME_HISTORY = os.path.join(CHROME_DEFAULT_DIR, "History")
# fig-dash paths.
FIG_DASH_DIR = os.path.join(CONFIG_DIR, "fig-dash")
FIG_DASH_DEFAULT_DIR = os.path.join(FIG_DASH_DIR, "Default")
FIG_DASH_CHROME_HISTORY = os.path.join(FIG_DASH_DEFAULT_DIR, "ChromeHistory")
FIG_DASH_BROWSER_HISTORY = os.path.join(FIG_DASH_DEFAULT_DIR, "History")
# create all config dirs.
os.makedirs(FIG_DASH_DIR, exist_ok=True)
os.makedirs(FIG_DASH_DEFAULT_DIR , exist_ok=True)
# os.makedirs(FIG_DASH_CHROME_HISTORY , exist_ok=True)