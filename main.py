
import cv2
from control import *
import maestro
from mapping import *
import math as m
import numpy as np
from perception import *
import time


'''
step0: setup 
'''
# channel definitions
# computer USB port specification
s = maestro.Controller()
channels = [1, 2]
axes = ['H', 'V']


"""
step1: start camera capture
"""
cap = cv2.VideoCapture(1)
time.sleep(5)
img = cap.read()
row, col, ch = img.shape()
M = get_warp_matrix(img)


"""
step2: get the list of calibration points
"""
calib_points, H_array, V_array = get_calib_points(img)


"""
step3: get the servo angle grid by following the calibration points
"""
servo_angles, calib_points = get_lookup(s, channels, calib_points, cap, M, axes)


"""
step4: tobii eye tracker calibration screen1
"""
print('press y to begin calibration')
while(True):
    k = cv2.waitKey(1)
    if (k == ord('y')):
        break

img = get_cropped_img(cap, M)
circles = get_target_circles(img)
go_to_pos_without_feedback(s, circles, servo_angles, H_array, V_array, channels)


"""
step5: tobii eye tracker calibration screen2
"""
print('press y to begin calibration')
while(True):
    k = cv2.waitKey(1)
    if (k == ord('y')):
        break

img = get_cropped_img(cap, M)
circles = get_target_circles(img)
go_to_pos_without_feedback(s, circles, servo_angles, H_array, V_array, channels)


"""
step6: accepting pixel coordinates from the user and tracking those
"""
go_to_pos_user(s, cap, M, servo_angles, H_array, V_array, channels)



