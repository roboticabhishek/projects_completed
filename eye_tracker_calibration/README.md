The aim of this project was to automate the calibration of an eye tracker, so that it won't be necessary to re-calibrate for every new user.

The setup consisted of-
A Screen, The eye tracker (paired to the screen), a Camera (facing the screen), and a servo-controlled mechanism which mimicked human eyes and on which a laser and artificial robotic eyes could be mounted

By pointing the laser on the screen at regular intervals, pixel co-ordinates and its corresponding servo command angles were recorded and stored as a grid. Image processing algorithms were used to detect laser position on the screen. Once a map/grid was formed, regression methods were used to interpolate between the grid points and generate servo commands to point the laser at the desired point on the screen. The Camera was used for visual feedback of the laser position. Once calibrated, the laser was replaced by artificial robotic eyes to fool the eye tracker.

main.py contains the main calibration routine  
control.py contains functions which mainly interface with the servo  
mapping.py contains functions which are related to generating pixel-servo map  
perception.py contains function used by the camera to detect laser, calibration points, screen warping, etc
