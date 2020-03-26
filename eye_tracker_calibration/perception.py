
import cv2
import numpy as np



"""
get_laser_pos() takes an image as the input and 
finds the coordinates of the red laser in the image
"""
def get_laser_pos(img):
    height, width, channel = img.shape
    low_range = np.array([160, 150, 150])
    high_range = np.array([179, 255, 255])

    # convert to HSV space, apply gaussian blur, apply red threshold
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv_mask = cv2.inRange(img_hsv, low_range, high_range)
    img_hsv_mask_blur = cv2.GaussianBlur(img_hsv_mask, (5, 5), 0)
    points = cv2.findNonZero(img_hsv_mask_blur)

    # average of all the red points
    if (points is None):
        print("laser not found")
        return 0
    else:
        avg = np.mean(points, axis=0)
        avg = avg[[0]]
        centre = (int(avg[0]), int(avg[1]))

    return centre


"""
get_warp_matrix() takes an image as the input and
detects the screen, crops it, finds the affine transform matrix
"""
def get_warp_matrix(img):
    M = np.zeros((3, 3))
    col, row = img[:2]
    IS_FOUND = False
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # preprocessing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bilateralFilter(img, 1, 10, 120)
    img = cv2.Canny(img, 10, 250)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # find all contours
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # find contour with a large area
        if cv2.contourArea(c) < 20000: continue

        arc_len = cv2.arcLength(c, True)
        c_approx = cv2.approxPolyDP(c, 0.1 * arc_len, True)

        # find if it's a square
        if (len(c_approx) != 4): continue
        IS_FOUND = True

        # rearrange its points in order, and pass them in getPerspectiveTransform()
        box = np.array([c_approx[0][0], c_approx[1][0], c_approx[2][0], c_approx[3][0]], dtype="float32")
        box = order_points(box)
        target = np.float32([[0, 0], [row, 0], [row, col], [0, col]])
        M = cv2.getPerspectiveTransform(box, target)

    if (IS_FOUND):
        return M
    else:
        print("screen not found")
        return 0


"""
order_points() takes 4 points and arranges them such that
they are in order: topleft - topright - bottomright - bottomleft
"""
def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


"""
apply_transform() applies the transformation matrix M
"""
def apply_transform(img, M):
    col, row = img[:2]
    out_img = cv2.warpPerspective(img, M, (row, col))
    return out_img


"""
get_cropped_img() takes a raw camera image as the input and
return a cropped version
"""
def get_cropped_img(cap, M):
    img = cap.read()
    M = get_warp_matrix(img)
    img = apply_transform(img, M)
    return img


"""
get_target_circles() takes an image as the input and
return a list of points that are the coordinates of the target points
"""
def get_target_circles(img):
    height, width, channel = img.shape
    low_range = np.array([100, 100, 100])
    high_range = np.array([120, 255, 255])

    # find connected components
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_range, high_range)
    output = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    num_labels = output[0]
    labels = output[1]

    # make the image b&w, set background black
    labels = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(labels)
    labeled_img = cv2.merge([labels, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2GRAY)
    labeled_img[labels == 0] = 0

    # hough circles
    circles_temp = cv2.HoughCircles(labeled_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=2, minRadius=2, maxRadius=30)
    circles = circles_temp[0, :, :]
    circles = np.uint16(np.around(circles))

    return circles


