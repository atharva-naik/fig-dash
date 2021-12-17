#!/home/atharva/anaconda3/envs/fig-dash/bin/python
# -*- coding: utf-8 -*-
import sys
from fig_dash import DashUI


def main(**kwargs):
    ui = DashUI(sys.argv, **kwargs)
    ui.launch()


if __name__ == '__main__':
    main(maximize_by_default=False)