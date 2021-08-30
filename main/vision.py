import cv2 as cv
import numpy as np #a
from hsvfilter import HsvFilter


class Vision:

    # constants
    TRACKBAR_WINDOW = "Trackbar"

    # properties
    template = None
    w, h = [0, 0]
    method = None

    def __init__(self, template, method=cv.TM_CCOEFF_NORMED):
        self.template = cv.imread(template, 0)
        self.w, self.h = self.template.shape[::-1]

        self.method = method

    def find(self, img_path, threshold=0.45, max_results=10):
        # truth will represent the state of debug mode, if it returns 0 debug mode
        # didn't run and if it returns 1 it did run.

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

        if len(rect_list) > max_results:
            rect_list = rect_list[:max_results]

        return rect_list

    def get_click_positions(self, rect_list):
        points = []

        if len(rect_list):

            # loop all over the locations and draw their rectangle
            for (x, y, w, h) in rect_list:

                # get the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # save the points
                points.append((center_x, center_y))
        return points

    def draw_rectangles(self, img, rect_list):
        # config for drawMarker function
        img = cv.imread(img)
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rect_list:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(img, top_left, bottom_right, line_color, 2, line_type)

        return img

    def draw_crosshairs(self, img, points):
        img = cv.imread(img)
        marker_color = (0, 100, 255)
        # marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(img, (center_x, center_y), marker_color)

        return img

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # cv.createTrackbar requires a callback function but we'll use
        # getTrackbarPos () to do lookups
        def nothing(position):
            pass

        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar("HMin", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("SMin", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("VMin", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("HMax", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("SMax", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("VMax", self.TRACKBAR_WINDOW, 0, 179, nothing)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos("HMax", self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos("SMax", self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos("VMax", self.TRACKBAR_WINDOW, 255)

        # trackbar for increasing/decreasing saturation and value
        cv.createTrackbar("SAdd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("SSub", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VAdd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VSub", self.TRACKBAR_WINDOW, 0, 255, nothing)

    def get_hsv_filter_from_controls(self):
        # get current position of all trackbars

        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos("HMin", self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos("SMin", self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos("VMin", self.TRACKBAR_WINDOW)

        hsv_filter.hMax = cv.getTrackbarPos("HMax", self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos("SMax", self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos("VMax", self.TRACKBAR_WINDOW)

        hsv_filter.sAdd = cv.getTrackbarPos("SAdd", self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos("SSub", self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos("VAdd", self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos("VSub", self.TRACKBAR_WINDOW)

        return hsv_filter

    def apply_hsv_filter(self, original_img, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # set minimum and maximum HSV values
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

        # apply thresholds
        # inRange() makes every pixel that is not in range black
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow()
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount

        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount

        return c
