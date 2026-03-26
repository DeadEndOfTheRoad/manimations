import os
import time
import numpy as np
import cv2
import pyautogui
import mss
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageGrab

project_dir = os.getcwd()
temp_dir = os.path.join(project_dir, "temp")
os.makedirs(temp_dir, exist_ok=True)
path = os.path.join(temp_dir, f"page_{i}.png")

def take_windows_snip(coords, path):

    x1, y1, x2, y2 = coords

    pyautogui.hotkey("win", "shift", "s")
    time.sleep(0.7)

    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    time.sleep(0.3)
    pyautogui.moveTo(x2, y2, duration=0.2)
    pyautogui.mouseUp()
    time.sleep(0.3)

    img = ImageGrab.grabclipboard()

    if img:
        img.save(path)
    else:
        raise RuntimeError("Clipboard did not receive snip image")


img = take_windows_snip((0, 0, 1920, 1080), path)

