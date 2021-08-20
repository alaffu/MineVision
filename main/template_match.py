import cv2 as cv

img = cv.imread('assets/background.jpg', 0)
template = cv.imread('assets/white_trunk.jpg', 0)

h, w = template.shape

methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR, cv.TM_CCORR_NORMED,
           cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]

for method in methods:
    img2 = img.copy()

    result = cv.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result) #d
    print(min_loc, max_loc)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

    bottom_right = (location[0] + w, location[1] + h)
    cv.rectangle(img2, location, bottom_right, 255, 5)
    cv.imshow("mathc", img2)
    while True:
        if cv.waitKey(1) == ord("q"):
            cv.destroyAllWindows()
            break
