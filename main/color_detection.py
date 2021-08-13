import numpy as np
from cv2 import cv2 as cv
from time import time
from record import window_id, window_screenshot


loop_time = time()
location = window_id()

while True:
    screenshot = window_screenshot(location)
    screenshot = cv.imread('screenshot.jpg')
    width = int(screenshot.shape[1])
    height = int(screenshot.shape[0])

    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    cv.imshow('screenshot', hsv)
    lower_blue = np.array([])
    upper_blue = np.array([])

    # resizing img
    scale = 0.6
    hsv = cv.resize(hsv, None,  fx=scale, fy=scale, interpolation=cv.INTER_LINEAR)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        break
