from cv2 import cv2 as cv
from record import window_id, window_screenshot

location = window_id()
screenshot = window_screenshot(location)

screenshot = cv.imread('colorpick.png')
hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)

cv.imwrite("~/Documents/minecraft_bot2/main/colorpick.png", hsv)
cv.imshow('screenshot', hsv)
while True:
    if cv.waitKey(1) == ord('q'):
        break
