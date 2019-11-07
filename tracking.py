import cv2
import numpy as np


def nothing(x):
    pass


cv2.namedWindow("Tracking")
# nothing = callback function
cv2.createTrackbar("lower hue", "Tracking", 0, 255, nothing)
cv2.createTrackbar("lower saturation", "Tracking", 0, 255, nothing)
cv2.createTrackbar("lower value", "Tracking", 0, 255, nothing)
cv2.createTrackbar("upper hue", "Tracking", 255, 255, nothing)
cv2.createTrackbar("upper saturation", "Tracking", 255, 255, nothing)
cv2.createTrackbar("upper value", "Tracking", 255, 255, nothing)
while True:

    frame = cv2.imread('smarties.png')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # trackbar positions
    l_h = cv2.getTrackbarPos("lower hue", "Tracking")
    l_s = cv2.getTrackbarPos("lower saturation", "Tracking")
    l_v = cv2.getTrackbarPos("lower value", "Tracking")

    u_h = cv2.getTrackbarPos("upper hue", "Tracking")
    u_s = cv2.getTrackbarPos("upper saturation", "Tracking")
    u_v = cv2.getTrackbarPos("upper value", "Tracking")
    # upper and lower values for blue
    # l_b = np.array([110, 50, 50])
    # u_b = np.array([130, 255, 255])
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    # hsv blue color range
    blue = cv2.inRange(hsv, l_b, u_b)

    # mask = the range
    res = cv2.bitwise_and(frame, frame, mask=blue)


    cv2.imshow("frame", frame)
    # these two are alterations
    cv2.imshow("mask", blue)
    cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
