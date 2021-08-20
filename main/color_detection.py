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

    # choose the colors that are going to be extracted
    lower_red = np.array([0, 100, 90])
    upper_red = np.array([19, 51, 69])

    # https://docs.opencv.org/master/da/d97/tutorial_threshold_inRange.html
    mask = cv.inRange(hsv, lower_red, upper_red)

    # look doc lol
    result = cv.bitwise_and(hsv, hsv, mask=mask)

    # resizing img
    scale = 0.6
    hsv = cv.resize(hsv, None,  fx=scale, fy=scale, interpolation=cv.INTER_LINEAR)
    cv.imshow('screenshot', result)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        break
