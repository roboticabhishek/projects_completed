import cv2
import numpy as np
import time

# objects and variables
cap = cv2.VideoCapture(0)
time.sleep(5)
low1 = np.array([130, 120, 70])
high1 = np.array([179, 255, 255])
low2 = np.array([0, 120, 70])
high2 = np.array([15, 255, 255])

# capturing the background
background = 0
for i in range(20):
    ret, background = cap.read()

while(cap.isOpened()):
    # read
    _, img = cap.read()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # inRange and mask
    mask1 = cv2.inRange(hsv, low1, high1)
    mask2 = cv2.inRange(hsv, low2, high2)
    mask1 = mask1 + mask2
    mask2 = cv2.bitwise_not(mask1)
    mask1 = cv2.merge([mask1, mask1, mask1])
    mask2 = cv2.merge([mask2, mask2, mask2])
    # bitwise operations
    res1 = cv2.bitwise_and(img, mask2)
    res2 = cv2.bitwise_and(background, mask1)
    res3 = cv2.addWeighted(res1, 1, res2, 1, 0)
    # show
    cv2.imshow("res3", res3)
    # break condition
    if cv2.waitKey(40) == 27: break

cap.release()
cv2.destroyAllWindows()




