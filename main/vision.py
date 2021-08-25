import cv2 as cv
import numpy as np #a
from record import window_screenshot, window_id


class Vision:

    # properties
    template = None
    w, h = 0
    method = None

    def __init__(self, template, method=cv.TM_CCOEFF_NORMED):
        self.template = cv.imread(template, 0)
        self.w, self.h = template.shape[::-1]

        self.method = method

    def findClickPositions(self, img_path, threshold=0.45, debug_mode=None):
        # truth will represent the state of debug mode, if it returns 0 debug mode
        # didn't run and if it returns 1 it did run.
        truth = 0

        img = cv.imread(img_path)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(img_gray, self.template, self.method)

        location = np.where(result >= threshold)
        location = list(zip(*location[::-1]))

        # list of rectangles needs to be [x, y, w, h]
        rect_list = []

        for loc in location:
            rect = [int(loc[0]), int(loc[1]), self.w, self.h]
            # it's appending two times bc then it will have two duplicates,
            # this is necessary groupRectangles will throw away every result
            #  that doesn't have overlapping rectangles.
            rect_list.append(rect)
            rect_list.append(rect)

        rect_list, weights = cv.groupRectangles(rect_list, 1, 0.5)
        print(rect_list)

        # loop over all the locations and draw their rectangle

        points = []
        if len(rect_list):

            # config for drawMarker function
            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            marker_color = (0, 100, 255)
            # marker_type = cv.MARKER_CROSS

            # loop all over the locations and draw their rectangle
            for (x, y, w, h) in rect_list:

                # get the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # save the points
                points.append((center_x, center_y))

                if debug_mode == "rectangles":
                    # drawing rectangles
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(img, top_left, bottom_right, line_color, 2, line_type)

                elif debug_mode == "points":
                    cv.drawMarker(img, (center_x, center_y), marker_color)

        if debug_mode:

            cv.imshow("img", img)
            if cv.waitKey(1) == ord("q"):
                cv.destroyAllWindows()
                truth = 1
        return points, truth


windows_number = window_id()
while True:
    window_screenshot(windows_number)
    points, truth = findClickPositions('screenshot.jpg', "assets/white_trunk.jpg", debug_mode="rectangles")

    if truth == 1:
        break
