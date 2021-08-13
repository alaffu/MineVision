import pyautogui
import numpy as np
from cv2 import cv2 as cv
from time import time
from subprocess import Popen, PIPE
import os


def window_position():
    '''find location of the minecraft windows'''
    location = pyautogui.locateOnScreen('options.jpg',
                                        confidence=.8, grayscale=True)
    while location is None:
        location = pyautogui.locateOnScreen('options.jpg',
                                            confidence=.8, grayscale=True)
    pyautogui.click(location)

    location = pyautogui.locateOnScreen('option_resource.jpg',
                                        confidence=.8, grayscale=True)
    while location is None:
        location = pyautogui.locateOnScreen('option_resource.jpg',
                                            confidence=.8, grayscale=True)
    pyautogui.click(location)

    location = pyautogui.locateOnScreen('resource_pack.jpg',
                                        confidence=.8, grayscale=True)
    while location is None:
        location = pyautogui.locateOnScreen('resource_pack.jpg',
                                            confidence=.8, grayscale=True)

    return location


def window_id():
    '''linux commands to take id of the window'''

    windowsInfo = 'xwininfo | grep -w id | cut -f 3 -d ":" | cut -c 2-10'

    p = Popen(windowsInfo, shell=True,
              stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    windowNumber = str(out.decode())
    return windowNumber


def window_screenshot(windows_number):
    '''takes screenshot of the right screen'''
    windows_print = 'import -frame -window {} screenshot.jpg'.format(str(windows_number[0:9]))
    os.system(windows_print)


