#!/usr/bin/python3
import Xlib
import Xlib.display

disp = Xlib.display.Display()
root = disp.screen().root 

NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
# print(NET_ACTIVE_WINDOW, NET_WM_NAME)
current_window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
current_window = disp.create_resource_object('window', current_window_id)
current_window_name = current_window.get_full_property(NET_WM_NAME, 0).value
for window in root.query_tree().children:
    if window.get_wm_class() is not None:
        print(window.get_wm_class())
print(type(window))
print(current_window_id)
print(current_window_name)
# root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
# while True:
#     try:
#         window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
#         window = disp.create_resource_object('window', window_id)
#         window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
#         window_name = window.get_full_property(NET_WM_NAME, 0).value
#     except Xlib.error.XError: # simplify dealing with BadWindow
#         window_name = None
#     print(window_name)
#     event = disp.next_event()