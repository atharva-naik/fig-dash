#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# read chrome's browser notifications.
import getpass
notif_path = f"/home/{getpass.getuser()}/.config/google-chrome/Default/Platform Notifications/000003.log"

def read_chrome_notifs(path=notif_path):
    data = []
    with open(path, "rb") as f:
        for line in f:
            data.append(str(line).strip("\n").strip())
            print(str(line).strip().strip("\n"))

    return data