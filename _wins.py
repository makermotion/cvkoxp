import win32gui
import time
from PIL import ImageGrab, Image
import numpy as np

def get_window_info():
    # set window info
    window_info = {}
    win32gui.EnumWindows(set_window_coordinates, window_info)
    return window_info

def set_window_coordinates(hwnd, window_info):
    if win32gui.IsWindowVisible(hwnd):
        if 'Knight' in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y
            window_info['x'] = x
            window_info['y'] = y
            window_info['width'] = w
            window_info['height'] = h
            window_info['name'] = win32gui.GetWindowText(hwnd)
            win32gui.SetForegroundWindow(hwnd)

def get_screen(x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    print(screen.size)
    img = np.array(screen.getdata(), dtype=np.uint8).reshape((screen.size[1], screen.size[0], 3))
    return img


wininf = get_window_info()
x1, y1, x2, y2 = wininf['x'], wininf['y'], wininf['width'], wininf['height']
Image.fromarray(get_screen(x1+700, y1, x2-700, y2-1000)).show()

