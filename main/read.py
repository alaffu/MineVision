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


loop_time = time()
location = window_id()
while True:
    # i can make it this run faster if i take the screenshots wihout using this
    # library

    screenshot = window_screenshot(location)
    screenshot = cv.imread('screenshot.jpg')
    width = int(screenshot.shape[1])
    height = int(screenshot.shape[0])

    # cv.line paramaters is a source image, starting position, ending position
    # color and line thickness
    img = cv.line(screenshot, (0, 0), (width, height), (255, 0, 0), 10)

    # resizing img
    img = cv.resize(img, (300, 300), interpolation=cv.INTER_LINEAR)

    cv.imshow('computer vision', img)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print("Done")

# translations
# def translate(img, x, y):
#     transMat = np.float32([[1, 0, x], [0, 1, y]])
#     dimensions = (img.shape[1], img.shape[0]) # img.shape[1] returns the widht
#                                               # img.shape[2] returns height
#     return cv.warpAffine(img, transMat, dimensions)

# translated = translate(img, 10, -10)

