#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-
import sys
from fig_dash import DashUI


def main(**kwargs):
    ui = DashUI(sys.argv, **kwargs)
    ui.launch(maximized=True)


if __name__ == '__main__':
    main(
        x=100, y=100, w=1000, h=850,
        maximize_by_default=False, 
        icon="/home/atharva/GUI/fig-dash/resources/icons/logo.svg",        
        wallpaper="/home/atharva/Pictures/Wallpapers/3339083.jpg",
        resources="/home/atharva/GUI/fig-dash/resources",
        windowFlags=["frameless"],
    ) # /home/atharva/Pictures/Wallpapers/3339083.jpg