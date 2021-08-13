import numpy as np
from cv2 import cv2 as cv
from time import time
from record import window_id, window_screenshot


screenshot = cv.imread('colorpick.png')
hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

status = cv.imwrite("~/Documents/minecraft_bot2/main/status.jpg", hsv)
cv.imshow('screenshot', hsv)
while True:
    if cv.waitKey(1) == ord('q'):
        break
