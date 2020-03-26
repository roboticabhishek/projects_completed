
from control import *
import cv2
import maestro
import math as m
import numpy as np
from perception import *
import time


"""
get_calib_points() takes an image as the input and 
returns 20 calibration points that the laser has to follow
"""
def get_calib_points(img):
    height, width, _ = img.shape
    offset = 50
    H_span = width - 2*offset
    V_span = height - 2*offset
    H_incr = H_span//4
    V_incr = V_span//3
    H_array = []
    V_array = []

    for i in range(5): H_array[i] = offset + H_incr*i
    for i in range(4): V_array[i] = offset + V_incr*i

    calib_points = []
    for v in V_array:
        for h in H_array:
            calib_points.append([v, h])

    return calib_points, H_array, V_array


"""
get_lookup() constructs the lookup table
"""
def get_lookup(s, channels, calib_points, cap, M, axes):
    servo_angles = []

    for calib_point in calib_points:
        go_to_pos(s, channels[0], calib_point, cap, M, axes[0])
        go_to_pos(s, channels[1], calib_point, cap, M, axes[1])
        curr_servo_angle = [s.getPosition(channels[0]), s.getPosition(channels[1])]
        servo_angles.append(curr_servo_angle)

    servo_angles = np.array(servo_angles)
    calib_points = np.array(calib_points)
    servo_angles = np.reshape(servo_angles, (4, 5))
    calib_points = np.reshape(calib_points, (4, 5))

    return servo_angles, calib_points








