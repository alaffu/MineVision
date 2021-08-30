import cv2 as cv
import numpy as np
from vision import Vision
from record import window_screenshot, window_id


vision_whitetrunk = Vision("assets/white_trunk.jpg")

vision_whitetrunk.init_control_gui()
windows_number = window_id()
while True:
    window_screenshot(windows_number)
    screenshot = 'screenshot.jpg'
    screenshot = cv.imread(screenshot)

    output = vision_whitetrunk.apply_hsv_filter(screenshot)

    # run detection algorithm
    # rectangles = vision_whitetrunk.find(screenshot)

    # draw detection results onto the original image
    # click = vision_whitetrunk.get_click_positions(rectangles)
    # output = vision_whitetrunk.draw_crosshairs(screenshot, click)
    cv.imshow("Matches", output)

    if cv.waitKey(1) == ord("q"):
        break
