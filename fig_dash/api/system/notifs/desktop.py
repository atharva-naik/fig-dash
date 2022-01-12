def desktop_notify(msg, title="", icon=None):
    import os
    # import getpass
    import platform
    # if msg is None: 
    #     msg = f"Hello {getpass.getuser()}!"
    # if icon is None:
    #     current_dir = os.path.dirname(os.path.realpath(__file__))
    #     icon = os.path.join(current_dir, "../logo.png")
    #     print(icon)
    if platform.system() == "Linux":
        # use notify send for Linux.
        print(f'''notify-send "{title}" "{msg}" -i {icon}''')
        os.system(f'''notify-send "{title}" "{msg}" -i {icon}''')