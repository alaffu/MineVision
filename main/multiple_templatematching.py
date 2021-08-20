import cv2 as cv
import numpy as np #a
from record import window_id, window_screenshot
# timestamp 9:54


def findClickPositions(img, template, threshold=0.45, debug_mode=None):

    windows_number = window_id()
    while True:

        img = window_screenshot(windows_number)
        img = cv.imread("screenshot.jpg")
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        template = cv.imread('assets/white_trunk.jpg', 0)
        w, h = template.shape[::-1]

        result = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

        location = np.where(result >= threshold)
        location = list(zip(*location[::-1]))

        # list of rectangles needs to be [x, y, w, h]
        rect_list = []

        for loc in location:
            rect = [int(loc[0]), int(loc[1]), w, h]
            # it's appending two times bc then it will have two duplicates,
            # this is necessary groupRectangles will throw away every result
            #  that doesn't have overlapping rectangles.
            rect_list.append(rect)
            rect_list.append(rect)

        rect_list, weights = cv.groupRectangles(rect_list, 1, 0.5)
        print(rect_list)

        # loop over all the locations and draw their rectangle
        if len(rect_list):

            # config for drawMarker function
            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            marker_color = (0, 100, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rect_list:
                # drawing rectangles
                # top_left = (x, y)
                # bottom_right = (x + w, y + h)
                # cv.rectangle(img, top_left, bottom_right, line_color, 2, line_type)

                # get the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                cv.drawMarker(img, (center_x, center_y), marker_color)

            # location = cv.groupRectangles(rect_list, 3, 0.3)

        # for pt in zip(*location[::-1]):
        #     x = cv.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 2)

        cv.imshow("img", img)

        if cv.waitKey(1) == ord("q"):
            cv.destroyAllWindows()
            break
