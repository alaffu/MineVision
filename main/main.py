import cv2 as cv
import numpy as np
from vision import Vision
from record import window_screenshot, window_id


vision_whitetrunk = Vision("assets/white_trunk.jpg")
windows_number = window_id()
while True:
    window_screenshot(windows_number)
    points, truth = vision_whitetrunk.find("screenshot.jpg")

    if truth == 1:
        break
