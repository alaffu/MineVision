import pyautogui
import numpy as np
from cv2 import cv2 as cv
from time import time
from subprocess import Popen, PIPE
import os
from record import window_id, window_screenshot


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

    # cv.rectangle paramaters source image, center position( bottom left corner
    # , top right corner), radius, color, line thickness(-1 to fill)
    img = cv.rectangle(img, (100, 100), (200, 200), (128, 128, 128), 6)

    # to display text a font is needed 
    font = cv.FONT_HERSHEY_SIMPLEX

    # paramaters putText is source image, text, center position, font, font
    # scale, color, line thickness, line type
    img = cv.putText(img, 'so nice', (200, height - 10), font, 4, (0, 0, 0), 5, cv.LINE_AA)



    # resizing img
    scale = 0.6
    img = cv.resize(img, None,  fx=scale, fy=scale, interpolation=cv.INTER_LINEAR)

    cv.imshow('computer vision', img)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print("Done")
