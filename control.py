
import cv2
import maestro
from mapping import *
import math as m
import numpy as np
from perception import *
import time



"""
go_to_pos() takes a target and makes the servo reach the target
using visual feedback. this function is used during the mapping stage
"""
def go_to_pos(s, channel, target, cap, M, axis):
    tolerance = 5

    img = get_cropped_img(cap, M)
    curr_pos_laser = get_laser_pos(img)

    if (axis == 'H'):
        error = abs(target[0] - curr_pos_laser[0])
        while (error > tolerance):
            signed_error = target[0] - curr_pos_laser[0]
            delta_angle = 0.5 * signed_error
            prev_servo_angle = s.getPosition(channel)
            new_servo_angle = s.setPosition(channel, prev_servo_angle + delta_angle)
            time.sleep(0.5)
            img = cap.read()
            img = get_cropped_img(img, M)
            curr_pos_laser = get_laser_pos(img)
            error = abs(target[0] - curr_pos_laser[0])

    elif (axis == 'V'):
        error = abs(target[1] - curr_pos_laser[1])
        while (error > tolerance):
            signed_error = target[1] - curr_pos_laser[1]
            delta_angle = 0.5 * signed_error
            prev_servo_angle = s.getPosition(channel)
            new_servo_angle = s.setPosition(channel, prev_servo_angle + delta_angle)
            time.sleep(0.5)
            img = cap.read()
            img = get_cropped_img(img, M)
            curr_pos_laser = get_laser_pos(img)
            error = abs(target[1] - curr_pos_laser[1])


"""
get_servo_commands() takes target pixel coords and 
generates the necessary servo angles, without visual feedback.
this is used after mapping is done.
"""
def get_servo_command(H_array, V_array, servo_angles, target):
    x = target[0]
    y = target[1]
    x_low = 0
    x_high = 0
    y_low = 0
    y_high = 0
    for i in range(len(H_array)-1):
        if ((x > H_array[i]) and (x < H_array[i+1])):
            x_low = i
            x_high = i+1
    for i in range(len(V_array)-1):
        if ((y > V_array[i]) and (y < V_array[i+1])):
            y_low = i
            y_high = i+1
    point1 = servo_angles[x_low][y_low]
    point2 = servo_angles[x_low][y_high]
    point3 = servo_angles[x_high][y_low]
    point4 = servo_angles[x_high][y_high]
    H_angle = (point1[0] + point2[0] + point3[0] + point4[0])//4
    V_angle = (point1[1] + point2[1] + point3[1] + point4[1])//4
    return H_angle, V_angle


"""
go_to_pos_without_feedback() takes a list of targets and 
moves the servo to reach those targets
"""
def go_to_pos_without_feedback(s, targets, servo_angles, H_array, V_array, channels):
    time.sleep(5)
    for target in targets:
        H_angle, V_angle = get_servo_command(H_array, V_array, servo_angles, target)
        s.setPosition(channels[0], H_angle)
        s.setPosition(channels[1], V_angle)
        time.sleep(5)


"""
go_to_pos_user() takes a single coord from user and follows
"""
def go_to_pos_user(s, cap, M, servo_angles, H_array, V_array, channels):
    img = get_cropped_img(cap, M)
    while(True):
        target = input("enter the pixel coordinates as a list [row, col]")
        time.sleep(2)
        go_to_pos_without_feedback(s, target, servo_angles, H_array, V_array, channels)
        k = cv2.waitKey(1)
        if (k == ord('q')):
            break
    print('exitting')
    return 0







